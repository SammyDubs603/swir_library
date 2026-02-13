from io import StringIO
import csv

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session, joinedload

from app.core.db import get_db
from app.models.models import Material, Source, Spectrum
from app.schemas.schemas import IngestResponse, MaterialOut, SourceOut, SpectrumDownload, SpectrumOut
from app.services.spectrum_ops import swir_subset
from worker.ingest import run_connector

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/materials", response_model=list[MaterialOut])
def list_materials(query: str | None = None, category: str | None = None, db: Session = Depends(get_db)):
    stmt = select(Material)
    if query:
        q = f"%{query.lower()}%"
        stmt = stmt.where(
            or_(
                Material.name.ilike(q),
                Material.category.ilike(q),
            )
        )
    if category:
        stmt = stmt.where(Material.category == category)
    return db.execute(stmt.order_by(Material.name)).scalars().all()


@router.get("/materials/{material_id}", response_model=MaterialOut)
def get_material(material_id: int, db: Session = Depends(get_db)):
    material = db.get(Material, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material


@router.get("/sources", response_model=list[SourceOut])
def list_sources(db: Session = Depends(get_db)):
    return db.execute(select(Source).order_by(Source.name)).scalars().all()


@router.get("/spectra", response_model=list[SpectrumOut])
def list_spectra(
    material_id: int | None = None,
    value_type: str | None = None,
    min_nm: float = 900,
    max_nm: float = 2500,
    source: str | None = None,
    db: Session = Depends(get_db),
):
    stmt = select(Spectrum).options(joinedload(Spectrum.provenance)).join(Source)
    filters = []
    if material_id:
        filters.append(Spectrum.material_id == material_id)
    if value_type:
        filters.append(Spectrum.value_type == value_type)
    if source:
        filters.append(Source.name == source)
    if filters:
        stmt = stmt.where(and_(*filters))

    spectra = db.execute(stmt).unique().scalars().all()
    for item in spectra:
        w, v = swir_subset(item.wavelength_nm, item.value, min_nm, max_nm)
        item.wavelength_nm = w
        item.value = v
    return spectra


@router.get("/spectra/{spectrum_id}", response_model=SpectrumOut)
def get_spectrum(spectrum_id: int, db: Session = Depends(get_db)):
    spec = db.execute(select(Spectrum).options(joinedload(Spectrum.provenance)).where(Spectrum.id == spectrum_id)).unique().scalar_one_or_none()
    if not spec:
        raise HTTPException(status_code=404, detail="Spectrum not found")
    return spec


@router.get("/spectra/{spectrum_id}/download")
def download_spectrum(spectrum_id: int, format: str = Query("json", pattern="^(csv|json)$"), db: Session = Depends(get_db)):
    spec = db.get(Spectrum, spectrum_id)
    if not spec:
        raise HTTPException(status_code=404, detail="Spectrum not found")
    if not spec.redistributable:
        raise HTTPException(status_code=403, detail="License does not allow redistribution")
    if format == "json":
        return SpectrumDownload(
            id=spec.id,
            metadata={"material_id": spec.material_id, "source_id": spec.source_id, "value_type": spec.value_type},
            wavelength_nm=spec.wavelength_nm,
            value=spec.value,
        )
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["wavelength_nm", "value"])
    for w, v in zip(spec.wavelength_nm, spec.value):
        writer.writerow([w, v])
    return Response(content=buffer.getvalue(), media_type="text/csv")


@router.post("/admin/ingest/{connector}", response_model=IngestResponse)
def ingest(connector: str, db: Session = Depends(get_db)):
    inserted = run_connector(connector, db)
    return IngestResponse(connector=connector, inserted=inserted)

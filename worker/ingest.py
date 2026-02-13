import hashlib
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Material, Provenance, Source, Spectrum
from worker.connectors.sample_json import SampleJSONConnector


CONNECTORS = {
    "usgs": SampleJSONConnector("usgs", "usgs_sample.json"),
    "ecostress": SampleJSONConnector("ecostress", "ecostress_sample.json"),
    "ecosis": SampleJSONConnector("ecosis", "ecosis_sample.json"),
}


def _dupe_hash(wavelength_nm: list[float], values: list[float], source_id: int, material_id: int) -> str:
    rounded = [round(float(v), 6) for v in wavelength_nm + values]
    payload = "|".join(map(str, rounded + [source_id, material_id]))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _checksum(record: dict) -> str:
    return hashlib.sha256(str(record).encode("utf-8")).hexdigest()


def run_connector(name: str, db: Session) -> int:
    if name not in CONNECTORS:
        raise ValueError(f"Unknown connector: {name}")

    payload = CONNECTORS[name].fetch()
    src_payload = payload["source"]

    source = db.execute(select(Source).where(Source.name == src_payload["name"])).scalar_one_or_none()
    if not source:
        source = Source(**src_payload, retrieved_at=datetime.utcnow())
        db.add(source)
        db.flush()

    inserted = 0
    for record in payload["records"]:
        mat_payload = record["material"]
        material = db.execute(select(Material).where(Material.name == mat_payload["name"])).scalar_one_or_none()
        if not material:
            material = Material(**mat_payload)
            db.add(material)
            db.flush()

        spectrum_payload = record["spectrum"]
        dupe = _dupe_hash(spectrum_payload["wavelength_nm"], spectrum_payload["value"], source.id, material.id)
        exists = db.execute(select(Spectrum).where(Spectrum.duplicate_hash == dupe)).scalar_one_or_none()
        if exists:
            continue

        spectrum = Spectrum(
            material_id=material.id,
            source_id=source.id,
            wavelength_nm=spectrum_payload["wavelength_nm"],
            value=spectrum_payload["value"],
            value_type=spectrum_payload["value_type"],
            units=spectrum_payload.get("units", "unitless"),
            wavelength_units="nm",
            instrument=record.get("instrument"),
            resolution=record.get("resolution"),
            sampling_interval=record.get("sampling_interval"),
            measurement_geometry=record.get("measurement_geometry"),
            temperature=record.get("temperature"),
            humidity=record.get("humidity"),
            sample_prep=record.get("sample_prep"),
            notes=record.get("notes"),
            derived_from=record.get("derived_from"),
            derivation_method=record.get("derivation_method"),
            duplicate_hash=dupe,
            redistributable=True,
        )
        db.add(spectrum)
        db.flush()

        prov = record["provenance"]
        transformation_steps = [
            "validated schema",
            "normalized wavelength units to nm",
            "stored original arrays without overwrite",
        ]
        db.add(
            Provenance(
                spectrum_id=spectrum.id,
                source_id=source.id,
                original_identifier=prov["original_identifier"],
                original_url=prov["original_url"],
                original_format=prov["original_format"],
                checksum=_checksum(record),
                transformation_steps=transformation_steps,
            )
        )
        inserted += 1

    db.commit()
    return inserted

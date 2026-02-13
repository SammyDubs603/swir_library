from datetime import datetime
from typing import Any

from pydantic import BaseModel


class MaterialOut(BaseModel):
    id: int
    name: str
    category: str
    tags: list[str]
    synonyms: list[str]

    class Config:
        from_attributes = True


class SourceOut(BaseModel):
    id: int
    name: str
    url: str
    license: str
    citation_text: str
    access_method: str
    retrieved_at: datetime

    class Config:
        from_attributes = True


class ProvenanceOut(BaseModel):
    original_identifier: str
    original_url: str
    original_format: str
    checksum: str
    transformation_steps: list[str]

    class Config:
        from_attributes = True


class SpectrumOut(BaseModel):
    id: int
    material_id: int
    source_id: int
    wavelength_nm: list[float]
    value: list[float]
    value_type: str
    units: str
    wavelength_units: str
    instrument: str | None
    resolution: float | None
    sampling_interval: float | None
    measurement_geometry: str | None
    temperature: float | None
    humidity: float | None
    sample_prep: str | None
    notes: str | None
    derived_from: str | None
    derivation_method: str | None
    redistributable: bool
    provenance: ProvenanceOut | None = None

    class Config:
        from_attributes = True


class SpectrumDownload(BaseModel):
    id: int
    metadata: dict[str, Any]
    wavelength_nm: list[float]
    value: list[float]


class IngestResponse(BaseModel):
    connector: str
    inserted: int

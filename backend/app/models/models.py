from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Material(Base):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    category: Mapped[str] = mapped_column(String(120), index=True)
    tags: Mapped[list] = mapped_column(JSON, default=list)
    synonyms: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    spectra = relationship("Spectrum", back_populates="material")


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    url: Mapped[str] = mapped_column(Text)
    license: Mapped[str] = mapped_column(String(255), index=True)
    citation_text: Mapped[str] = mapped_column(Text)
    access_method: Mapped[str] = mapped_column(String(50))
    retrieved_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    spectra = relationship("Spectrum", back_populates="source")


class Spectrum(Base):
    __tablename__ = "spectra"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id"), index=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"), index=True)
    wavelength_nm: Mapped[list] = mapped_column(JSON)
    value: Mapped[list] = mapped_column(JSON)
    value_type: Mapped[str] = mapped_column(String(64), index=True)
    units: Mapped[str] = mapped_column(String(64), default="unitless")
    wavelength_units: Mapped[str] = mapped_column(String(32), default="nm")
    instrument: Mapped[str | None] = mapped_column(String(255), nullable=True)
    resolution: Mapped[float | None] = mapped_column(Float, nullable=True)
    sampling_interval: Mapped[float | None] = mapped_column(Float, nullable=True)
    measurement_geometry: Mapped[str | None] = mapped_column(String(255), nullable=True)
    temperature: Mapped[float | None] = mapped_column(Float, nullable=True)
    humidity: Mapped[float | None] = mapped_column(Float, nullable=True)
    sample_prep: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    derived_from: Mapped[str | None] = mapped_column(String(255), nullable=True)
    derivation_method: Mapped[str | None] = mapped_column(Text, nullable=True)
    duplicate_hash: Mapped[str] = mapped_column(String(128), index=True)
    redistributable: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    material = relationship("Material", back_populates="spectra")
    source = relationship("Source", back_populates="spectra")
    provenance = relationship("Provenance", back_populates="spectrum", uselist=False)


class Provenance(Base):
    __tablename__ = "provenance"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    spectrum_id: Mapped[int] = mapped_column(ForeignKey("spectra.id"), unique=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"))
    original_identifier: Mapped[str] = mapped_column(String(255))
    original_url: Mapped[str] = mapped_column(Text)
    original_format: Mapped[str] = mapped_column(String(64))
    checksum: Mapped[str] = mapped_column(String(128))
    transformation_steps: Mapped[list] = mapped_column(JSON, default=list)

    spectrum = relationship("Spectrum", back_populates="provenance")

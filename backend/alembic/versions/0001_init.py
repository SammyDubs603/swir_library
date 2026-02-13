"""init schema

Revision ID: 0001
"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "materials",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("category", sa.String(120), nullable=False),
        sa.Column("tags", sa.JSON, nullable=False),
        sa.Column("synonyms", sa.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )
    op.create_table(
        "sources",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False, unique=True),
        sa.Column("url", sa.Text, nullable=False),
        sa.Column("license", sa.String(255), nullable=False),
        sa.Column("citation_text", sa.Text, nullable=False),
        sa.Column("access_method", sa.String(50), nullable=False),
        sa.Column("retrieved_at", sa.DateTime, nullable=False),
    )
    op.create_table(
        "spectra",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("material_id", sa.Integer, sa.ForeignKey("materials.id"), nullable=False),
        sa.Column("source_id", sa.Integer, sa.ForeignKey("sources.id"), nullable=False),
        sa.Column("wavelength_nm", sa.JSON, nullable=False),
        sa.Column("value", sa.JSON, nullable=False),
        sa.Column("value_type", sa.String(64), nullable=False),
        sa.Column("units", sa.String(64), nullable=False),
        sa.Column("wavelength_units", sa.String(32), nullable=False),
        sa.Column("instrument", sa.String(255)),
        sa.Column("resolution", sa.Float),
        sa.Column("sampling_interval", sa.Float),
        sa.Column("measurement_geometry", sa.String(255)),
        sa.Column("temperature", sa.Float),
        sa.Column("humidity", sa.Float),
        sa.Column("sample_prep", sa.Text),
        sa.Column("notes", sa.Text),
        sa.Column("derived_from", sa.String(255)),
        sa.Column("derivation_method", sa.Text),
        sa.Column("duplicate_hash", sa.String(128), nullable=False),
        sa.Column("redistributable", sa.Boolean, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )
    op.create_table(
        "provenance",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("spectrum_id", sa.Integer, sa.ForeignKey("spectra.id"), unique=True),
        sa.Column("source_id", sa.Integer, sa.ForeignKey("sources.id"), nullable=False),
        sa.Column("original_identifier", sa.String(255), nullable=False),
        sa.Column("original_url", sa.Text, nullable=False),
        sa.Column("original_format", sa.String(64), nullable=False),
        sa.Column("checksum", sa.String(128), nullable=False),
        sa.Column("transformation_steps", sa.JSON, nullable=False),
    )


def downgrade():
    op.drop_table("provenance")
    op.drop_table("spectra")
    op.drop_table("sources")
    op.drop_table("materials")

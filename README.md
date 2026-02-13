# SWIR Spectra Library

Production-oriented monorepo for ingesting, normalizing, and serving SWIR spectra (900–2500 nm focus, with full-spectrum retention).

## Stack
- Backend: FastAPI + SQLAlchemy + Postgres
- Worker: Celery + Redis + connector interface
- Frontend: Next.js + Plotly overlay chart
- Orchestration: Docker Compose

## One-command local start
```bash
make up
```

## Run ingest
```bash
make ingest CONNECTOR=usgs
make ingest CONNECTOR=ecostress
make ingest CONNECTOR=ecosis
```

## Add connector
1. Implement `Connector` in `worker/connectors/`.
2. Return source + records payload (`material`, `spectrum`, `provenance`).
3. Register in `worker/ingest.py` `CONNECTORS` map.
4. Run `make ingest CONNECTOR=<name>`.

## Data conventions
- `wavelength_nm` stored in nm in DB.
- Original arrays never overwritten.
- SWIR range filtering done at query-time (`min_nm`, `max_nm`).
- Any derived field must set `derived_from` + `derivation_method`.
- Provenance stores checksum + transformation steps.

## Example API calls
```bash
curl http://localhost:8000/health
curl 'http://localhost:8000/materials?query=kaolinite'
curl 'http://localhost:8000/spectra?min_nm=900&max_nm=2500'
curl http://localhost:8000/spectra/1/download?format=csv
curl http://localhost:8000/sources
```

## License handling
Every source includes license metadata; non-redistributable spectra are blocked from download (`403`).

## Notes on sample data
This repo includes small demo spectra in `worker/sample_data/*.json` as connector-friendly fixtures for local development.

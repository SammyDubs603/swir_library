up:
	docker compose up --build

ingest:
	docker compose exec api python -c "from app.core.db import SessionLocal; from worker.ingest import run_connector; db=SessionLocal(); print(run_connector('$(CONNECTOR)', db)); db.close()"

test:
	docker compose exec api pytest -q

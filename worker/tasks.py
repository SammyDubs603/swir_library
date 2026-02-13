from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from worker.ingest import run_connector

celery_app = Celery("swir_worker", broker="redis://redis:6379/0")
engine = create_engine("postgresql://swir:swir@db:5432/swir")
SessionLocal = sessionmaker(bind=engine)


@celery_app.task
def ingest_connector(connector: str) -> int:
    db = SessionLocal()
    try:
        return run_connector(connector, db)
    finally:
        db.close()

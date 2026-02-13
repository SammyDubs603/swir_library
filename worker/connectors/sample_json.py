import json
from pathlib import Path

from worker.connectors.base import Connector


class SampleJSONConnector(Connector):
    def __init__(self, name: str, file_name: str):
        self.name = name
        self.file_name = file_name

    def fetch(self) -> dict:
        data_path = Path(__file__).resolve().parents[1] / "sample_data" / self.file_name
        with open(data_path, "r", encoding="utf-8") as fh:
            return json.load(fh)

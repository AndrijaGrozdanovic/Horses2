from pathlib import Path
import json


class JsonReader(object):
    BASE_PATH = Path(__file__).resolve().parent.parent / "JsonFiles"

    def __init__(self, file_name, base_path=BASE_PATH):
        self.file_name = file_name
        self.file_path = Path(base_path) / file_name
        self.data = None
        if not self.file_path.exists():
            raise FileNotFoundError(f"{self.file_path} not found")
        if self.data is None:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)

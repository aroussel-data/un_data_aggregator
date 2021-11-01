import json
import logging
import os
from datetime import datetime

import requests
from pymongo import MongoClient

from acquire_data.config import settings

logging.basicConfig(level="INFO")


class Fetcher:
    def __init__(self):
        self.session = requests.Session()
        self.target_url = settings.get("api", "api_url")
        self.filepath = f"data/{datetime.today().strftime('%Y-%m-%d')}-data.json"

    def _download_and_load_file(self):
        response = self.session.get(self.target_url)
        if not os.path.isfile(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as file_p:
                json.dump(response.json(), file_p, ensure_ascii=False, indent=4)
            self._load_file_into_db()
        else:
            logging.info(f"{self.filepath} already in data folder")

    def _load_file_into_db(self):
        client = MongoClient(os.environ.get("MONGODB_URL"))
        db = client["countries_db"]
        collection_conflict = db["conflict"]

        with open(self.filepath) as f:
            file_data = json.load(f)

        collection_conflict.insert_many(file_data["data"])
        client.close()
        logging.info("data loaded into DB")

    def run(self):
        logging.info(f"downloading files from {self.target_url}")
        self._download_and_load_file()

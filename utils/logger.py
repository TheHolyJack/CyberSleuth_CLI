import csv
import json
from datetime import datetime

class Logger():

    def log_csv(filename, data, headers=None):

        with open(filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers or data[0].keys())

            if f.tell() == 0:
                writer.writeheader()
            for row in data:
                writer.writerow(row)

    def log_json(filename, data):

        try:
            with open(filename, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            existing = []

        existing.append(data)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)


    def timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
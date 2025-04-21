import csv
import json

def add_rows_json(file_path: str, headers: list, rows: list[str]) -> list[list[str]]:
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for idx, escenario in enumerate(rows):
            e_name = f"e_{idx}"
            p_dict = {p: d for p, d in escenario}
            json_data = json.dumps(p_dict)
            writer.writerow([e_name,json_data])

def add_rows(file_path: str, headers: list, rows: list):
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
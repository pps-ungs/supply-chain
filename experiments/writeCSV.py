
import csv

def writeCSV(filename: str, rows: list):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerows(row) 
    print(f"Results has been successfully written in {filename}")
import csv
from typing import List, Dict

def save_to_csv(data: List[Dict[str, str]], output_file: str) -> None:
    """Save the extracted data to a CSV file."""
    if not data:
        print("No data to save.")
        return

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

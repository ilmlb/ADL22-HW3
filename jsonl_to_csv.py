import os
import csv
import argparse
from pathlib import Path
import jsonlines

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input_jsonl", 
        type=Path,
        help="Path to the jsonl file.",
        required=True
        )
    parser.add_argument(
        "-o", "--output_csv", 
        type=Path,
        help="Path to the csv file.",
        required=True
        )
    args = parser.parse_args()
    assert os.path.splitext(args.input_jsonl)[-1] == ".jsonl"
    assert os.path.splitext(args.output_csv)[-1] == ".csv"

    with jsonlines.open(args.input_jsonl) as f1, open(args.output_csv, 'w', encoding="utf-8") as f2:
        writer = csv.writer(f2)
        writer.writerow(["text", "summary", "id"])
        for obj in f1:
            summary = "摘要" if "title" not in obj else obj["title"]
            writer.writerow([obj["maintext"], summary, obj["id"]])
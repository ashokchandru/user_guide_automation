#!/usr/bin/env python3
"""
extract.py

Extract H1 sections from a Markdown file and convert each into a separate JSON file
matching the user's schema:

{
  "title": "H1 title",
  "sections": {
    "Body": "content"
  }
}

Usage:
    python3 extract.py input.md output_folder/
"""

import argparse
import json
import os
import re
from pathlib import Path


H1_PATTERN = re.compile(r"^# (.*)$")   # match H1 only


def sanitize_filename(title: str) -> str:
    """Convert title into the user's filename style."""
    fname = title.strip()
    fname = re.sub(r"[^\w]+", "_", fname)  # replace spaces & punctuation with _
    fname = re.sub(r"_+", "_", fname)      # collapse repeated _
    return fname + ".json"


def main():
    parser = argparse.ArgumentParser(description="Extract H1 sections into separate JSON files.")
    parser.add_argument("input_md", help="Path to input Markdown file")
    parser.add_argument("output_dir", help="Directory to store JSON files")
    args = parser.parse_args()

    input_path = Path(args.input_md)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise SystemExit(f"Markdown file not found: {input_path}")

    lines = input_path.read_text(encoding="utf-8").splitlines()

    current_title = None
    current_body = []

    def save_current():
        if not current_title:
            return
        fname = sanitize_filename(current_title)
        out_path = output_dir / fname
        data = {
            "title": current_title,
            "sections": {
                "Body": "\n".join(current_body).strip()
            }
        }
        out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Wrote {out_path.name}")

    for line in lines:
        h1_match = H1_PATTERN.match(line)
        if h1_match:
            # Save previous
            save_current()
            current_title = h1_match.group(1).strip()
            current_body = []
        else:
            if current_title:  # only capture body after first H1
                current_body.append(line)

    # Save last section
    save_current()

    print("Extraction completed.")


if __name__ == "__main__":
    main()

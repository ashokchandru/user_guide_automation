#!/usr/bin/env python3
"""
update.py

Apply content updates to multiple JSON files of the form:

{
  "title": "Title here",
  "sections": { "Body": "content" }
}

Usage:
    python3 update.py json_folder/ changes.json
"""

import argparse
import json
from pathlib import Path
import re


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def find_json_by_title(folder: Path, title: str):
    """Search for a JSON file whose 'title' matches exactly."""
    for file in folder.glob("*.json"):
        obj = load_json(file)
        if obj.get("title") == title:
            return file
    return None


def main():
    parser = argparse.ArgumentParser(description="Apply changes to JSON files.")
    parser.add_argument("json_folder", help="Folder containing JSON files")
    parser.add_argument("changes_json", help="JSON file specifying changes")
    args = parser.parse_args()

    folder = Path(args.json_folder)
    changes = load_json(Path(args.changes_json))

    for change in changes.get("changes", []):
        title = change["title"]
        action = change.get("action", "replace")
        new_content = change.get("new_content", "")

        target_file = find_json_by_title(folder, title)
        if not target_file:
            print(f"[WARN] No JSON file found for title: {title}")
            continue

        data = load_json(target_file)

        old_content = data["sections"]["Body"]

        if action == "replace":
            data["sections"]["Body"] = new_content
        elif action == "append":
            data["sections"]["Body"] = old_content + "\n" + new_content
        elif action == "prepend":
            data["sections"]["Body"] = new_content + "\n" + old_content
        else:
            print(f"[WARN] Unknown action '{action}' for: {title}")
            continue

        save_json(target_file, data)
        print(f"Updated → {target_file.name}")

    print("All updates completed.")


if __name__ == "__main__":
    main()

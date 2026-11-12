#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"
IMAGES = SRC / "assets" / "portfolio"
META = SRC / "metadata" / "portfolio"
EXTENSIONS = {".png", ".gif", ".jpg", ".jpeg", ".webp"}

META.mkdir(parents=True, exist_ok=True)
created = 0

# prompt the user on which folder to search
folder_name = input("Which folder? (blank for all): ").strip().strip("/")
root = (IMAGES / folder_name).resolve()

if not root.is_dir() or not root.is_relative_to(IMAGES):
    sys.exit(f"Folder not found. Aborting...")

print(f"searching {root.relative_to(IMAGES) if root != IMAGES else 'all folders'}")

# prompt the user on the kind of images they added
input_tags = str(input("What tags to use?: "))
extra_tags = [t.strip().strip("'\"") for t in input_tags.strip("[] ").split(",") if t.strip()]

for img in sorted(root.rglob("*")):
    if img.suffix.lower() not in EXTENSIONS:
        continue

    folder = img.parent.relative_to(IMAGES)
    md_dir = META / folder
    md = md_dir / f"{img.stem}.md"

    if md.exists():
        print(f"skipped {img.name}, already exists")
        continue

    tags = list(dict.fromkeys(extra_tags))

    image_path = os.path.relpath(img, md_dir).replace(os.sep, "/")
    date = datetime.fromtimestamp(img.stat().st_mtime).strftime("%Y-%m-%d")

    md_dir.mkdir(parents=True, exist_ok=True)
    md.write_text(
        "---\n"
        f"title: {json.dumps(img.stem)}\n"
        f"image: {json.dumps(image_path)}\n"
        f"date: {date}\n"
        f"tags: {json.dumps(tags)}\n"
        "---\n"
    )
    print(f"created {md.relative_to(SRC.parent)}")
    created += 1

print(f"done, {created} new file(s)")

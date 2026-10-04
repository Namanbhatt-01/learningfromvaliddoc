#!/usr/bin/env python3
"""
Scaffolding tool for adding a new technical study document + Reel script.
Usage:
    python3 scripts/new_study.py --type rfc --id 9114 --title "HTTP3"
    or simply:
    python3 scripts/new_study.py (for interactive prompts)
"""

import os
import sys
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

TYPE_MAP = {
    "rfc": {"dir": "rfcs", "template": "templates/RFC_TEMPLATE.md", "prefix": "RFC-"},
    "cve": {"dir": "cves", "template": "templates/CVE_TEMPLATE.md", "prefix": "CVE-"},
    "paper": {"dir": "research-papers", "template": "templates/PAPER_TEMPLATE.md", "prefix": ""},
    "standard": {"dir": "standards", "template": "templates/PAPER_TEMPLATE.md", "prefix": ""},
    "article": {"dir": "articles", "template": "templates/PAPER_TEMPLATE.md", "prefix": ""},
}

def slugify(text: str) -> str:
    cleaned = "".join(c if c.isalnum() or c in ("-", "_") else "-" for c in text.lower())
    return "-".join(filter(None, cleaned.split("-")))

def scaffold_study(study_type: str, item_id: str, title: str):
    study_type = study_type.lower()
    if study_type not in TYPE_MAP:
        print(f"❌ Error: Unknown study type '{study_type}'. Choose from: {list(TYPE_MAP.keys())}")
        sys.exit(1)

    info = TYPE_MAP[study_type]
    prefix = info["prefix"]
    clean_id = item_id.strip().upper()
    if prefix and not clean_id.startswith(prefix):
        clean_id = f"{prefix}{clean_id}"

    folder_name = slugify(f"{clean_id}-{title}" if clean_id else title)
    target_dir = REPO_ROOT / info["dir"] / folder_name

    if target_dir.exists():
        print(f"⚠️  Directory already exists: {target_dir}")
        proceed = input("Overwrite files? (y/N): ").strip().lower()
        if proceed != "y":
            print("Aborted.")
            sys.exit(0)

    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "assets").mkdir(exist_ok=True)
    (target_dir / "lab").mkdir(exist_ok=True)

    # 1. Study Notes README.md
    template_path = REPO_ROOT / info["template"]
    with open(template_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Pre-fill placeholders
    content = content.replace("[NUMBER]", clean_id)
    content = content.replace("[YEAR]-[ID]", clean_id)
    content = content.replace("[TITLE]", title)
    content = content.replace("[VULNERABILITY TITLE / SHORT NAME]", title)
    content = content.replace("[PAPER / STANDARD TITLE]", title)

    readme_file = target_dir / "README.md"
    with open(readme_file, "w", encoding="utf-8") as f:
        f.write(content)

    # 2. Reel Script reel-script.md
    reel_template_path = REPO_ROOT / "templates" / "REEL_SCRIPT_TEMPLATE.md"
    with open(reel_template_path, "r", encoding="utf-8") as f:
        reel_content = f.read()

    reel_content = reel_content.replace("[TOPIC NAME]", f"{clean_id}: {title}".strip(": "))
    reel_content = reel_content.replace("[TOPIC]", title)

    script_file = target_dir / "reel-script.md"
    with open(script_file, "w", encoding="utf-8") as f:
        f.write(reel_content)

    print("\n✅ Successfully created new study workspace!")
    print(f"📁 Directory: {target_dir.relative_to(REPO_ROOT)}")
    print(f"📝 Study Notes: {readme_file.relative_to(REPO_ROOT)}")
    print(f"🎬 Reel Script: {script_file.relative_to(REPO_ROOT)}")
    print(f"🔬 Lab PoC Folder: {target_dir.relative_to(REPO_ROOT)}/lab")
    print(f"🖼️  Assets Folder: {target_dir.relative_to(REPO_ROOT)}/assets\n")

def main():
    parser = argparse.ArgumentParser(description="Scaffold a new technical document study workspace.")
    parser.add_argument("--type", choices=list(TYPE_MAP.keys()), help="Type of document (rfc, cve, paper, standard, article)")
    parser.add_argument("--id", help="Identifier (e.g. 9114 for RFC, 2024-3094 for CVE, 2017 for Paper year)")
    parser.add_argument("--title", help="Title of the topic/document")

    args = parser.parse_args()

    if not args.type:
        print("--- 📚 New Technical Study Generator ---")
        print("Available types: " + ", ".join(TYPE_MAP.keys()))
        doc_type = input("Choose document type: ").strip().lower()
        doc_id = input("Identifier (e.g. 9114, 2024-3094, 2017, or blank): ").strip()
        doc_title = input("Document Title: ").strip()
        scaffold_study(doc_type, doc_id, doc_title)
    else:
        scaffold_study(args.type, args.id or "", args.title or "Untitled")

if __name__ == "__main__":
    main()

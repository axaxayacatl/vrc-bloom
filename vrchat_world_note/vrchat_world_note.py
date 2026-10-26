

#!/usr/bin/env python3
"""VRChat World Note — a tiny local notes tool. Python standard library only."""

import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).with_name("vrchat_world_notes.json")


def load_notes():
    if not DATA_FILE.exists():
        return []
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Could not read the notes file; starting with an empty list.")
        return []


def save_notes(notes):
    DATA_FILE.write_text(json.dumps(notes, ensure_ascii=False, indent=2), encoding="utf-8")


def show_notes(notes):
    if not notes:
        print("\nNo notes yet. Add one with option 1.")
        return
    print()
    for i, note in enumerate(notes, 1):
        print(f"{i}. [{note.get('kind', 'Note')}] {note.get('title', '(untitled)')}")
        print(f"   {note.get('details', '')}")
        print(f"   Saved: {note.get('created', 'unknown date')}\n")


def main():
    notes = load_notes()
    while True:
        print("\n=== VRCHAT WORLD NOTE ===")
        print("1. Add a note\n2. View all notes\n3. Search notes\n4. Delete a note\n5. Export notes as text\n0. Exit")
        choice = input("> ").strip()

        if choice == "1":
            kind = input("Type (World / Avatar / Creator / Instance / Idea / Other): ").strip() or "Note"
            title = input("Title or world name: ").strip()
            if not title:
                print("A title is required.")
                continue
            details = input("Details, link, or revisit reminder: ").strip()
            notes.append({
                "kind": kind,
                "title": title,
                "details": details,
                "created": datetime.now().astimezone().isoformat(timespec="minutes"),
            })
            save_notes(notes)
            print("Saved locally.")

        elif choice == "2":
            show_notes(notes)

        elif choice == "3":
            term = input("Search text: ").strip().casefold()
            matches = [n for n in notes if any(
                term in n.get(field, "").casefold()
                for field in ("title", "details", "kind")
            )]
            show_notes(matches)

        elif choice == "4":
            show_notes(notes)
            if notes:
                try:
                    number = int(input("Number to delete (0 cancels): "))
                    if number == 0:
                        continue
                    if 1 <= number <= len(notes):
                        removed = notes.pop(number - 1)
                        save_notes(notes)
                        print(f"Deleted: {removed.get('title', '(untitled)')}")
                    else:
                        print("That number is out of range.")
                except ValueError:
                    print("Enter a number.")

        elif choice == "5":
            export_path = DATA_FILE.with_name("vrchat_world_notes.txt")
            lines = ["VRCHAT WORLD NOTE", "=" * 18, ""]
            for i, note in enumerate(notes, 1):
                lines.extend([
                    f"{i}. [{note.get('kind', 'Note')}] {note.get('title', '(untitled)')}",
                    note.get("details", ""),
                    f"Saved: {note.get('created', 'unknown date')}",
                    "",
                ])
            export_path.write_text("\n".join(lines), encoding="utf-8")
            print(f"Exported to: {export_path}")

        elif choice == "0":
            print("See you in the worlds.")
            break
        else:
            print("Choose one of the listed options.")


if __name__ == "__main__":
    main()


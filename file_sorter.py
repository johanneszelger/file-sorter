import json
import os
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Union


def log_dir_creation(dir: Union[Path, str], created: bool, log_path: str):
    if not created:
        return

    if not os.path.exists(log_path):
        log_data = []
    else:
        with open(log_path, "r") as file:
            log_data = json.load(file)

    log_data.append({"created": str(dir)})

    with open(log_path, "w") as file:
        json.dump(log_data, file, indent=4)

def log_movement(original: Union[Path, str], new: Union[Path, str], log_path: str):
    if not os.path.exists(log_path):
        log_data = []
    else:
        with open(log_path, "r") as file:
            log_data = json.load(file)

    log_data.append({"original": str(original), "new": str(new)})

    with open(log_path, "w") as file:
        json.dump(log_data, file, indent=4)


def move_file(file: Path, target_dir: Path, simulate: bool, log_path: str):
    if not simulate:
        created = not os.path.exists(target_dir)
        log_dir_creation(target_dir, created, log_path)
        target_dir.mkdir(exist_ok=True)
        shutil.move(str(file), str(target_dir / file.name))
        log_movement(file, target_dir / file.name, log_path)
        print(f"Moving {file.name} to {target_dir}")
    else:
        print(f"Would move {file.name} to {target_dir}")


def undo_last_organization(log_path: str):
    if not os.path.exists(log_path):
        print(f"No log file found at {log_path}. Cannot undo.")
        return

    with open(log_path, "r") as file:
        log_data = json.load(file)

    for entry in reversed(log_data):
        if "original" not in entry or "new" not in entry:
            continue
        original = Path(entry["original"])
        new = Path(entry["new"])
        if new.exists():
            shutil.move(str(new), str(original))
            print(f"Moved {new.name} back to {original}")
        else:
            print(f"File {new.name} not found. Skipping.")

    for entry in reversed(log_data):
        if "created" not in entry:
            continue
        created = Path(entry["created"])
        if created.exists():
            shutil.rmtree(str(created))
            print(f"Delete dir {created}")
        else:
            print(f"File {created} not found. Skipping.")

    os.remove(log_path)
    print("Undo completed.")


def organize_by_type(path: str, simulate: bool, log_file: str):
    for item in os.listdir(path):
        file = Path(path) / item
        if file.is_file():
            file_type = file.suffix.lower().strip('.')
            target_dir = Path(path) / file_type
            move_file(file, target_dir, simulate, log_file)


def organize_by_date(path: str, simulate: bool, log_file: str):
    for item in os.listdir(path):
        file = Path(path) / item
        if file.is_file():
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            date_folder = mtime.strftime("%Y-%m-%d")
            target_dir = Path(path) / date_folder
            move_file(file, target_dir, simulate, log_file)


def organize_by_size(path: str, simulate: bool, log_file: str, small: int, medium: int, large: int):
    for item in os.listdir(path):
        file = Path(path) / item
        if file.is_file():
            size = file.stat().st_size
            if size < small:  # less than 1MB
                size_folder = 'Small'
            elif size < medium:  # less than 10MB
                size_folder = 'Medium'
            elif size < large:
                size_folder = 'Large'
            else:
                print(f"File {file} too large. Skipping.")
            target_dir = Path(path) / size_folder
            move_file(file, target_dir, simulate, log_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files in a directory.")
    parser.add_argument('--path', type=str, help="Path to the directory to be organized", required=True)
    parser.add_argument('--type', action='store_true', help="Organize by file type")
    parser.add_argument('--date', action='store_true', help="Organize by file modification date")
    parser.add_argument('--size', action='store_true', help="Organize by file size")
    parser.add_argument('--simulate', action='store_true', help="Simulate the organization process")
    parser.add_argument('--undo', action='store_true', help="Undo the last organization")
    parser.add_argument('--history', action='store_true',
                        help="Give a file path to store the history in. This file is used to undo changes",
                        default=f"history_{datetime.now()}.json")
    parser.add_argument('--small', type=int, default=10 ** 6, help="Upper limit for small files in bytes")
    parser.add_argument('--medium', type=int, default=10 ** 7, help="Upper limit for medium files in bytes")
    parser.add_argument('--large', type=int, default=10 ** 15, help="Upper limit for large files in bytes")
    args = parser.parse_args()

    log_file = args.history

    if args.undo:
        undo_last_organization(log_file)
    else:
        if args.type:
            organize_by_type(args.path, args.simulate, log_file)
        if args.date:
            organize_by_date(args.path, args.simulate, log_file)
        if args.size:
            organize_by_size(args.path, args.simulate, log_file, args.small, args.medium, args.large)

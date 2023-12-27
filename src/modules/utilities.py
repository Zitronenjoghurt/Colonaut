import json
import os
from pathlib import Path

ROOT_DIR = str(Path(__file__).parent.parent.parent)
SAFE_TO_DELETE = ["game_state.json", "global_state.json"]

def file_exists(file_path: str) -> bool:
    return os.path.exists(file_path)

def file_to_dict(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def dict_to_file(file_path: str, data: dict):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4) 

def delete_file(file_path: str) -> None:
    for deletable_file in SAFE_TO_DELETE:
        if deletable_file in file_path:
            break
        raise RuntimeError("Tried to delete file that is not allowed to be deleted.")
    if file_exists(file_path=file_path):
        os.remove(file_path)

def construct_path(relative_path: str) -> str:
    path_parts = relative_path.split("/")
    absolute_path = os.path.join(ROOT_DIR, *path_parts)
    return absolute_path
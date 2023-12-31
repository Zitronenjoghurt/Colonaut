import cbor2
import json
import os
from pathlib import Path
from typing import Optional

ROOT_DIR = str(Path(__file__).parent.parent.parent)
SAFE_TO_DELETE = ["game_state.json", "global_state.json"]

def file_exists(file_path: str) -> bool:
    return os.path.exists(file_path)

def file_to_dict(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise RuntimeError("Deserialized data is not a dictionary.")
    return data

def cbor_file_to_dict(file_path: str) -> dict:
    with open(file_path, 'rb') as f:
        data_bytes = f.read()
    data = cbor2.loads(data_bytes)
    if not isinstance(data, dict):
        raise RuntimeError("Deserialized data is not a dictionary.")
    return data

def dict_to_file(file_path: str, data: dict):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def dict_to_cbor_file(file_path: str, data: dict):
    data_bytes = cbor2.dumps(data)
    with open(file_path, 'wb') as f:
        f.write(data_bytes)

def str_to_file(file_path: str, string: str):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(string)

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

# Returns a list of files in the given directory with a specific suffix
def files_in_directory(path: str, suffix: Optional[str] = None) -> list[str]:
    if not os.path.exists(path):
        raise ValueError(f"Directory {path} does not exist.")
    
    files = []
    for file in os.listdir(path):
        if suffix is not None:
            if suffix in file:
                files.append(file)
        else:
            files.append(file)
    return files
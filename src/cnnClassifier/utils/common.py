import os
import json
import base64
from pathlib import Path
from typing import Any, Iterable

from box import ConfigBox
from box.exceptions import BoxValueError

from cnnClassifier import logger

# --- Python 3.12 compatibility: drop-in shim for ensure.ensure_annotations ---
# If the legacy 'ensure' package is unavailable or incompatible, we use a no-op decorator.
try:
    from ensure import ensure_annotations  # type: ignore
except Exception:  # pragma: no cover
    def ensure_annotations(func=None, **kwargs):
        if func is None:
            def deco(f):
                return f
            return deco
        return func
# ---------------------------------------------------------------------------


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Read a YAML file and return its content as a ConfigBox.

    Args:
        path_to_yaml (Path): path to a YAML file.

    Raises:
        ValueError: if the YAML file is empty.

    Returns:
        ConfigBox: object exposing keys as attributes.
    """
    try:
        import yaml  # local import to keep base deps minimal
        with open(path_to_yaml, "r", encoding="utf-8") as yaml_file:
            content = yaml.safe_load(yaml_file)
            if content is None:
                raise BoxValueError("empty yaml")
            logger.info(f"YAML file loaded: {path_to_yaml}")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: Iterable[Path], verbose: bool = True) -> None:
    """
    Create a list of directories if they don't exist.

    Args:
        path_to_directories (Iterable[Path]): directories to create.
        verbose (bool): log creation messages.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory: {path}")


@ensure_annotations
def save_json(path: Path, data: dict) -> None:
    """
    Save a dictionary to a JSON file.

    Args:
        path (Path): destination path.
        data (dict): serializable dictionary.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    logger.info(f"JSON saved at: {path}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    Load JSON file content.

    Args:
        path (Path): source path.

    Returns:
        ConfigBox: data as attributes instead of dict.
    """
    with open(path, "r", encoding="utf-8") as f:
        content = json.load(f)
    logger.info(f"JSON loaded from: {path}")
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path) -> None:
    """
    Save a Python object to a binary file via joblib.

    Args:
        data (Any): object to persist.
        path (Path): destination path.
    """
    import joblib  # local import
    joblib.dump(value=data, filename=path)
    logger.info(f"Binary saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """
    Load a Python object from a joblib file.

    Args:
        path (Path): source path.

    Returns:
        Any: deserialized object.
    """
    import joblib  # local import
    obj = joblib.load(path)
    logger.info(f"Binary loaded from: {path}")
    return obj


@ensure_annotations
def get_size(path: Path) -> str:
    """
    Get file size as a friendly string in KB.

    Args:
        path (Path): file path.

    Returns:
        str: size in KB (rounded).
    """
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {size_in_kb} KB"


@ensure_annotations
def decodeImage(imgstring: str, fileName: str) -> None:
    """
    Decode a base64 string and write it to a file.

    Args:
        imgstring (str): base64-encoded image string.
        fileName (str): output file path.
    """
    imgdata = base64.b64decode(imgstring)
    with open(fileName, "wb") as f:
        f.write(imgdata)


@ensure_annotations
def encodeImageIntoBase64(croppedImagePath: str) -> bytes:
    """
    Read an image file and return its base64-encoded bytes.

    Args:
        croppedImagePath (str): input image path.

    Returns:
        bytes: base64-encoded content.
    """
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())

import os
from box.exception import BoxValueError
from box import ConfigBox 
import yaml
from src.TextSummarizer.logging import logger
from ensure import ensure_annotations
from pathlib import Path
from typing import Any

@ensure_annotations
def read_yaml(path_to_yaml: Path)->ConfigBox:
    try:
        with open(path_to_yaml) as f_yaml:
            content=yaml.safe_load(path_to_yaml)
            logger.info(f"yaml file {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("Yaml file is empty")      
    except Exception as e:
        raise e
@ensure_annotations
def create_directories(path_to_dir : list, verbose=True):
    for dir in path_to_dir:
        os.makedirs(dir, exist_ok=True)
        if verbose:
            logger.info(f"{dir} directory created")
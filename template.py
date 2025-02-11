import os
from pathlib import Path
import logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')
project_name="TextSummarizer"


list_of_files=[
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
     f"src/{project_name}/logging/__init__.py",
    f"src/{project_name}/constants/__init__.py",
    "config/config.yaml",
    "params.yaml",
    "main.py",
    "schema.yaml",
    "Dockerfile",
    "setup.py",
    "app.py",
    "requirements.txt",
    "research/research.ipynb"

]

for files in list_of_files:
    file=Path(files)
    file_dir,file_name=os.path.split(file)

    if file_dir !="" :
        os.makedirs(file_dir,exist_ok=True)
        logging.info(f"Creating directory {file_dir} for {file_name}")

    if (not os.path.exists(file))or (os.path.getsize(file)==0) :
        with open(file,"w") as f:
            pass
            logging.info(f"creating empty files: {file}")
    else:
        logging.info(f"File {file} already exists")

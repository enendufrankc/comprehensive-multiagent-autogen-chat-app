import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "autogen_project"

list_of_files = [
    f"src/__init__.py",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/settings.py",
    f"src/{project_name}/readers/__init__.py",
    f"src/{project_name}/readers/wikipedia_reader.py",
    f"src/{project_name}/indexing/__init__.py",
    f"src/{project_name}/indexing/index_functions.py",
    f"src/{project_name}/utilities/__init__.py",
    f"src/{project_name}/utilities/utils.py",
    f"src/{project_name}/agents/__init__.py",
    f"src/{project_name}/agents/autogen_agents.py",
    f"src/{project_name}/chat_manager/__init__.py",
    f"src/{project_name}/chat_manager/group_chat_manager.py",
    "requirements.txt",
    "setup.py",
    "README.md",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for file: {filename}")

    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        with open(filepath, "w") as f:
            pass  # Creates an empty file
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")


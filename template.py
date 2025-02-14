import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO,format='[%(asctime)s]:%(message)s:')
                    

list_of_files=[
    "src/__init__.py",
    "src/database.py",
    "src/langchain_utils.py",
    "src/examples.py",
    "src/chains.py",
    "src/prompts.py",
    "src/table_details.py",
    ".env",
    "setup.py",
    "research/trials.ipynb",
    "requirements.txt"

]

for filepath in list_of_files:
    filepath=Path(filepath)
    filedir,filename=os.path.split(filepath)

    if filedir!= "":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"creating directory ;{filedir} for the file {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0): 
        with open(filepath,"w") as f:
            pass
            logging.info(f"creating empty file {filepath}")
    else:
        logging.info(f"{filename} already exists")
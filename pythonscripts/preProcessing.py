import shutil
import logging
from configReader import ConfigReader

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Fetch config reader
try:
    path_config = ConfigReader.get_path_config()
    # Get paths from config
    source_folder = path_config.landing_folder
    destination_folder = path_config.processing_folder
    file_name = path_config.file_name 
    # To do: filename to accept regex
    logging.info(f"Path Config: {path_config}")  

except Exception as e:
    logging.error(f"Error reading config: {e}")

try: 
    shutil.move(f"{source_folder}/{file_name}", f"{destination_folder}/{file_name}")
    logging.info(f"{file_name} moved successfully to folder {destination_folder}")    

except Exception as e:
    logging.error(f"Error moving file from source to landing: {e}")
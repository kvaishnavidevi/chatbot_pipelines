import shutil
import configparser

# Read config file
config = configparser.ConfigParser()
config.read("config.ini")

# Get paths from config
source_folder = config["PATHS"]["landing_folder"]
destination_folder = config["PATHS"]["processing_folder"]

# Define file name
file_name = "dataset.json"

# Move file
shutil.move(f"{source_folder}/{file_name}", f"{destination_folder}/{file_name}")

print("File moved successfully!")

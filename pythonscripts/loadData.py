import json
import pandas as pd
import psycopg2
import shutil
import logging
import random
from configReader import ConfigReader

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Fetch config reader
try:
    path_config = ConfigReader.get_path_config()
    # Get paths from config
    processing_folder = path_config.processing_folder
    file_name = path_config.file_name 
    success_folder = path_config.success_folder
    error_folder = path_config.error_folder
    logging.info(f"Path Config: {path_config}") 
    db_config = ConfigReader.get_database_config()
    logging.info(f"DB Config: {db_config}")  

except Exception as e:
    logging.error(f"Error reading config: {e}")

try:
    logging.info(f"Processing Folder: {processing_folder}")
    with open(f"{processing_folder}/{file_name}", "r", encoding="utf-8") as file:
        data = json.load(file)
        logging.debug(type(data))
        
except FileNotFoundError:
    logging.error(f"Error: File {file_name} was not found in {processing_folder}")
except json.JSONDecodeError:
    logging.error("Error: Invalid JSON format.")
    shutil.move(f"{processing_folder}/{file_name}", f"{error_folder}/{file_name}")

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=db_config.database,
    user=db_config.user,
    password=db_config.password,
    host=db_config.host,
    port=db_config.port
)
cur = conn.cursor()
user_ids = ["user1", "user2", "user3", "user4","user5","user6","user7","user8","user9","user10"]

# Select a random user ID

try:
# Step 2: Loop Through Conversations
    for conversation in data:
        conversation_id = conversation["id"]
        conv_user_id = random.choice(user_ids)
        conv_seqno = 1  # Access "id" field correctly
        for message in conversation["messages"]:
            role = message["role"]
            content = message["content"]
            conv = content[:8000]
            cur.execute(
                "INSERT INTO ai_conversations (conv_id, conv_role,conv_seqno, conversations,conv_userid) VALUES (%s, %s, %s, %s, %s);",
                (conversation_id, role,conv_seqno, conv,conv_user_id)
            )
            conv_seqno = conv_seqno+1

    conn.commit()
    shutil.move(f"{processing_folder}/{file_name}", f"{success_folder}/{file_name}")
    logging.info(f"Conv data {len(data)} inserted successfully!")
except Exception as e:
    # Move file to error folder
    conn.rollback()  # 
    shutil.move(f"{processing_folder}/{file_name}", f"{error_folder}/{file_name}")
    # Insert error details into error_log table
    logging.error(e)
    error_message = str(e)[:500]
    cur.execute(
        "INSERT INTO ai_conv_loaderror (filename,error_message) VALUES (%s,%s);",
        (file_name, error_message,)
    )
    conn.commit()
    logging.error(f"Error occurred! Moved file to {error_folder} and logged error.")
cur.close()
conn.close()
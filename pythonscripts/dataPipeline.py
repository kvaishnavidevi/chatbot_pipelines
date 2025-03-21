import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Step 1: Run Preprocessing
logging.info("Step 1: Running Preprocessing...")
subprocess.run(["python", "preProcessing.py"])
logging.info("Preprocessing completed")

# Step 2: Run Data Loading
logging.info("Step 2: Running Data Loading...")
subprocess.run(["python", "loadData.py"])
logging.info("Data Loading completed..")
logging.info("Data Pipeline Execution Completed!")
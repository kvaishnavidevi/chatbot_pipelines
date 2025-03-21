# Evolve Chat Interaction Dashboard

## Overview

This project sets up a dashboard to track and visualize chatbot interactions using PostgreSQL, Python, and Dash. The setup involves database initialization, script execution, and launching a web-based dashboard.

## Prerequisites

- **PostgreSQL**: Ensure PostgreSQL is installed and running.
- **Python 3.x**: Install Python and required libraries.

## 1. Database Setup

Run the following SQL scripts in the given order to set up the required database tables:

**Download from:** [GitHub Repository](https://github.com/kvaishnavidevi/chatbot_pipelines/tree/main/db_scripts)

```sh
ai_groups.sql
ai_users.sql
ai_conversations.sql
ai_roles.sql
ai_conv_loaderrors.sql
ai_role_user_mapping.sql
```

## 2. Install Required Python Libraries

Execute the following command to install necessary dependencies:

```sh
pip install psycopg2 shutil configparser dash sqlalchemy plotly wordcloud
```

## 3. Configuration Setup

Update the `config.ini` file with the following details:

```ini
[PATHS]
landing_folder = D:\evollve\landing\
processing_folder = D:\evollve\processing\
success_folder = D:\evollve\success\
error_folder = D:\evollve\error\
file_name = dataset.json

[postgresql]
host = localhost
port = 5433
database = Evolve
user = postgres
password =
```

## 4. Generate Encrypted Password

Run the `encryptPassword.py` script:

```sh
python encryptPassword.py
```

### Steps:

1. Copy the encryption key from `encryptPassword.py` and paste it in `configReader.py`.
2. Copy the encrypted password and update `config.ini`.

[Encryption Script](https://github.com/kvaishnavidevi/chatbot_pipelines/blob/main/pythonscripts/encryptPassword.py)

## 5. Running the Data Pipeline

### Step 1: Execute `dataPipeline.py`

```sh
python dataPipeline.py
```

This script will:

- Move `dataset.json` from `landing_folder` to `processing_folder`.
- Load data into `ai_conversations`.
- Move the processed file to `success_folder` or `error_folder` based on execution status.

## 6. Running the Dashboard

### Step 2: Run `dashboard.py`

```sh
python dashboard.py
```

The dashboard will be accessible at: [http://127.0.0.1:8050](http://127.0.0.1:8050)

## License

This project is licensed under the MIT License.



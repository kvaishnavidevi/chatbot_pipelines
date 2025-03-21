import configparser
from cryptography.fernet import Fernet

class DatabaseConfig:
   #DBConfig object
    def __init__(self, host, port,database,user,password):
        self.host = host
        self.port = port 
        self.database = database
        self.user = user
        self.password = password

    def __repr__(self):
        return f"DatabaseConfig(host='{self.host}', port='{self.port}',database='{self.database},user='{self.user}')"  
    
class PathConfig:
    #Path config object 
    def __init__(self, processing_folder, error_folder, success_folder,file_name,landing_folder):
        self.processing_folder = processing_folder
        self.error_folder = error_folder
        self.success_folder = success_folder
        self.file_name = file_name
        self.landing_folder = landing_folder

    def __repr__(self):
        return f"PathConfig(processing_folder='{self.processing_folder}', error_folder='{self.error_folder}', success_folder='{self.success_folder}', file_name='{self.file_name}', landing_folder='{self.landing_folder}')"
    
class ConfigReader:
    config_file = "config.ini"
    encryption_key = b'QoTRfPj26ZPbQCm0TIjxodjdzqyImYk0oITSG6Ner_A='
    # Handles config file reading and decryption
    def __init__(self):
       
        self._load_config()

    # fetch db configs
    @staticmethod
    def get_database_config():
        config = configparser.ConfigParser()
        config.read(ConfigReader.config_file)
        cipher_suite = Fernet(ConfigReader.encryption_key)
        db_required_fields = ["host", "port","database","user","password"]

        if "postgresql" not in config:
            raise ValueError("Missing postgresql section in config file")

        for field in db_required_fields:
            if field not in config["postgresql"] or not config["postgresql"][field].strip():
                raise ValueError(f"Missing or empty '{field}' in config file under postgresql")
            
        user = config["postgresql"]["user"]
        host = config["postgresql"]["host"]
        database = config["postgresql"]["database"]
        port = config["postgresql"]["port"]
        encrypted_password = config["postgresql"]["password"].encode()
        password = cipher_suite.decrypt(encrypted_password).decode()

        return DatabaseConfig(host,port,database,user,password)
    
    # fetch path related configs
    @staticmethod
    def get_path_config():
        config = configparser.ConfigParser()
        config.read(ConfigReader.config_file)
        path_required_fields = ["processing_folder","error_folder","success_folder","file_name","landing_folder"]

        if "PATHS" not in config:
                raise ValueError("Missing PATHS section in config file")
        for field in path_required_fields:
            if field not in config["PATHS"] or not config["PATHS"][field].strip():
                raise ValueError(f"Missing or empty '{field}' in config file under paths")
            
        processing_folder = config["PATHS"]["processing_folder"]
        error_folder = config["PATHS"]["error_folder"]
        success_folder = config["PATHS"]["success_folder"]
        landing_folder = config["PATHS"]["landing_folder"]
        file_name = config["PATHS"]["file_name"]

        return PathConfig(processing_folder, error_folder,success_folder,file_name,landing_folder)
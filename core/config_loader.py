import os
import yaml
import warnings
from dotenv import load_dotenv

class ConfigLoader:
    def __init__(self, config_path='config.yaml', env_path='.env'):
       self.load_from_yaml(config_path)
       self.load_from_env(env_path)

    def load_from_yaml(self, config_path='config.yaml'):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

        self.ollama_base_url=config['ollama']['base_url']
        self.default_model=config['ollama']['default_model']
        self.temperature=config['ollama']['temperature']
        self.output_folder_path=config['output']['folder_path']
        self.summary_sample_rows=config['summary']['sample_rows']

        self.drive_folder_id=config['google_drive']['folder_id']
    
    def load_from_env(self, env_path='.env'):
        load_dotenv(env_path)
        self.google_drive_credentials=os.getenv('GOOGLE_DRIVE_CREDENTIALS')
        if self.google_drive_credentials is None:
            warnings.warn("GOOGLE_DRIVE_CREDENTIALS not found in environment variables. Google Drive integration will not work.")

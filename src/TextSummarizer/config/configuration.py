from src.TextSummarizer.constants import *
from src.TextSummarizer.utils.common import * 
from src.TextSummarizer.entity import DataIngestionConfig
class ConfigurationManager:
    def __init__(self,
                 config_file=CONFIG_FILE_PATH,
                 param_file=PARAM_FILE_PATH) :
        self.config=read_yaml(config_file)
        self.params=read_yaml(param_file)

        create_directories([self.config.artifacts_root])
    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config=self.config.data_ingestion
        create_directories([config.root_dir])

        data_ingestion_config=DataIngestionConfig(
            root_dir=config.root_dir,
            source_url=config.source_url,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )
        return data_ingestion_config
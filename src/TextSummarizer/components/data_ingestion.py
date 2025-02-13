import os
import urllib.request as request
import zipfile
from src.TextSummarizer.logging import logger
from src.TextSummarizer.entity import DataIngestionConfig
class DataIngestion:
    def __init__(self, config:DataIngestionConfig):
        self.config=config
    def download_file(self):
        if not os.path.exists(self.config.local_data_file) :
            filename, hearders=request.urlretrieve(
                url=self.config.source_url,
                filename=self.config.local_data_file
            )
            logger.info(f"File is downloaded")
        else:
            logger.info(f"File already exists")

    def extract_zip_file(self):
        unzip_dir=self.config.unzip_dir
        os.makedirs(unzip_dir,exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_file:
            zip_file.extractall(unzip_dir)
            

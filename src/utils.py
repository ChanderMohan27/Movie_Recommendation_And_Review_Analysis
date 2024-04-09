import yaml
import sys
from logger import logging
from exception import CustomException
sys.path.append("..")

class YamlReader:
    def __init__(self, file_path="params.yaml"):
        self.file_path = file_path
 
    def read_param(self):
        try:
            logging.info("Trying to open Param.yaml file")
            with open(self.file_path) as yaml_file:
                config = yaml.safe_load(yaml_file)
            logging.info("Successfully opened the yaml file")
            return config
        except Exception as e:
            raise CustomException(e, sys)


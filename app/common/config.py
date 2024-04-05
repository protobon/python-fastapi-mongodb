import yaml
from app.common.constants import Constants


class Config:
    config = dict()
    mongo = dict()

    def __init__(self, config: dict):
        self.config = config

    def load_mongodb(self):
        mongo_config = dict()
        yaml.load(self.config[Constants.MONGODB], mongo_config)


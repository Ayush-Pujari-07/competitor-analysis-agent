import sys

from pymongo.mongo_client import MongoClient
from pymongo.errors import PyMongoError

from competitor_analysis_agent.logger import logger
from competitor_analysis_agent.constants import MONGO_URI
from competitor_analysis_agent.exception import CustomException


class MongoClientManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def initialize_mongo(self):
        if not self._initialized:
            self.client = MongoClient(MONGO_URI)
            self._initialized = True

        return self.client


try:
    mongo_client = MongoClientManager().initialize_mongo()
except PyMongoError as e:
    logger.error(f"An error occurred: {CustomException(e,sys)}")

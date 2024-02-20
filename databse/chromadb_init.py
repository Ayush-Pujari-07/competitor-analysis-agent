import sys
import chromadb

from competitor_analysis_agent.logger import logger
from llm_manager.openai_manager import openai_manager
from competitor_analysis_agent.utils import generate_metadata
from competitor_analysis_agent.exception import CustomException


class ChromadbManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def initialize_chromnadb(self):
        if not self._initialized:
            self.client = chromadb.PersistentClient(path="./chroma")
            self._initialized = True

    def create_collection(self, metadata):
        self.embedding_collection = self.client.get_or_create_collection(
            name="openai_embading_test",
        )

        document, ids, metadatas, embeddings = generate_metadata(metadata)

        self.embedding_collection.add(
            documents=document,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings
        )

    def query_collection(self, query):
        result = self.embedding_collection.query(
            query_embeddings=openai_manager.client.embeddings.create(
                input=query,
                model="text-embedding-3-small"
            ),
            n_results=1
        )

        return result['documents'][0][0]


try:
    chromadb_client = ChromadbManager()
    chromadb_client.initialize_chromnadb()
except Exception as e:
    logger.error(f"An error occurred: {CustomException(e,sys)}")

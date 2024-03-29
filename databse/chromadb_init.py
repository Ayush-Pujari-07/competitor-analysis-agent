import sys
import chromadb

from uuid import uuid4
from langsmith import traceable
from langchain.callbacks.tracers import LangChainTracer

from competitor_analysis_agent.logger import logger
from llm_manager.openai_manager import openai_manager
from competitor_analysis_agent.utils import generate_metadata
from competitor_analysis_agent.exception import CustomException


tracer = LangChainTracer(project_name="Competative-Analysis-Agent")


class ChromadbManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    @traceable(name="Chromadb Manager Traceable")
    def initialize_chromnadb(self):
        if not self._initialized:
            self.client = chromadb.PersistentClient(path="./chroma")
            self._initialized = True

    @traceable(name="Chromadb Manager Traceable")
    async def create_collection(
        self,
        complete_data: list,
        user_id: str
    ):
        self.embedding_collection = self.client.get_or_create_collection(
            name=f"{user_id}_{uuid4().hex[:6]}",
        )

        document, ids, metadata, embeddings = await generate_metadata(complete_data)
        # logger.info(
        #     f"document: {document}, ids: {ids}, metadata: {metadata}, embeddings: {embeddings}")
        self.embedding_collection.add(
            documents=document,
            metadatas=metadata,
            ids=ids,
            embeddings=embeddings
        )

    @traceable(name="Chromadb Manager Traceable")
    async def query_collection(
        self,
        query: str
    ):
        embedding = await openai_manager.client.embeddings.create(
            input=query,
            model="text-embedding-3-small"
        )
        result = self.embedding_collection.query(
            query_embeddings=embedding.data[0].embedding,
            n_results=5
        )
        logger.info(f"Query: {query}, Result: {result}")
        return result['documents'][0][0]


try:
    chromadb_client = ChromadbManager()
    chromadb_client.initialize_chromnadb()
except Exception as e:
    logger.error(f"An error occurred: {CustomException(e,sys)}")

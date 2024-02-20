import gc
import sys
import tiktoken

from llm_manager.openai_manager import openai_manager
from competitor_analysis_agent.logger import logger
from competitor_analysis_agent.exception import CustomException


def token_count(string: str, encoding_name: str = "cl100k_base") -> int:
    """
    Returns the number of tokens in a text string.
    """
    try:
        encoding = tiktoken.get_encoding(encoding_name)
        return len(encoding.encode(string))
    except Exception as e:
        logger.error(f"An error occurred: {CustomException(e,sys)}")
    finally:
        garbage_collector()


def garbage_collector():
    gc.collect()


def generate_metadata(metadata):
    document = []
    ids = []
    metadatas = []
    embeddings = []
    for index, data in enumerate(metadata):
        embeddings.append(openai_manager.client.embeddings.create(
            input=data['content'],
            model="text-embedding-3-small"
        ).data[0].embedding)
        document.append(data['content'])
        ids.append(f"id{index+1}")
        metadatas.append({"source":data['title']})
    
    return document, ids, metadatas, embeddings
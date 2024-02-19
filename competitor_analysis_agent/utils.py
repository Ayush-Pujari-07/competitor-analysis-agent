import gc
import sys
import tiktoken

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

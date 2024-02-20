import gc
import re
import sys
import tiktoken
import requests

from nltk.corpus import stopwords

from llm_manager.openai_manager import openai_manager
from competitor_analysis_agent.logger import logger
from competitor_analysis_agent.exception import CustomException

from bs4 import BeautifulSoup
from langchain.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper

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


async def generate_metadata(complete_data: list):
    """
    Generate metadata for the given input metadata and return the document, ids, metadata, and embeddings.
    """
    try:
        document = []
        ids = []
        metadata = []
        embeddings = []
        for index, data in enumerate(complete_data):
            embedding = await openai_manager.client.embeddings.create(
                model="text-embedding-3-small",
                input=data['content']
            )
            embeddings.append(embedding.data[0].embedding)
            document.append(data['content'])
            ids.append(f"id{index+1}")
            metadata.append({"source":data['title']})
    
        return document, ids, metadata, embeddings
    
    except Exception as e:
        logger.error(f"An error occurred: {CustomException(e,sys)}")



RESULTS_PER_QUESTION = 5

# ddg_search = DuckDuckGoSearchAPIWrapper()

# async def web_search(query: str, num_results: int = RESULTS_PER_QUESTION):
#     """
#     Perform a web search using the specified query and return a list of links from the search results.
#     """
#     try:
#         results = await ddg_search.results(query, max_results=num_results)
#         return results
#     except Exception as e:
#         logger.error(f"An error occurred: {CustomException(e,sys)}")


def scrape_text(url: str):
    """
    A function to scrape text from a given URL.
    """
    try:
        response = requests.get(
            url=url
        )

        if response.status_code != 200:
            return f"Failed to retrive text from the website: {response.status_code}"

        soup = BeautifulSoup(response.text, 'html.parser')

        return soup.get_text(
            separator=" ",
            strip=True
        )
    except Exception as e:
        logger.error(f"An error occurred: {CustomException(e,sys)}")


def text_cleaner(text: str):
    """
    A function to clean the data by removing special characters and stop words.
    """
    try:
        # Remove special characters using regex
        cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text)

        # Remove stop words using nltk
        stop_words = set(stopwords.words('english'))
        words = cleaned_text.split()
        filtered_words = [word for word in words if word.lower() not in stop_words]

        # Join the filtered words to form cleaned text
        cleaned_text = ' '.join(filtered_words)

        return cleaned_text
    except Exception as e:
        logger.error(f"An error occurred: {CustomException(e,sys)}")

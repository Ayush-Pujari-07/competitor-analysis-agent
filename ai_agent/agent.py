import sys
import requests

from competitor_analysis_agent.logger import logger
from llm_manager.openai_manager import openai_manager
from competitor_analysis_agent.exception import CustomException

from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv

from langsmith import traceable
from langsmith.wrappers import wrap_openai
from langchain.callbacks.tracers import LangChainTracer
from langchain.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper

load_dotenv(find_dotenv())


tracer = LangChainTracer(project_name="Competative-Analysis-Agent")

RESULTS_PER_QUESTION = 3

ddg_search = DuckDuckGoSearchAPIWrapper()


def web_search(query: str, num_results: int = RESULTS_PER_QUESTION):
    """
    Perform a web search using the specified query and return a list of links from the search results.
    """
    try:
        results = ddg_search.run(query)
        return results
    except Exception as e:
        logger.error(f"An error occurred: {CustomException(e,sys)}")

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

        scrape_data = soup.get_text(
            separator=" ",
            strip=True
        )

        return scrape_data
    except Exception as e:
        logger.error(f"An error occurred: {CustomException(e,sys)}")

@traceable(name="Chat Pipeline Traceable")
def chat_pipeline(query: str):
    try:
        # we can also use scraper to get the data if not using duckduckgo wrapper and if we are willing to pass the link manually
        # context = "".join([scrape_text(url)[:3500] for url in data])
        context = web_search(query)
        
        # Prompt tempate
        template = f"As a researcher, your objective is to analyze the given Context below. Context: {context}\n"+"""
    Generate a comprehensive competitor analysis report, presenting insights into products and services. The report should include tables and graphs formatted in HTML, and the entire output should be enclosed within a JSON format with the following structure: 

    `{"response": "True", "report_data": "html report data"}`

    Example: If the question is unclear, respond with 'None'."""
        
        messages = [
            {"role": "system", "content": template},
            {"role": "user", "content": f"Question: {query}"}
        ]
        chat_completion = openai_manager.generate_text(messages)
        
        return chat_completion.choices[0].message.content
    except Exception as e:
        logger.error(f"An error occurred: {CustomException(e,sys)}")
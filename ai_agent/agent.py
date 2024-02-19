import os
import sys
import requests

# from competitor_analysis_agent.logger import logger
# from competitor_analysis_agent.exception import CustomException


from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks.tracers import LangChainTracer
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper

load_dotenv(find_dotenv())


tracer = LangChainTracer(project_name="Competative-Analysis-Agent")

RESULTS_PER_QUESTION = 3

ddg_search = DuckDuckGoSearchAPIWrapper()


def web_search(query: str, num_results: int):
    results = ddg_search.run(query)
    return [r['link'] for r in results]


def scrape_text(url: str):
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
        # logger.error(f"An error occurred: {CustomException(e,sys)}")
        print(e)


def agent_invoke(user_query: str, url):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a researcher and your task is to analyze the  above text, generate a detailed competatitor analysis report providing product and service insights along with tables and graphs in html format inside a json format. if the question is not clear, just respond with None"),
        ("user", "Question: {question}\nContext: {context}")
    ])

    page_content = scrape_text(url)[:10000]

    chain = prompt | ChatOpenAI(openai_api_key=os.environ.get(
        "OPENAI_API_KEY"), model_name="gpt-3.5-turbo-0125") | StrOutputParser()

    chain.invoke(
        {
            "question": user_query,
            "context": page_content,
        }
    )

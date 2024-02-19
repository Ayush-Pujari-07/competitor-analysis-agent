import os
import sys
import requests

# from competitor_analysis_agent.logger import logger
from competitor_analysis_agent.exception import CustomException
from llm_manager.openai_manager import openai_manager
from openai import OpenAI

from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv

from langsmith import traceable
from langsmith.wrappers import wrap_openai

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


def web_search(query: str, num_results: int = RESULTS_PER_QUESTION):
    """
    Perform a web search using the specified query and return a list of links from the search results.
    """
    results = ddg_search.run(query)
    print(results)
    return results


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
        # logger.error(f"An error occurred: {CustomException(e,sys)}")
        print(e)


# def agent_invoke(user_query: str, url):
#     """
#     This function takes in a user query and a URL, creates a chat prompt template, scrapes text content from the URL, and then invokes a chain of operations using the user query and the scraped page content.
#     """
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", "You are a researcher and your task is to analyze the  above text, generate a detailed competatitor analysis report providing product and service insights along with tables and graphs in html format inside a json format.\n example:. if the question is not clear, just respond with None"),
#         ("user", "Question: {question}\nContext: {context}")
#     ])

#     page_content = scrape_text(url)[:10000]

#     chain = prompt | ChatOpenAI(openai_api_key=os.environ.get(
#         "OPENAI_API_KEY"), model_name="gpt-3.5-turbo-0125") | StrOutputParser()

#     chain.invoke(
#         {
#             "question": user_query,
#             "context": page_content,
#         }
#     )

@traceable(name="Chat Pipeline Traceable")
def chat_pipeline(query: str):
    try:
        print(query)
        client = wrap_openai(openai_manager.initialize_openai())
        print("client: ",client)
        data = web_search(query)
        print("data",data)
        # context = "".join([scrape_text(url)[:3500] for url in data])
        context = data
        print("context",context)

        template = f"As a researcher, your objective is to analyze the given Context below. Context: {context}\n"+"""
    Generate a comprehensive competitor analysis report, presenting insights into products and services. The report should include tables and graphs formatted in HTML, and the entire output should be enclosed within a JSON format with the following structure: 

    `{"response": "True", "report_data": "html report data"}`

    Example: If the question is unclear, respond with 'None'."""
        # logger.info(f"The data template is: {template}")
        print("template: ",template)
        messages = [
            {"role": "system", "content": template},
            {"role": "user", "content": f"Question: {query}"}
        ]
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            response_format={"type": "json_object"},
            temperature=1.0,
            top_p=1
        )
        print(chat_completion.choices[0].message.content)
        return chat_completion.choices[0].message.content
    except Exception as e:
        # logger.error(f"An error occurred: {CustomException(e,sys)}")
        print(CustomException(e,sys))
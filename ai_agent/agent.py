import sys

from databse.chromadb_init import chromadb_client
from competitor_analysis_agent.logger import logger
from llm_manager.openai_manager import openai_manager
from competitor_analysis_agent.exception import CustomException
from competitor_analysis_agent.utils import scrape_text
from competitor_analysis_agent.google_search.google import GoogleSearch

from langsmith import traceable
from langchain.callbacks.tracers import LangChainTracer

tracer = LangChainTracer(project_name="Competative-Analysis-Agent")

@traceable(name="Chat Pipeline Traceable")
async def chat_pipeline(query: str, user_id: str):
    """
    A function that represents a chat pipeline. It takes a query as input and performs a series of operations to generate a chat completion. The function is asynchronous and returns the completed chat message.
    """
    try:
        # we can also use scraper to get the data if not using duckduckgo wrapper and if we are willing to pass the link manually.
        # ddg_search_output = web_search(query)
        search_output = GoogleSearch(query).search()
        print(search_output)
        logger.info(f"search output: {search_output}")
        complete_data = [{"title": result['title'], "content": scrape_text(result['link'])} for result in search_output]
        
        logger.info(f"Metadata: {complete_data}")

        await chromadb_client.create_collection(complete_data, user_id)
        context = await chromadb_client.query_collection(
            query=query
        )

        # Prompt tempate
        template = f"\"As a researcher, your mission is to conduct a thorough analysis of the provided context below:\n\nContext: {context}\n" + \
            "\nGenerate an extensive competitor analysis report for the company, delivering valuable insights into its products and services. Ensure that the report is visually appealing with well-crafted tables and graphs formatted in HTML. The entire output should be neatly encapsulated within a JSON format structured as follows: \n\n'{\"response\": \"True\", \"report_data\": \"html report data\"}'\n\nMake the report not only informative but also visually appealing. Example: If the question is unclear, respond with 'None'.\"\n"

        messages = [
            {"role": "system", "content": template},
            {"role": "user", "content": f"Provide me a detailed competitor analysis report for {query} in beautified HTML format.."}
        ]

        logger.info(f"Messages: {messages}")

        chat_completion = await openai_manager.generate_text(messages)
        logger.info(
            f"Chat completion: {chat_completion.choices[0].message.content}")
        return chat_completion.choices[0].message.content
    except Exception as e:
        logger.error(f"An error occurred: {CustomException(e,sys)}")

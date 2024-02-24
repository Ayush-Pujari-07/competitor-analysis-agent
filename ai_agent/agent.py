import sys

from databse.chromadb_init import chromadb_client
from competitor_analysis_agent.logger import logger
from llm_manager.openai_manager import openai_manager
from competitor_analysis_agent.exception import CustomException
from competitor_analysis_agent.utils import process_search_results, text_cleaner
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
        search_output = GoogleSearch(query+"competitors of top research firm reports").search()

        logger.info(f"search output: {search_output}")

        # data = [{"title": result['title'], "content": text_cleaner(result['content'])} for result in search_output]

        complete_data = process_search_results(search_output)

        # logger.info(f"complete data: {complete_data}")

        await chromadb_client.create_collection(complete_data, user_id)

        context = await chromadb_client.query_collection(
            query=query
        )

        # Prompt template
        # template = f"\"As a researcher, your mission is to conduct a thorough analysis of the provided context below:\n\nContext: {context}\n" + \
        # "\nGenerate an extensive competitor analysis report for the company, delivering valuable insights into its products and services. Ensure that the report is visually appealing with well-crafted tables and detail pointers for strategy building. The report should be formatted in HTML. The entire output should be neatly encapsulated within a JSON format structured as follows: \n\n'{\"response\": \"True/False\", \"report_data\": \"html report/None\"}'\n\nMake the report not only informative but also visually appealing."

        # Strategic questions
        strategic_question_template = f"Context informaition is below\nContext: {context}\n" + f"Given the context information and not prior knowledge. Generate only Questions based on the context.\n\nYou are a Research Analyst/ strategist a professional who prepares investigative reports on securities or assets for in-house or client use. Your task is to generate questions for an upcoming presentation on strategy building.\n\nRestrict your question generation based on the context information provided.\n"
        strategic_question_message = [
            {"role": "system", "content": strategic_question_template},
            {"role": "user", "content": f"Provide me a 10 detailed strategic question for above context."}
        ]
        query_questions = await openai_manager.generate_text(strategic_question_message)

        # Final report genearation.
        template = f"Context informaition is below\nContext: {context}\n" + f"Given the context information and not prior knowledge. Generate only answers based on the below query\n\nYou are a Research Analyst/ strategist a professional who prepares investigative reports on securities or assets for in-house or client use. Your task is to answer questions for an upcoming presentation on strategy building. MOreover, your task is to present a detailed report with insights in proper format.\n\nRestrict your answer based on the context information provided. If you dont know the answer then you can apply your prior knowledge and generate a detailed report.\n" + f"query: {query_questions}\n"

        messages = [
            {"role": "system", "content": template},
            {"role": "user", "content": f"Provide me a detailed strategic/competitor analysis report."}
        ]

        logger.info(f"Messages: {messages}")

        chat_completion = await openai_manager.generate_text(messages)
        logger.info(
            f"Chat completion: {chat_completion.choices[0].message.content}")
        return chat_completion.choices[0].message.content
    except Exception as e:
        logger.error(f"An error occurred: {CustomException(e,sys)}")

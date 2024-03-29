import os
import sys

from xhtml2pdf import pisa
from pydantic import BaseModel
from datetime import datetime
from fastapi.templating import Jinja2Templates
from fastapi import requests, FastAPI, responses, Depends, Form

from ai_agent.agent import chat_pipeline
from databse.mongo_init import mongo_client
from competitor_analysis_agent.constants import API_KEY
from competitor_analysis_agent.logger import logger
from competitor_analysis_agent.auth import authenticate_JWT
from competitor_analysis_agent.exception import CustomException

app = FastAPI(
    title="Competitive Analysis Agent",
    description="An agent for creating competitive analysis reports"
)

# used langsmith for creating traces and used this values in .env
# export LANGCHAIN_TRACING_V2=true
# export LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
# export LANGCHAIN_API_KEY="YOUR_LANGCHAIN_API_KEY"

templates = Jinja2Templates(directory="templates")


class ResearchInput(BaseModel):
    query: str
    user_id: str

class OpenAIResponse(BaseModel):
    response: str
    report_data: str

@app.get("/", response_class=responses.HTMLResponse)
async def root(request: requests.Request):
    # return responses.JSONResponse(content={"message": "Hello World"})
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/openai", response_class=responses.HTMLResponse)
# async def openai(data: ResearchInput, request: requests.Request, user: str = Depends(authenticate_JWT)):
async def openai(query: str, user_id: str, request: requests.Request, user: str = Depends(authenticate_JWT)):
    """
    A description of the entire function, its parameters, and its return types.
    """
    try:
        # Create a top-level run
        response = await chat_pipeline(query, user_id)
        logger.info(f"Response: {response}")
        if eval(response)['response'] is None:
            # return responses.JSONResponse(content={"message": "None"})
            return templates.TemplateResponse("result.html", {"request": request, "response": {"message": "None"}})

        # Create a directory
        if not os.path.exists('report'):
            os.mkdir('report')
        directory = os.path.join(os.getcwd(), 'report')
        output_filename = os.path.join(directory, f'{query}_{user_id}.pdf')
        mongo_client['reports']['reports_files'].insert_one(
            {'created_at': datetime.now().utcnow(), 'user_id': user_id, 'user_query': query, 'data': eval(response)['report_data']})

        # Save as PDF
        with open(output_filename, "wb") as out_file:
            pisa.CreatePDF(eval(response)['report_data'], dest=out_file)
        
        response_json = eval(response)
        result_data = OpenAIResponse(**response_json)

        # return responses.JSONResponse(content={"message": f"Report pdf created at {output_filename}"})
        return templates.TemplateResponse("result.html", {"request": request, "result_data": result_data})


    except Exception as e:
        logger.error(f"An error occurred: {CustomException(e,sys)}")
        error_message = f"An error occurred: {str(e)}"
        return templates.TemplateResponse("result.html", {"request": request, "error_message": error_message})

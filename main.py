import os

from xhtml2pdf import pisa
from pydantic import BaseModel
from fastapi import requests, FastAPI, responses

# from databse.mongo_init import mongo_client
from ai_agent.agent import chat_pipeline

app = FastAPI()


class ResearchInput(BaseModel):
    query: str
    user_id: str


@app.get("/")
async def root():
    return responses.JSONResponse(content={"message": "Hello World"})



@app.get("/openai")
def openai(data: ResearchInput, request: requests.Request):
    # Create a top-level run
    response = chat_pipeline(data.query)
    if eval(response)['response'] is None:
        return responses.JSONResponse(content={"message": "None"})
    
    os.mkdir('report')
    directory = os.path.join(os.getcwd(), 'report')
    output_filename = os.path.join(directory, 'report.pdf')

    # Create a sub-level run
    with open(output_filename, "wb") as out_file:
        pisa.CreatePDF(eval(response)['report_data'], dest=out_file)

    return responses.JSONResponse(content={"message": f"Report pdf created at {output_filename}"})
    
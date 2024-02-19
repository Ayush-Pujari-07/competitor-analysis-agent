import os

from xhtml2pdf import pisa
from pydantic import BaseModel
from fastapi import requests, FastAPI, responses, Depends

from ai_agent.agent import chat_pipeline
from competitor_analysis_agent.auth import authenticate_JWT

app = FastAPI(
    title="Competitive Analysis Agent",
    description="An agent for creating competitive analysis reports"
)

# used langsmith for creating traces and used this values in .env
# export LANGCHAIN_TRACING_V2=true
# export LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
# export LANGCHAIN_API_KEY="YOUR_LANGCHAIN_API_KEY"

class ResearchInput(BaseModel):
    query: str
    user_id: str


@app.get("/")
async def root():
    return responses.JSONResponse(content={"message": "Hello World"})

@app.get("/openai")
def openai(data: ResearchInput, request: requests.Request, user: str=Depends(authenticate_JWT)):
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
    
# question = "Can you summarize this morning's meetings?"

# # This can be retrieved in a retrieval step
# context = "During this morning's meeting, we solved all world conflict."

# messages = [
#     { "role": "system", "content": "You are a helpful assistant. Please respond to the user's request only based on the given context." },
#     { "role": "user", "content": f"Question: {question}\nContext: {context}"}
# ]

# # Create a child run
# child_llm_run = pipeline.create_child(
#     name="OpenAI Call",
#     run_type="llm",
#     inputs={"messages": messages},
# )

# # Generate a completion

# chat_completion = openai_manager.generate_text(messages=messages)

# # End the runs and log them
# child_llm_run.end(outputs=chat_completion)
# child_llm_run.post()

# pipeline.end(outputs={"answer": chat_completion.choices[0].message.content})
# pipeline.post()

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


# @app.get("/mongo")
# def mongo():
#     return responses.JSONResponse(content={"message": f"{mongo_client.client}"})


@app.get("/openai")
def openai(data: ResearchInput, request: requests.Request):
    # Create a top-level run
    response = chat_pipeline(data.query)

    return responses.JSONResponse(content={"message": f'{response}'})

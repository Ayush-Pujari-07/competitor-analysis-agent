# # To run the example below, ensure the environment variable OPENAI_API_KEY is set
# import os

# from llm_manager.openai_manager import openai_manager
# from langsmith.run_trees import RunTree

# ### OPTION 1: Use RunTree API (more explicit) ###
# # This can be a user input to your app
# question = "Can you summarize this morning's meetings?"

# # Create a top-level run
# pipeline = RunTree(
#     name="Chat Pipeline Run Tree",
#     run_type="chain",
#     inputs={"question": question}
# )

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

from fastapi import requests, FastAPI, responses
# from databse.mongo_init import mongo_client
from llm_manager.openai_manager import openai_manager


app = FastAPI()


@app.get("/")
async def root():
    return responses.JSONResponse(content={"message": "Hello World"})


# @app.get("/mongo")
# def mongo():
#     return responses.JSONResponse(content={"message": mongo_client})


@app.get("/openai")
def openai():
    return responses.JSONResponse(content={"message": openai_manager})

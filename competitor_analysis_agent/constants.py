import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


GPT_MODEL = os.environ.get("GPT_MODEL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MONGO_URI = os.environ.get("MONGO_URI")

secreats = os.environ.get("SECRET_KEY")
PAYLOAD = os.environ.get("PAYLOAD")

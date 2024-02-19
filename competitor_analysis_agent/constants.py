import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# Import Models
GPT_MODEL = os.environ.get("GPT_MODEL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Import DB url
MONGO_URI = os.environ.get("MONGO_URI")

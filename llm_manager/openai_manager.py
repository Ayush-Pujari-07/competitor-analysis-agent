import os
import sys

from openai import OpenAI

from competitor_analysis_agent.logger import logger
from competitor_analysis_agent.constants import OPENAI_API_KEY, GPT_MODEL
from competitor_analysis_agent.exception import CustomException


class OpenAIManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def initialize_openai(self):
        """
        Initialize OpenAI API key and model.
        """
        if not self._initialized:
            self.client = OpenAI(
                api_key=OPENAI_API_KEY,
                max_retries=3
            )
            self._initialized = True
    
    def generate_text(self, messages):
        if not self._initialized:
            raise CustomException(
                "OpenAI API key not initialized. Please initialize OpenAI API key using the `initialize_openai` method."
            )

        return self.client.chat.completions.create(
            model=GPT_MODEL,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=1.0,
            top_p=1
        )


try:
    openai_manager = OpenAIManager()
    openai_manager.initialize_openai()
except Exception as e:
    logger.error(f"An error occurred: {CustomException(e,sys)}")

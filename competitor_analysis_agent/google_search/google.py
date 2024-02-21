import os
import os
import json
import requests

from competitor_analysis_agent.logger import logger
from competitor_analysis_agent.utils import scrape_text

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

class GoogleSearch:

    def __init__(self, query) -> None:
        self.query = query
        self.api_key = self.get_api_key()
        self.cx_key = self.get_cx_key()

    def get_api_key(self):
        """Get the Google API key from the environment variables."""
        try:
            return os.environ.get("GOOGLE_API_KEY")
        except:
            raise Exception("Google API key not found. Set the GOOGLE_API_KEY environment variable."
                            "You can get your API key from https://developers.google.com/custom-search/v1/introduction")

    def get_cx_key(self):
        """Get the Google CX key from the environment variables."""
        try:
            return os.environ.get("GOOGLE_CX_KEY")
        except:
            raise Exception("Google CX key not found. Set the GOOGLE_CX_KEY environment variable."
                            "You can get your CX key from https://developers.google.com/custom-search/v1/introduction")

    def search(self, max_retries: int=7)-> list:
        """
        A function to search using the Google Custom Search API.

        Args:
            max_retries (int): The maximum number of retries for the search.

        Returns:
            list: A list of search results containing title, link, and snippet.
        """
        logger.info(f"Searched Query; {self.query}")
        URL = f"https://www.googleapis.com/customsearch/v1?key={self.api_key}&cx={self.cx_key}&q={self.query}"
        response = requests.get(URL)

        if response is None:
            return None

        try:
            search_results = json.loads(response.text)
        except Exception as e:
            logger.error(e)
            return None

        results = search_results.get("items", [])
        search_results = []

        # Normalizing search result for matching the format for other API's
        for result in results:
            # skip youtube links
            if "youtube.com" in result["link"]:
                continue
            search_results.append({
                "title": result["title"],
                "link": result["link"],
                "content": scrape_text(result["link"])
            })
        logger.info(f"search: {search_results}")
        
        return search_results
import os
import requests
from typing import List
from loguru import logger
from app.schemas.search_schemas import SearchResult

class GoogleSearchService:
    BASE_URL = "https://www.googleapis.com/customsearch/v1"
    
    def __init__(self):
        logger.info("Initializing GoogleSearchService")
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
        
        if not self.api_key or not self.search_engine_id:
            error_msg = "Google API key and Search Engine ID must be set in environment variables"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        logger.debug("GoogleSearchService initialized with API key and search engine ID")
    
    async def search_company(self, company_name: str, num_results: int = 5) -> List[SearchResult]:
        """
        Search for a company and return top results
        
        Args:
            company_name: Name of the company to search for
            num_results: Number of search results to return (default: 5)
            
        Returns:
            List[SearchResult]: List of search results
            
        Raises:
            Exception: If there's an error performing the search
        """
        logger.info(f"Initiating company search for: {company_name}")
        logger.debug(f"Search parameters - num_results: {num_results}")
        
        try:
            search_query = f"official website of {company_name}"
            logger.debug(f"Constructed search query: '{search_query}'")
            
            params = {
                'q': search_query,
                'key': self.api_key,
                'cx': self.search_engine_id,
                'num': num_results
            }
            
            logger.debug(f"Sending request to Google Custom Search API")
            response = requests.get(self.BASE_URL, params=params)
            logger.debug(f"Received response with status code: {response.status_code}")
            
            response.raise_for_status()
            
            results = response.json().get('items', [])
            logger.info(f"Successfully retrieved {len(results)} search results")
            
            search_results = [
                SearchResult(
                    title=item.get('title', ''),
                    link=item.get('link', ''),
                    snippet=item.get('snippet', '')
                )
                for item in results
            ]
            
            logger.debug(f"Processed {len(search_results)} search results")
            return search_results
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error performing Google search: {str(e)}"
            logger.error(f"{error_msg}. Response: {getattr(e.response, 'text', 'No response')}")
            raise Exception(error_msg) from e
            
        except Exception as e:
            error_msg = f"Unexpected error during company search: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise Exception(error_msg) from e

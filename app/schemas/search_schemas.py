from pydantic import BaseModel, Field
from typing import List, Optional

class CompanyRequest(BaseModel):
    company_name: str = Field(..., description="Name of the company to search for")
    num_results: int = Field(5, description="Number of search results to return", ge=1, le=10)

class SearchResult(BaseModel):
    title: str = Field(..., description="Title of the search result")
    link: str = Field(..., description="URL of the search result")
    snippet: str = Field(..., description="Brief description of the search result")

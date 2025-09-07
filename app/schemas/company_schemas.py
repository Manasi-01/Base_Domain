from pydantic import BaseModel, Field

class CompanyRequest(BaseModel):
    company_name: str = Field(..., description="Name of the company to search for")

class CompanySearchResponse(BaseModel):
    company_name: str = Field(..., description="Name of the company that was searched")
    search_url: str = Field(..., description="Google search URL for the company")
    status: str = Field("success", description="Status of the search operation")

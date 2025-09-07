from fastapi import APIRouter, HTTPException
import urllib.parse
from app.schemas.company_schemas import CompanyRequest, CompanySearchResponse

router = APIRouter(
    prefix="/api/v1",
    tags=["company"],
    responses={404: {"description": "Not found"}},
)


@router.get("/health")
async def health_check():
    return {"status": "healthy"}

@router.post("/search", response_model=CompanySearchResponse)
async def search_company(company: CompanyRequest) -> CompanySearchResponse:
    try:
        # Format the company name for URL
        formatted_name = urllib.parse.quote_plus(f"official website of {company.company_name}")
        search_url = f"https://www.google.com/search?q={formatted_name}"
        
        return CompanySearchResponse(
            company_name=company.company_name,
            search_url=search_url
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

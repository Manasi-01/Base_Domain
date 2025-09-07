from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.services.google_search import GoogleSearchService
from app.schemas.search_schemas import CompanyRequest, SearchResult

router = APIRouter(
    prefix="/api/v1/google",
    tags=["google-search"],
    responses={404: {"description": "Not found"}},
)


@router.post("/search", response_model=List[SearchResult])
async def google_search_company(request: CompanyRequest) -> List[SearchResult]:
    """
    Search for a company using Google Custom Search API and return top results
    """
    try:
        search_service = GoogleSearchService()
        results = await search_service.search_company(
            company_name=request.company_name,
            num_results=request.num_results
        )
        return results
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing search: {str(e)}")

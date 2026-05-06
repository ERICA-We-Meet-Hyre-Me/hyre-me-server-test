from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel
from app.api.services.company import get_random_company

router = APIRouter()


class CompanyRequest(BaseModel):
    name: str


@router.post("/company")
def company_endpoint(request: CompanyRequest) -> dict:
    """랜덤한 기업명을 반환하는 엔드포인트"""
    company = get_random_company()
    message = f"{request.name}님의 최적의 기업은 {company} 입니다"
    return {
        "status": "success",
        "message": message,
        "name": request.name,
        "company": company,
    }

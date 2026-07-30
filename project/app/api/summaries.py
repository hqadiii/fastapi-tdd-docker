from fastapi import APIRouter, HTTPException
from typing import List
from app.models.pydantic import SummaryResponseSchema, SummaryPayloadSchema
from app.api import crud
from app.models.tortoise import SummarySchema

router = APIRouter()


@router.post("/", response_model=SummaryResponseSchema, status_code=201)
async def create_summary(payload: SummaryPayloadSchema) -> SummaryResponseSchema:
    id = await crud.post(payload)
    return {"id": id, "url": payload.url}


@router.get("/{id}/", response_model=SummarySchema)
async def get_summary(id: int) -> SummarySchema:
    summary = await crud.get(id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary


@router.get("/", response_model=List[SummarySchema])
async def get_all_summaries() -> List[SummarySchema]:
    return await crud.get_all()

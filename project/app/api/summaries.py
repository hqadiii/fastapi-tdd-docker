from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.api import crud
from app.models.tortoise import SummarySchema

from app.models.pydantic import (  # isort:skip
    SummaryPayloadSchema,
    SummaryResponseSchema,
    SummaryUpdatePayloadSchema,
)

router = APIRouter()


@router.post("/", response_model=SummaryResponseSchema, status_code=201)
async def create_summary(payload: SummaryPayloadSchema) -> SummaryResponseSchema:
    id = await crud.post(payload)
    return {"id": id, "url": payload.url}


@router.get("/{id}/", response_model=SummarySchema)
async def get_summary(id: int = Path(..., gt=0)) -> SummarySchema:
    summary = await crud.get(id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary


@router.get("/", response_model=List[SummarySchema])
async def get_all_summaries() -> List[SummarySchema]:
    return await crud.get_all()


@router.delete("/{id}/", status_code=204)
async def delete_summary(id: int = Path(..., gt=0)):
    deleted = await crud.delete(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Summary not found")


@router.put("/{id}/", response_model=SummarySchema)
async def update_summary(
    payload: SummaryUpdatePayloadSchema, id: int = Path(..., gt=0)
) -> SummarySchema:
    summary = await crud.put(id, payload)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary

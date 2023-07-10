from typing import List

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi_auth0 import Auth0User

from app.api import crud
from app.auth import auth
from app.models.pydantic import SummaryPayloadSchema, SummaryResponseSchema
from app.models.tortoise import SummarySchema

router = APIRouter()


@router.post("/", response_model=SummaryResponseSchema, status_code=201, dependencies=[Depends(auth.implicit_scheme)])
async def create_summary(payload: SummaryPayloadSchema, user: Auth0User = Security(auth.get_user, scopes=["write:diary"])) -> SummaryResponseSchema:
    summary_id = await crud.post(payload)

    response_object = {"id": summary_id, "url": payload.url}
    return response_object


@router.get("/{id}/", response_model=SummarySchema, dependencies=[Depends(auth.implicit_scheme)])
async def read_summary(id: int, user: Auth0User = Security(auth.get_user, scopes=["read:diary"])) -> SummarySchema:
    summary = await crud.get(id)
    if not summary:
        raise HTTPException(status_code=404, detail=f"Summary {id} not found")

    return summary


@router.get("/", response_model=List[SummarySchema], dependencies=[Depends(auth.implicit_scheme)])
async def read_all_summaries(user: Auth0User = Security(auth.get_user, scopes=["read:diary"])) -> List[SummarySchema]:
    print(user.json())
    return await crud.get_all()


@router.delete("/{id}/", response_model=SummaryResponseSchema, dependencies=[Depends(auth.implicit_scheme)])
async def delete_summary(id: int, user: Auth0User = Security(auth.get_user, scopes=["write:diary"])) -> SummaryResponseSchema:
    summary = await crud.get(id)
    if not summary:
        raise HTTPException(status_code=404, detail=f"Summary {id} not found")
    await crud.delete(id)

    return summary

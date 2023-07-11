from typing import List

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi_auth0 import Auth0User

from app.crud import spot_crud
from app.auth import auth

from app.models.spot import CreateSpotSchema, UpdateSpotSchema
from app.models.tortoise import SpotSchema

router = APIRouter()


@router.post("/", response_model=SpotSchema, status_code=201, dependencies=[Depends(auth.implicit_scheme)])
async def create_spot(payload: CreateSpotSchema, user: Auth0User = Security(auth.get_user, scopes=["write:diary"])) -> SpotSchema:
    spot = await spot_crud.post(payload, user)
    response_object = spot
    return response_object


@router.get("/{id}/", response_model=SpotSchema, dependencies=[Depends(auth.implicit_scheme)])
async def read_spot(id: int, user: Auth0User = Security(auth.get_user, scopes=["read:diary"])) -> SpotSchema:
    spot = await spot_crud.get(id)
    if not spot:
        raise HTTPException(status_code=404, detail=f"Spot {id} not found")

    return spot


@router.get("/", response_model=List[SpotSchema], dependencies=[Depends(auth.implicit_scheme)])
async def read_all_spots(user: Auth0User = Security(auth.get_user, scopes=["read:diary"])) -> List[SpotSchema]:
    return await spot_crud.get_all()


@router.put("/{id}/", response_model=SpotSchema, dependencies=[Depends(auth.implicit_scheme)])
async def update_spot(id: int, payload: UpdateSpotSchema, user: Auth0User = Security(auth.get_user, scopes=["write:diary"])) -> SpotSchema:
    updated_spot = await spot_crud.put(id, payload)
    if updated_spot:
        return updated_spot
    raise HTTPException(status_code=404, detail=f"Spot {id} not found")


@router.delete("/{id}/", response_model=SpotSchema, dependencies=[Depends(auth.implicit_scheme)])
async def delete_spot(id: int, user: Auth0User = Security(auth.get_user, scopes=["write:diary"])) -> SpotSchema:
    spot = await spot_crud.get(id)
    if not spot:
        raise HTTPException(status_code=404, detail=f"Spot {id} not found")
    await spot_crud.delete(id)

    return spot


@router.delete("/", dependencies=[Depends(auth.implicit_scheme)])
async def delete_all_spots(user: Auth0User = Security(auth.get_user, scopes=["write:diary"])):
    await spot_crud.delete_all()

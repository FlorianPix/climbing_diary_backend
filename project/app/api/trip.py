from typing import List

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi_auth0 import Auth0User

from app.api import trip_crud
from app.auth import auth

from app.models.trip import TripSchema, CreateTripSchema, UpdateTripSchema

router = APIRouter()


@router.post("/", response_model=TripSchema, status_code=201, dependencies=[Depends(auth.implicit_scheme)])
async def create_trip(payload: CreateTripSchema, user: Auth0User = Security(auth.get_user, scopes=["write:diary"])) -> TripSchema:
    trip = await trip_crud.post(payload, user)

    response_object = trip
    return response_object


@router.get("/{id}/", response_model=TripSchema, dependencies=[Depends(auth.implicit_scheme)])
async def read_trip(id: int, user: Auth0User = Security(auth.get_user, scopes=["read:diary"])) -> TripSchema:
    trip = await trip_crud.get(id)
    if not trip:
        raise HTTPException(status_code=404, detail=f"Trip {id} not found")

    return trip


@router.get("/", response_model=List[TripSchema], dependencies=[Depends(auth.implicit_scheme)])
async def read_all_trips(user: Auth0User = Security(auth.get_user, scopes=["read:diary"])) -> List[TripSchema]:
    return await trip_crud.get_all()


@router.put("/{id}/", response_model=TripSchema, dependencies=[Depends(auth.implicit_scheme)])
async def update_trip(id: int, payload: UpdateTripSchema, user: Auth0User = Security(auth.get_user, scopes=["write:diary"])) -> TripSchema:
    updated_trip = await trip_crud.put(id, payload)
    if updated_trip:
        return updated_trip
    raise HTTPException(status_code=404, detail=f"Trip {id} not found")


@router.delete("/{id}/", response_model=TripSchema, dependencies=[Depends(auth.implicit_scheme)])
async def delete_trip(id: int, user: Auth0User = Security(auth.get_user, scopes=["write:diary"])) -> TripSchema:
    trip = await trip_crud.get(id)
    if not trip:
        raise HTTPException(status_code=404, detail=f"Trip {id} not found")
    await trip_crud.delete(id)
    return trip


@router.delete("/", dependencies=[Depends(auth.implicit_scheme)])
async def delete_all_trips(user: Auth0User = Security(auth.get_user, scopes=["write:diary"])):
    await trip_crud.delete_all()

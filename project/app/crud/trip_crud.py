from typing import List, Optional, Union

from app.models.trip import CreateTripSchema, UpdateTripSchema
from app.models.tortoise import Trip, TripSchema
from fastapi_auth0 import Auth0User


async def post(payload: CreateTripSchema, user: Auth0User) -> int:
    trip = Trip(
        user_id=user.id,
        comment=payload.comment,
        end_date=payload.end_date,
        name=payload.name,
        rating=payload.rating,
        start_date=payload.start_date,
    )
    await trip.save()
    return trip


async def get(id: int) -> Optional[dict]:
    trip = await Trip.filter(id=id).first().values()
    if trip:
        return trip
    return None


async def get_all() -> List:
    trips = await Trip.all().values()
    return trips


async def put(id: int, payload: UpdateTripSchema) -> Union[dict, None]:
    trip_dict = {k: v for k, v in payload.dict().items() if v is not None}
    if len(trip_dict) >= 1:
        await Trip.filter(id=id).update(**trip_dict)
    if (existing_trip := await Trip.filter(id=id).first().values()) is not None:
        return existing_trip
    return None


async def delete(id: int) -> int:
    trip = await Trip.filter(id=id).first().delete()
    return trip


async def delete_all():
    await Trip.filter().delete()

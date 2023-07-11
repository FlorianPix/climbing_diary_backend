from typing import List, Optional, Union

from app.models.spot import CreateSpotSchema, UpdateSpotSchema
from app.models.tortoise import Spot, SpotSchema
from fastapi_auth0 import Auth0User


async def post(payload: CreateSpotSchema, user: Auth0User) -> int:
    spot = Spot(
        media_ids=[],
        single_pitch_route_ids=[],
        multi_pitch_route_ids=[],
        user_id=user.id,
        comment=payload.comment,
        coordinates=payload.coordinates,
        distance_parking=payload.distance_parking,
        distance_public=payload.distance_public,
        location=payload.location,
        name=payload.name,
        rating=payload.rating,
    )
    await spot.save()
    return spot


async def get(id: int) -> Optional[dict]:
    spot = await Spot.filter(id=id).first().values()
    if spot:
        return spot
    return None


async def get_all() -> List:
    spots = await Spot.all().values()
    return spots


async def put(id: int, payload: UpdateSpotSchema) -> Union[dict, None]:
    spot_dict = {k: v for k, v in payload.dict().items() if v is not None}
    if len(spot_dict) >= 1:
        await Spot.filter(id=id).update(**spot_dict)
    if (existing_spot := await Spot.filter(id=id).first().values()) is not None:
        return existing_spot
    return None


async def delete(id: int) -> int:
    spot = await Spot.filter(id=id).first().delete()
    return spot


async def delete_all():
    await Spot.filter().delete()

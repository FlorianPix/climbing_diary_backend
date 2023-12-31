from typing import Optional

from pydantic import BaseModel
from pydantic.fields import Field


class CreateSpotSchema(BaseModel):
    comment: Optional[str]
    lat: Optional[float]
    long: Optional[float]
    distance_parking: Optional[int]
    distance_public: Optional[int]
    location: str = Field(...)
    name: str = Field(...)
    rating: int = Field(..., ge=0, le=5)

    class Config:
        schema_extra = {
            "example": {
                "comment": "Great spot close to a lake with solid holds but kinda hard to reach.",
                "lat": 50.746036,
                "long": 10.642666,
                "distance_parking": 120,
                "distance_public": 120,
                "location": "Deutschland, Thüringen, Thüringer Wald",
                "name": "Falkenstein",
                "rating": 5,
            }
        }


class UpdateSpotSchema(BaseModel):
    media_ids: Optional[tuple]
    single_pitch_route_ids: Optional[tuple]
    multi_pitch_route_ids: Optional[tuple]
    comment: Optional[str]
    lat: Optional[float]
    long: Optional[float]
    distance_parking: Optional[int]
    distance_public: Optional[int]
    location: Optional[str]
    name: Optional[str]
    rating: Optional[int]

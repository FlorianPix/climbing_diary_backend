from datetime import date
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel
from pydantic.fields import Field


class CreateTripSchema(BaseModel):
    comment: Optional[str]
    end_date: date
    name: str = Field(...)
    rating: int = Field(..., ge=0, le=5)
    start_date: date

    class Config:
        schema_extra = {
            "example": {
                "comment": "Great trip",
                "end_date": "2022-10-08",
                "name": "Ausflug zum Falkenstein",
                "start_date": "2022-10-06",
                "rating": 5,
            }
        }


class UpdateTripSchema(BaseModel):
    media_ids: Optional[tuple]
    spot_ids: Optional[tuple]
    comment: Optional[str]
    end_date: Optional[str]
    name: Optional[str]
    rating: Optional[int]
    start_date: Optional[str]

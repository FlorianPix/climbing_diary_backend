from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Trip(models.Model):
    media_ids = fields.JSONField()
    spot_ids = fields.JSONField()
    user_id = fields.TextField()

    comment = fields.TextField()
    end_date = fields.DateField()
    name = fields.TextField()
    rating = fields.IntField()
    start_date = fields.DateField()

    def __str__(self):
        return self.name


TripSchema = pydantic_model_creator(Trip)

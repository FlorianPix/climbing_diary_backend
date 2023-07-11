from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Trip(models.Model):
    user_id = fields.TextField()

    comment = fields.TextField()
    end_date = fields.DateField()
    name = fields.TextField()
    rating = fields.IntField()
    start_date = fields.DateField()

    def __str__(self):
        return self.name


TripSchema = pydantic_model_creator(Trip)


class TripMedia(models.Model):
    trip: fields.ForeignKeyRelation[Trip] = fields.ForeignKeyField(
        "models.Trip",
        related_name="media",
        on_delete=fields.CASCADE
    )
    media_id = fields.IntField()


class Spot(models.Model):
    user_id = fields.TextField()
    trip: fields.ForeignKeyRelation[Trip] = fields.ForeignKeyField(
        "models.Trip",
        related_name="spots",
        on_delete=fields.CASCADE
    )

    comment = fields.TextField()
    lat = fields.FloatField()
    long = fields.FloatField()
    distance_parking = fields.IntField()
    distance_public = fields.IntField()
    location = fields.TextField()
    name = fields.TextField()
    rating = fields.IntField()

    def __str__(self):
        return self.name


SpotSchema = pydantic_model_creator(Spot)


class SpotMedia(models.Model):
    spot: fields.ForeignKeyRelation[Spot] = fields.ForeignKeyField(
        "models.Spot",
        related_name="media",
        on_delete=fields.CASCADE
    )
    media_id = fields.IntField()


class SinglePitchRoute(models.Model):
    spot: fields.ForeignKeyRelation[Spot] = fields.ForeignKeyField(
        "models.Spot",
        related_name="single_pitch_route",
        on_delete=fields.CASCADE
    )
    single_pitch_route_id = fields.IntField()


class MultiPitchRoute(models.Model):
    spot: fields.ForeignKeyRelation[Spot] = fields.ForeignKeyField(
        "models.Spot",
        related_name="multi_pitch_route",
        on_delete=fields.CASCADE
    )
    multi_pitch_route_id = fields.IntField()

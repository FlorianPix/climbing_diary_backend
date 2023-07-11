import json
from fastapi import Security
from fastapi_auth0 import Auth0User
from app.auth import auth


test_spot = {
    "media_ids": [],
    "single_pitch_route_ids": [],
    "multi_pitch_route_ids": [],
    "comment": "Great spot",
    "coordinates": [50.746036, 10.642666],
    "distance_parking": 120,
    "distance_public": 120,
    "location": "Deutschland, Thüringen, Thüringer Wald",
    "name": "Falkenstein",
    "rating": 5,
}


def test_create_spot(test_app_with_db, headers):
    response = test_app_with_db.post(
        "/spot/",
        data=json.dumps(test_spot),
        headers=headers
    )

    assert response.status_code == 201
    response_dict = response.json()
    del response_dict['id']
    del response_dict['user_id']
    assert response_dict == test_spot


def test_create_spot_invalid_json(test_app, headers):
    response = test_app.post("/spot/", data=json.dumps({}), headers=headers)
    assert response.status_code == 422
    assert response.json() == {
        'detail': [
            {
                'loc': ['body', 'location'],
                'msg': 'field required',
                'type': 'value_error.missing'
            },
            {
                'loc': ['body', 'name'],
                'msg': 'field required',
                'type': 'value_error.missing'
            },
            {
                'loc': ['body', 'rating'],
                'msg': 'field required',
                'type': 'value_error.missing'
            }
        ]
    }


def test_read_spot(test_app_with_db, headers):
    response = test_app_with_db.post(
        "/spot/",
        data=json.dumps(test_spot),
        headers=headers
    )
    spot_id = response.json()["id"]

    response = test_app_with_db.get(f"/spot/{spot_id}/", headers=headers)
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict['id'] == spot_id
    del response_dict['id']
    del response_dict['user_id']
    assert response_dict == test_spot


def test_read_spot_incorrect_id(test_app_with_db, headers):
    id = 999
    response = test_app_with_db.get(f"/spot/{id}/", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == f"Spot {id} not found"


def test_read_all_spots(test_app_with_db, headers):
    response = test_app_with_db.post(
        "/spot/",
        data=json.dumps(test_spot),
        headers=headers
    )
    spot_id = response.json()["id"]

    response = test_app_with_db.get("/spot/", headers=headers)
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == spot_id, response_list))) == 1


def test_update_spot(test_app_with_db, headers):
    response = test_app_with_db.post(
        "/spot/",
        data=json.dumps(test_spot),
        headers=headers
    )
    spot_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/spot/{spot_id}/",
        data=json.dumps({
            "media_ids": [],
            "single_pitch_route_ids": [],
            "multi_pitch_route_ids": [],
            "comment": "Great spot",
            "coordinates": [50.746036, 10.642666],
            "distance_parking": 120,
            "distance_public": 120,
            "location": "Deutschland, Thüringen, Thüringer Wald",
            "name": "Falkenstein updated",
            "rating": 5,
        }),
        headers=headers,
    )
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == spot_id
    assert response_dict["name"] == "Falkenstein updated"


def test_update_spot_incorrect_id(test_app_with_db, headers):
    id = 999
    response = test_app_with_db.put(
        f"/spot/{id}/",
        data=json.dumps(test_spot),
        headers=headers,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == f"Spot {id} not found"


def test_update_spot_empty_json(test_app_with_db, headers):
    response = test_app_with_db.post(
        "/spot/",
        data=json.dumps(test_spot),
        headers=headers,
    )
    spot_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/spot/{spot_id}/",
        data=json.dumps({}),
        headers=headers
    )
    assert response.status_code == 200
    response_dict = response.json()
    del response_dict['id']
    del response_dict['user_id']
    assert response_dict == test_spot


def test_update_spot_invalid_keys(test_app_with_db, headers):
    response = test_app_with_db.post(
        "/spot/",
        data=json.dumps(test_spot),
        headers=headers
    )
    spot_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/spot/{spot_id}/",
        data=json.dumps({"invalid_key": "foo"}),
        headers=headers
    )
    assert response.status_code == 200
    response_dict = response.json()
    del response_dict['id']
    del response_dict['user_id']
    assert response_dict == test_spot
    assert "invalid_key" not in response_dict.keys()


def test_delete_spot(test_app_with_db, headers):
    response = test_app_with_db.post(
        "/spot/",
        data=json.dumps(test_spot),
        headers=headers
    )
    spot_id = response.json()["id"]

    response = test_app_with_db.delete(
        f"/spot/{spot_id}/", headers=headers
    )
    assert response.status_code == 200
    response_dict = response.json()
    del response_dict['id']
    del response_dict['user_id']
    assert response_dict == test_spot


def test_remove_spot_incorrect_id(test_app_with_db, headers):
    id = 999
    response = test_app_with_db.delete(f"/spot/{id}/", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == f"Spot {id} not found"

import json
from fastapi import Security
from fastapi_auth0 import Auth0User
from app.auth import auth


def test_create_trip(test_app_with_db, headers):
    response = test_app_with_db.post(
        "/trip/",
        data=json.dumps({
            "media_ids": [],
            "spot_ids": [],
            "comment": "Great trip",
            "end_date": "2022-10-08",
            "name": "Ausflug zum Falkenstein",
            "start_date": "2022-10-06",
            "rating": 5,
        }),
        headers=headers
    )

    assert response.status_code == 201
    response_dict = response.json()
    assert response_dict["media_ids"] == []
    assert response_dict["spot_ids"] == []
    assert response_dict["comment"] == "Great trip"
    assert response_dict["end_date"] == "2022-10-08"
    assert response_dict["name"] == "Ausflug zum Falkenstein"
    assert response_dict["start_date"] == "2022-10-06"
    assert response_dict["rating"] == 5


def test_create_trip_invalid_json(test_app, headers):
    response = test_app.post("/trip/", data=json.dumps({}), headers=headers)
    assert response.status_code == 422
    assert response.json() == {
        'detail': [
            {
                'loc': ['body', 'end_date'],
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
            },
            {
                'loc': ['body', 'start_date'],
                'msg': 'field required',
                'type': 'value_error.missing'
            }
        ]
    }


def test_read_trip(test_app_with_db, headers):
    response = test_app_with_db.post(
        "/trip/",
        data=json.dumps({
            "media_ids": [],
            "spot_ids": [],
            "comment": "Great trip",
            "end_date": "2022-10-08",
            "name": "Ausflug zum Falkenstein",
            "start_date": "2022-10-06",
            "rating": 5,
        }),
        headers=headers
    )
    trip_id = response.json()["id"]

    response = test_app_with_db.get(f"/trip/{trip_id}/", headers=headers)
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == trip_id
    assert response_dict["media_ids"] == []
    assert response_dict["spot_ids"] == []
    assert response_dict["comment"] == "Great trip"
    assert response_dict["end_date"] == "2022-10-08"
    assert response_dict["name"] == "Ausflug zum Falkenstein"
    assert response_dict["start_date"] == "2022-10-06"
    assert response_dict["rating"] == 5


def test_read_trip_incorrect_id(test_app_with_db, headers):
    id = 999
    response = test_app_with_db.get(f"/trip/{id}/", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == f"Trip {id} not found"


def test_read_all_trips(test_app_with_db, headers):
    response = test_app_with_db.post(
        "/trip/",
        data=json.dumps({
            "media_ids": [],
            "spot_ids": [],
            "comment": "Great trip",
            "end_date": "2022-10-08",
            "name": "Ausflug zum Falkenstein",
            "start_date": "2022-10-06",
            "rating": 5,
        }),
        headers=headers
    )
    trip_id = response.json()["id"]

    response = test_app_with_db.get("/trip/", headers=headers)
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == trip_id, response_list))) == 1


def test_update_trip(test_app_with_db, headers):
    response = test_app_with_db.post(
        "/trip/",
        data=json.dumps({
            "media_ids": [],
            "spot_ids": [],
            "comment": "Great trip",
            "end_date": "2022-10-08",
            "name": "Ausflug zum Falkenstein",
            "start_date": "2022-10-06",
            "rating": 5,
        }),
        headers=headers
    )
    trip_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/trip/{trip_id}/",
        data=json.dumps({
            "media_ids": [],
            "spot_ids": [],
            "comment": "Great trip",
            "end_date": "2022-10-08",
            "name": "Ausflug zum Falkenstein updated",
            "start_date": "2022-10-06",
            "rating": 5,
        }),
        headers=headers,
    )
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == trip_id
    assert response_dict["name"] == "Ausflug zum Falkenstein updated"


def test_update_trip_incorrect_id(test_app_with_db, headers):
    id = 999
    response = test_app_with_db.put(
        f"/trip/{id}/",
        data=json.dumps({
            "media_ids": [],
            "spot_ids": [],
            "comment": "Great trip",
            "end_date": "2022-10-08",
            "name": "Ausflug zum Falkenstein updated",
            "start_date": "2022-10-06",
            "rating": 5,
        }),
        headers=headers,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == f"Trip {id} not found"


def test_update_trip_empty_json(test_app_with_db, headers):
    response = test_app_with_db.post(
        "/trip/",
        data=json.dumps({
            "media_ids": [],
            "spot_ids": [],
            "comment": "Great trip",
            "end_date": "2022-10-08",
            "name": "Ausflug zum Falkenstein",
            "start_date": "2022-10-06",
            "rating": 5,
        }),
        headers=headers,
    )
    trip_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/trip/{trip_id}/",
        data=json.dumps({}),
        headers=headers
    )
    assert response.status_code == 200
    response_dict = response.json()
    assert response_dict["id"] == trip_id
    assert response_dict["media_ids"] == []
    assert response_dict["spot_ids"] == []
    assert response_dict["comment"] == "Great trip"
    assert response_dict["end_date"] == "2022-10-08"
    assert response_dict["name"] == "Ausflug zum Falkenstein"
    assert response_dict["start_date"] == "2022-10-06"
    assert response_dict["rating"] == 5


def test_update_trip_invalid_keys(test_app_with_db, headers):
    response = test_app_with_db.post(
        "/trip/",
        data=json.dumps({
            "media_ids": [],
            "spot_ids": [],
            "comment": "Great trip",
            "end_date": "2022-10-08",
            "name": "Ausflug zum Falkenstein",
            "start_date": "2022-10-06",
            "rating": 5,
        }),
        headers=headers
    )
    trip_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/trip/{trip_id}/",
        data=json.dumps({"invalid_key": "foo"}),
        headers=headers
    )
    assert response.status_code == 200
    response_dict = response.json()
    assert response_dict["id"] == trip_id
    assert response_dict["media_ids"] == []
    assert response_dict["spot_ids"] == []
    assert response_dict["comment"] == "Great trip"
    assert response_dict["end_date"] == "2022-10-08"
    assert response_dict["name"] == "Ausflug zum Falkenstein"
    assert response_dict["start_date"] == "2022-10-06"
    assert response_dict["rating"] == 5
    assert "invalid_key" not in response_dict.keys()


def test_delete_trip(test_app_with_db, headers):
    response = test_app_with_db.post(
        "/trip/",
        data=json.dumps({
            "media_ids": [],
            "spot_ids": [],
            "comment": "Great trip",
            "end_date": "2022-10-08",
            "name": "Ausflug zum Falkenstein",
            "start_date": "2022-10-06",
            "rating": 5,
        }),
        headers=headers
    )
    trip_id = response.json()["id"]

    response = test_app_with_db.delete(
        f"/trip/{trip_id}/", headers=headers
    )
    assert response.status_code == 200
    response_dict = response.json()
    assert response_dict["id"] == trip_id
    assert response_dict["media_ids"] == []
    assert response_dict["spot_ids"] == []
    assert response_dict["comment"] == "Great trip"
    assert response_dict["end_date"] == "2022-10-08"
    assert response_dict["name"] == "Ausflug zum Falkenstein"
    assert response_dict["start_date"] == "2022-10-06"
    assert response_dict["rating"] == 5


def test_remove_trip_incorrect_id(test_app_with_db, headers):
    id = 999
    response = test_app_with_db.delete(f"/trip/{id}/", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == f"Trip {id} not found"

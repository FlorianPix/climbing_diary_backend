import json


def test_create_summary(test_app_with_db, headers):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"}), headers=headers
    )

    assert response.status_code == 201
    assert response.json()["url"] == "https://foo.bar"


def test_create_summaries_invalid_json(test_app, headers):
    response = test_app.post("/summaries/", data=json.dumps({}), headers=headers)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "url"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_read_summary(test_app_with_db, headers):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"}), headers=headers
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.get(f"/summaries/{summary_id}/", headers=headers)
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["summary"]
    assert response_dict["created_at"]


def test_read_summary_incorrect_id(test_app_with_db, headers):
    id = 999
    response = test_app_with_db.get(f"/summaries/{id}/", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == f"Summary {id} not found"


def test_read_all_summaries(test_app_with_db, headers):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"}), headers=headers
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.get("/summaries/", headers=headers)
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == summary_id, response_list))) == 1


def test_delete_summary(test_app_with_db, headers):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"}), headers=headers
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.delete(
        f"/summaries/{summary_id}/", headers=headers
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": summary_id,
        "url": "https://foo.bar"
    }


def test_remove_summary_incorrect_id(test_app_with_db, headers):
    id = 999
    response = test_app_with_db.delete(f"/summaries/{id}/", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == f"Summary {id} not found"

def test_no_token(test_app_with_db):
    # Given
    # test_app_with_db

    # When any request is sent without a bearer token
    response = test_app_with_db.get("/summaries/")

    # Then a 403 Forbidden HTTPError should be the response with the "missing bearer token" detail
    assert response.status_code == 403
    assert response.json()["detail"] == "Missing bearer token"

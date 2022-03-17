from fastapi.testclient import TestClient
from arnold.api.api_v1.endpoints.sample import router
from fastapi import status

client = TestClient(router)


def test_post_valid_sample(fast_app_client, valid_load_sample):
    # GIVEN valid sample request data
    # WHEN running the user request with the data
    response = fast_app_client.post("/api/v1/sample/", json=valid_load_sample.dict())

    # THEN assert status is ok
    assert response.status_code == status.HTTP_200_OK


def test_post_invalid_sample(fast_app_client, invalid_load_sample):
    # GIVEN invalid sample request data

    # WHEN running the user request with the data
    response = fast_app_client.post("/api/v1/sample/", json=invalid_load_sample)

    # THEN assert status 422
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_post_sample_already_in_db(mocker, fast_app_client, valid_load_sample):
    # GIVEN that the sample to load is already in the database. Ie, find_sample is True
    mocker.patch("arnold.crud.read.find_sample", return_value=True)

    # WHEN running the sample request with data
    response = fast_app_client.post("/api/v1/sample/", json=valid_load_sample.dict())

    # THEN assert status is 405
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert "Sample already in database" in str(response.content)


def test_post_sample_create_sample_failing(mocker, fast_app_client, valid_load_sample):
    # GIVEN that the sample is not in the database but the create_sample fails
    mocker.patch("arnold.crud.read.find_sample", return_value=False)
    mocker.patch("arnold.crud.create.create_sample", side_effect=Exception("mocked error"))

    # WHEN running the sample request with data
    response = fast_app_client.post("/api/v1/sample/", json=valid_load_sample.dict())

    # THEN assert status is 405
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert "mocked error" in str(response.content)


def test_post_valid_samples(fast_app_client, valid_load_samples):
    # GIVEN a list of valid samples as request data
    # WHEN running the user request with the data
    response = fast_app_client.post("/api/v1/samples/", json=valid_load_samples)

    # THEN assert status is ok
    assert response.status_code == status.HTTP_200_OK


def test_post_invalid_samples(fast_app_client, invalid_load_samples):
    # GIVEN  a list of invalid samples as request data
    # WHEN running the user request with the data
    response = fast_app_client.post("/api/v1/samples/", json=invalid_load_samples)

    # THEN assert status 422
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_post_sample_create_samples_failing(mocker, fast_app_client, valid_load_samples):
    # GIVEN that the create_samples fails
    mocker.patch("arnold.crud.create.create_samples", side_effect=Exception("mocked error"))

    # WHEN running the samples request with data
    response = fast_app_client.post("/api/v1/samples/", json=valid_load_samples)

    # THEN assert status is 405
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert "mocked error" in str(response.content)

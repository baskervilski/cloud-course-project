import tempfile
from typing import (
    Generator,
    List,
)

import pytest
from fastapi import Response
from fastapi.testclient import TestClient

from files_api.main import APP
from files_api.s3.read_objects import fetch_s3_objects_metadata
from files_api.s3.write_objects import upload_s3_object
from tests.consts import TEST_OBJECT_CONTENT


# Fixture for FastAPI test client
@pytest.fixture
def client(mocked_aws) -> TestClient:  # pylint: disable=unused-argument
    with TestClient(APP) as client:
        yield client


@pytest.fixture(scope="function")
def tmp_test_file() -> Generator:  # pylint: disable=unused-argument
    with tempfile.NamedTemporaryFile() as tmp_file:
        tmp_file.write(TEST_OBJECT_CONTENT.encode("utf-8"))
        yield tmp_file


@pytest.fixture(scope="function")
def test_files_on_test_bucket(mock_bucket) -> List[str]:  # pylint: disable=unused-argument
    test_file_keys = [f"test_file_{i}.txt" for i in range(1, 6)]

    for file_key in test_file_keys:
        upload_s3_object(
            bucket_name=mock_bucket,
            object_key=file_key,
            file_content=TEST_OBJECT_CONTENT.encode("utf8"),
            content_type="text/plain",
        )

    obj_meta, _ = fetch_s3_objects_metadata(bucket_name=mock_bucket, max_keys=10)
    assert len(obj_meta) == len(test_file_keys)

    return test_file_keys


def test_upload_file(client: TestClient, tmp_test_file, mock_bucket):
    response = client.put(f"/files/{tmp_test_file.name!s}", files={"file": tmp_test_file})

    assert response.status_code == 201, response.text


def test_list_files_with_pagination(client: TestClient, test_files_on_test_bucket):
    response = client.get(f"/files", params={"max_keys": 2 * len(test_files_on_test_bucket)}).json()
    assert len(response["objects"]) == len(test_files_on_test_bucket)
    assert {o["Key"] for o in response["objects"]} == set(test_files_on_test_bucket)

    response = client.get(f"/files", params={"max_keys": 2}).json()
    assert len(response["objects"]) == 2
    response = client.get(
        f"/files", params={"max_keys": 5, "continuation_token": response["continuation_token"]}
    ).json()
    assert len(response["objects"]) == 3


def test_get_file_metadata(client: TestClient):
    ...


def test_get_file(client: TestClient, mock_bucket, tmp_test_file):
    upload_response = client.put(f"/files/{tmp_test_file.name}", files={"file": tmp_test_file})
    assert upload_response.status_code == 201, upload_response.text

    bucket_objects, token = fetch_s3_objects_metadata(mock_bucket)
    bucket_keys = [obj["Key"] for obj in bucket_objects]
    assert tmp_test_file.name in bucket_keys, bucket_keys

    response: Response = client.get(f"/files/{tmp_test_file.name}")
    file_content = response.json()  # .decode("utf-8"))
    assert file_content == TEST_OBJECT_CONTENT


def test_delete_file(client: TestClient):
    ...

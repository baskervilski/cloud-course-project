"""Test cases for `s3.read_objects`."""

import pytest
from mypy_boto3_s3 import S3Client

from files_api.s3.delete_objects import delete_s3_object
from files_api.s3.read_objects import (
    fetch_s3_object,
    fetch_s3_objects_metadata,
    fetch_s3_objects_using_page_token,
)
from files_api.s3.write_objects import upload_s3_object
from tests.consts import (
    TEST_BUCKET_NAME,
    TEST_OBJECT_CONTENT,
    TEST_OBJECT_KEY,
)


@pytest.fixture()
def test_object(s3_client):
    """Dummy object for testing."""
    upload_s3_object(
        bucket_name=TEST_BUCKET_NAME,
        object_key=TEST_OBJECT_KEY,
        content_type="text/plain",
        file_content=TEST_OBJECT_CONTENT.encode("utf8"),
        s3_client=s3_client,
    )
    yield TEST_OBJECT_KEY

    delete_s3_object(s3_client=s3_client, bucket_name=TEST_BUCKET_NAME, object_key=TEST_OBJECT_KEY)


def test_object_exists_in_s3(test_object, s3_client: S3Client):
    """Test object exists."""
    from files_api.s3.read_objects import object_exists_in_s3

    assert object_exists_in_s3(bucket_name=TEST_BUCKET_NAME, object_key=test_object, s3_client=s3_client)
    assert (
        object_exists_in_s3(bucket_name=TEST_BUCKET_NAME, object_key="this-key-doesn't exist", s3_client=s3_client)
        is False
    )


def test_pagination(s3_client: S3Client):  # noqa: R701
    """Test pagination exists."""
    for i in range(1, 6):
        s3_client.put_object(Bucket=TEST_BUCKET_NAME, Key=f"file{i}.txt", Body=f"content {i}")

    # Paginate 2 at a time
    files, next_page_token = fetch_s3_objects_metadata(TEST_BUCKET_NAME, max_keys=2)
    assert len(files) == 2
    assert files[0]["Key"] == "file1.txt"
    assert files[1]["Key"] == "file2.txt"

    files, next_page_token = fetch_s3_objects_using_page_token(TEST_BUCKET_NAME, next_page_token, max_keys=2)
    assert len(files) == 2
    assert files[0]["Key"] == "file3.txt"
    assert files[1]["Key"] == "file4.txt"

    files, next_page_token = fetch_s3_objects_using_page_token(TEST_BUCKET_NAME, next_page_token, max_keys=2)
    assert len(files) == 1
    assert files[0]["Key"] == "file5.txt"
    assert next_page_token is None


# pylint: disable=unused-argument
def test_mixed_page_sizes(s3_client):  # noqa: R701 - too complex
    """Assert that pagination works correctly for pages of differing sizes."""
    # Upload 5 objects
    for i in range(1, 6):
        s3_client.put_object(Bucket=TEST_BUCKET_NAME, Key=f"file{i}.txt", Body=f"content {i}")

    # Paginate with mixed page sizes
    files, next_page_token = fetch_s3_objects_metadata(TEST_BUCKET_NAME, max_keys=3)
    assert len(files) == 3
    assert files[0]["Key"] == "file1.txt"
    assert files[1]["Key"] == "file2.txt"
    assert files[2]["Key"] == "file3.txt"

    files, next_page_token = fetch_s3_objects_using_page_token(TEST_BUCKET_NAME, next_page_token, max_keys=1)
    assert len(files) == 1
    assert files[0]["Key"] == "file4.txt"

    files, next_page_token = fetch_s3_objects_using_page_token(TEST_BUCKET_NAME, next_page_token, max_keys=2)
    assert len(files) == 1
    assert files[0]["Key"] == "file5.txt"
    assert next_page_token is None


def test_directory_queries(s3_client):  # noqa: R701 - too complex
    """Assert that queries with prefixes work correctly with various directory prefixes on object keys."""
    # Upload nested objects
    s3_client.put_object(Bucket=TEST_BUCKET_NAME, Key="folder1/file1.txt", Body="content 1")
    s3_client.put_object(Bucket=TEST_BUCKET_NAME, Key="folder1/file2.txt", Body="content 2")
    s3_client.put_object(Bucket=TEST_BUCKET_NAME, Key="folder2/file3.txt", Body="content 3")
    s3_client.put_object(Bucket=TEST_BUCKET_NAME, Key="folder2/subfolder1/file4.txt", Body="content 4")
    s3_client.put_object(Bucket=TEST_BUCKET_NAME, Key="file5.txt", Body="content 5")

    # Query with prefix
    files, next_page_token = fetch_s3_objects_metadata(TEST_BUCKET_NAME, prefix="folder1/")
    assert len(files) == 2
    assert files[0]["Key"] == "folder1/file1.txt"
    assert files[1]["Key"] == "folder1/file2.txt"
    assert next_page_token is None

    # Query with prefix for nested folder
    files, next_page_token = fetch_s3_objects_metadata(TEST_BUCKET_NAME, prefix="folder2/subfolder1/")
    assert len(files) == 1
    assert files[0]["Key"] == "folder2/subfolder1/file4.txt"
    assert next_page_token is None

    # Query with no prefix
    files, next_page_token = fetch_s3_objects_metadata(TEST_BUCKET_NAME)
    assert len(files) == 5
    assert files[0]["Key"] == "file5.txt"
    assert files[1]["Key"] == "folder1/file1.txt"
    assert files[2]["Key"] == "folder1/file2.txt"
    assert files[3]["Key"] == "folder2/file3.txt"
    assert files[4]["Key"] == "folder2/subfolder1/file4.txt"
    assert next_page_token is None


def test_fetch_s3_object(test_object, s3_client: S3Client):
    """TODO."""
    content = fetch_s3_object(TEST_BUCKET_NAME, test_object, s3_client=s3_client)
    decoded_obj = content.decode("utf8")
    assert TEST_OBJECT_CONTENT == decoded_obj


def test_fetch_s3_objects_metadata(test_object):
    """TODO."""
    metas, next_token = fetch_s3_objects_metadata(TEST_BUCKET_NAME)

    from mypy_boto3_s3.type_defs import ObjectTypeDef

    assert [ObjectTypeDef(meta) for meta in metas]
    assert [meta for meta in metas if meta["Key"] == test_object]

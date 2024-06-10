"""Example pytest fixture."""

import boto3
import pytest
from moto import mock_aws
from mypy_boto3_s3 import S3Client

from tests.consts import DEFAULT_REGION

# @pytest.fixture(scope="session")
# def test_session_id() -> str:
#     """Demonstrate how pytest fixtures are used."""
#     test_session_id = str(PROJECT_DIR.name) + str(uuid4())[:6]
#     return test_session_id


@pytest.fixture()
def test_bucket_name():
    """TODO."""
    return "test-bucket"


@pytest.fixture(scope="session")
def s3_client(test_bucket_name: str):
    """TODO."""
    with mock_aws():
        client: S3Client = boto3.client("s3")

        client.create_bucket(Bucket=test_bucket_name, CreateBucketConfiguration={"LocationConstraint": DEFAULT_REGION})

        yield client

        client.delete_bucket(test_bucket_name)

"""Example pytest fixture."""

import os
from typing import Generator

import pytest
from moto import mock_aws

from files_api.config import BUCKET_NAME
from files_api.s3.bucket_ops import (
    create_bucket,
    delete_bucket,
)
from tests.consts import DEFAULT_REGION

# @pytest.fixture(scope="session")
# def test_session_id() -> str:
#     """Demonstrate how pytest fixtures are used."""
#     test_session_id = str(PROJECT_DIR.name) + str(uuid4())[:6]
#     return test_session_id


def point_away_from_aws():
    """Ensure we don't test on actual AWS."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(scope="function")
def mocked_aws() -> Generator[None, None, None]:
    """
    Set up a mocked AWS environment for testing and clean up after the test.
    """
    with mock_aws():
        # Set the environment variables to point away from AWS
        point_away_from_aws()

        # # 1. Create an S3 bucket
        # s3_client = boto3.client("s3")
        # s3_client.create_bucket(Bucket=BUCKET_NAME)

        yield

        # # 4. Clean up/Teardown by deleting the bucket
        # response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        # for obj in response.get("Contents", []):
        #     s3_client.delete_object(Bucket=BUCKET_NAME, Key=obj["Key"])

        # s3_client.delete_bucket(Bucket=BUCKET_NAME)


@pytest.fixture(scope="function")
def mock_bucket(mocked_aws) -> Generator:
    """Create a test bucket for each test function."""
    create_bucket(BUCKET_NAME, DEFAULT_REGION)
    yield BUCKET_NAME
    delete_bucket(BUCKET_NAME)

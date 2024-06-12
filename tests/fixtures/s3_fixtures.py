"""Example pytest fixture."""

import os

import boto3
import pytest
from moto import mock_aws
from mypy_boto3_s3 import S3Client

from files_api.s3.bucket_ops import (
    create_bucket,
    delete_bucket,
)
from tests.consts import (
    DEFAULT_REGION,
    TEST_BUCKET_NAME,
)

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


@pytest.fixture()
def s3_client():
    """TODO."""
    with mock_aws():
        point_away_from_aws()
        client: S3Client = boto3.client("s3")

        create_bucket(bucket_name=TEST_BUCKET_NAME, region=DEFAULT_REGION, s3_client=client)

        yield client

        delete_bucket(bucket_name=TEST_BUCKET_NAME, s3_client=client)

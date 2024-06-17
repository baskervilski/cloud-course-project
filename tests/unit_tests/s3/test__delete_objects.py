"""Test cases for `s3.delete_objects`."""

import boto3


def test_delete_existing_s3_object(mocked_aws):
    """TODO."""
    boto3.client("s3")


def test_delete_nonexistent_s3_object(mocked_aws):
    """TODO."""
    boto3.client("s3")

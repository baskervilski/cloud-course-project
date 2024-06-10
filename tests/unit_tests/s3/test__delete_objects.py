"""Test cases for `s3.delete_objects`."""

from mypy_boto3_s3 import S3Client


def test_delete_existing_s3_object(s3_client: S3Client):
    """TODO."""


def test_delete_nonexistent_s3_object(s3_client: S3Client):
    """TODO."""

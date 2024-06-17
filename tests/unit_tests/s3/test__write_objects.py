"""Test cases for `s3.write_objects`."""

import boto3


def test_upload_s3_object(mocked_aws):
    """TODO."""
    boto3.client("s3")

import boto3

from files_api.s3.bucket_ops import (
    create_bucket,
    delete_bucket,
)
from files_api.s3.write_objects import upload_s3_object


def test_create_and_delete_bucket(mocked_aws):
    """Selfexplanatory."""

    s3_client = boto3.client("s3")
    tmp_bucket_name = "tmp-bucket-123"

    # Verify that the bucket doesn't exist at first
    buckets = s3_client.list_buckets()["Buckets"]
    assert [] == [bucket for bucket in buckets if bucket["Name"] == tmp_bucket_name]

    # Create the bucket
    create_bucket(s3_client=s3_client, bucket_name=tmp_bucket_name, region="eu-central-1")
    upload_s3_object(
        s3_client=s3_client,
        content_type="text/plain",
        bucket_name=tmp_bucket_name,
        object_key="dummy_file.txt",
        file_content="dummy".encode("utf8"),
    )

    buckets = s3_client.list_buckets()["Buckets"]
    assert [tmp_bucket_name] == [bucket["Name"] for bucket in buckets if bucket["Name"] == tmp_bucket_name]
    create_bucket(s3_client=s3_client, bucket_name=tmp_bucket_name, region="eu-central-1")

    # Cleanup and validation
    delete_bucket(bucket_name=tmp_bucket_name, s3_client=s3_client)
    buckets = s3_client.list_buckets()["Buckets"]
    assert [] == [bucket for bucket in buckets if bucket["Name"] == tmp_bucket_name]

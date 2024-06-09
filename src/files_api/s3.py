"""Module to interact with AWS S3."""

from typing import Optional

import boto3

from files_api.config import (
    AWS_REGION,
    BUCKET_NAME,
)

try:
    from mypy_boto3_s3.type_defs import CreateBucketOutputTypeDef
except ImportError:
    print("boto3-stubs[s3] not installed")


S3_CLIENT = boto3.client("s3")


def create_bucket(bucket_name: str) -> Optional["CreateBucketOutputTypeDef"]:
    """
    Create an S3 bucket.

    :param bucket_name: Name of the bucket to create
    :type bucket_name: str
    """
    try:
        response = S3_CLIENT.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": AWS_REGION},  # type: ignore
        )
        print(f"Bucket '{bucket_name}' created successfully.")
        return response
    except S3_CLIENT.exceptions.BucketAlreadyOwnedByYou:
        print(f"Bucket '{bucket_name}' already exists and you own it.")
    return None


# Create a bucket
create_bucket(bucket_name=BUCKET_NAME)

response = S3_CLIENT.put_object(Bucket=BUCKET_NAME, Key="folder/test.txt", Body="Hello, World!")

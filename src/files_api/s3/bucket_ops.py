"""Module to interact with AWS S3."""

from typing import (
    List,
    Optional,
)

import boto3
from mypy_boto3_s3 import S3Client

try:
    from mypy_boto3_s3.type_defs import (
        CreateBucketOutputTypeDef,
        EmptyResponseMetadataTypeDef,
    )
except ImportError:
    print("boto3-stubs[s3] not installed")


def create_bucket(
    bucket_name: str, region: str, s3_client: Optional["S3Client"] = None
) -> Optional["CreateBucketOutputTypeDef"]:
    """
    Create an S3 bucket.

    :param bucket_name: Name of the bucket to create
    :param region: Bucket region
    :param s3_client: [optional] S3Client, otherwise a default one will be initialized
    """
    s3_client = s3_client or boto3.client("s3")

    try:
        response = s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": region},  # type: ignore
        )
        print(f"Bucket '{bucket_name}' created successfully.")
        return response
    except s3_client.exceptions.BucketAlreadyOwnedByYou:
        print(f"Bucket '{bucket_name}' already exists and you own it.")
    return None


def list_bucket_objects_client_api(bucket_name: str, s3_client: Optional[S3Client] = None) -> List[str]:
    """
    List all objects in an S3 bucket using the client API.

    :param bucket_name: Name of the bucket to list objects from
    """
    s3_client = s3_client or boto3.client("s3")

    response = s3_client.list_objects_v2(Bucket=bucket_name)
    return [obj["Key"] for obj in response.get("Contents", [])]


def delete_bucket(bucket_name: str, s3_client: Optional[S3Client] = None) -> Optional["EmptyResponseMetadataTypeDef"]:
    """
    Delete an S3 bucket, including all its objects.

    If the bucket does not exist, no error is raised.

    :param bucket_name: Name of the bucket to delete
    :return: Response from the delete_bucket call or None if there is no bucket.
    """
    s3_client = s3_client or boto3.client("s3")

    for key in list_bucket_objects_client_api(bucket_name=bucket_name):
        s3_client.delete_object(Bucket=bucket_name, Key=key)

    s3_client.delete_bucket(Bucket=bucket_name)

    return None

# pragma: no-cover
"""All configuration goes here."""

import os

BUCKET_NAME = "cloud-course-bucket-nemo"
DEFAULT_REGION = "eu-central-1"
DEFAULT_PROFILE = "py-cloud-user"

# Set the profile and region for the AWS SDK (boto3) to use
AWS_PROFILE = os.environ.get("AWS_PROFILE", DEFAULT_PROFILE)
os.environ["AWS_PROFILE"] = AWS_PROFILE

AWS_REGION = os.environ.get("AWS_REGION", DEFAULT_REGION)
os.environ["AWS_REGION"] = AWS_REGION

# pragma: no-cover
"""All configuration goes here."""

import os
from pathlib import Path

THIS_DIR = Path(__file__).parent

BUCKET_NAME = "some-bucket"
# BUCKET_NAME = "cloud-course-bucket-nemo"
DEFAULT_REGION = "eu-central-1"
DEFAULT_PROFILE = "py-cloud-user"

DATA_DIR = Path(os.getenv("DATA_DIR", str(THIS_DIR / "data")))
DATA_DIR.mkdir(exist_ok=True)

# Set the profile and region for the AWS SDK (boto3) to use
AWS_PROFILE = os.environ.get("AWS_PROFILE", DEFAULT_PROFILE)
os.environ["AWS_PROFILE"] = AWS_PROFILE

AWS_REGION = os.environ.get("AWS_REGION", DEFAULT_REGION)
os.environ["AWS_REGION"] = AWS_REGION

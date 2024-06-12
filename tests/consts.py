"""Constant values used for tests."""

from pathlib import Path

THIS_DIR = Path(__file__).parent
PROJECT_DIR = (THIS_DIR / "../").resolve()

DEFAULT_REGION = "eu-central-1"
TEST_BUCKET_NAME = "test-bucket"
TEST_OBJECT_KEY = "dummy_object.txt"
TEST_OBJECT_CONTENT = ""

import os
import shutil

import boto3
import pytest
from fixtures import SimpleFixtureModel
from transformers import AutoModel
from utils import delete_bucket_contents
from pathlib import Path

from savingface import save_face

save_face()

S3_BUCKET_NAME = "my-model-backup-bucket"
MODEL_KEY = "your_model_directory/model.safetensors"


@pytest.fixture(scope="session")
def cache_dir(tmp_path_factory):
    """Create a persistent cache directory for the session and ensure its cleanup."""
    base_temp = tmp_path_factory.getbasetemp()
    cache_dir_path = Path(base_temp) / "model_cache"
    cache_dir_path.mkdir(exist_ok=True)

    yield cache_dir_path  # Use the directory during the tests

    # Cleanup code after yielding
    shutil.rmtree(cache_dir_path, ignore_errors=True)


@pytest.fixture(scope="module", autouse=True)
def s3_bucket():
    """Create and delete the bucket before and after every test."""
    s3_client = boto3.client(
        "s3",
        endpoint_url=os.environ.get("S3_ENDPOINT_URL", "http://localhost:4566"),
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1",
    )

    # Create the bucket
    s3_client.create_bucket(Bucket=S3_BUCKET_NAME)

    yield s3_client  # Provide the client to the test functions if needed

    # After the tests run, delete the bucket and its contents
    delete_bucket_contents(S3_BUCKET_NAME, s3_client)
    s3_client.delete_bucket(Bucket=S3_BUCKET_NAME)


@pytest.fixture(scope="function")
def ensure_model_in_s3(s3_bucket, tmp_path):
    """
    Ensure the model is available in S3 before each test.
    """
    # Create and save a dummy model
    config = {"num_channels": 3, "hidden_size": 32, "num_classes": 10}
    model = SimpleFixtureModel(config=config)
    model_path = tmp_path / "my-awesome-model"
    model.save_pretrained(str(model_path), config=config)

    # Assuming the model file is saved as "pytorch_model.bin" in the directory
    model_file = model_path / "model.safetensors"
    s3_bucket.upload_file(
        Filename=str(model_file), Bucket=S3_BUCKET_NAME, Key=MODEL_KEY
    )
    yield  # This allows the test to run after setup
    # Cleanup: The tmp_path and its contents are automatically cleaned up by pytest


def test_from_pretrained_fallback_to_s3(ensure_model_in_s3, cache_dir):
    """
    Test `from_pretrained` fallback mechanism when Hugging Face Hub is unreachable.
    """
    # Simulate failure by providing an invalid model identifier
    invalid_model_identifier = "some_nonexistent_model"

    # The patched `from_pretrained` should now attempt to fallback to S3
    try:
        result = AutoModel.from_pretrained(invalid_model_identifier, cache_dir=cache_dir)
        assert (
            result is not None
        ), "Failed to fallback to S3 when Hugging Face Hub is unreachable"
    except Exception as e:
        pytest.fail(f"Unexpected error when trying to fallback to S3: {e}")

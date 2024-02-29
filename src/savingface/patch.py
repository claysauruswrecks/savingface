import os
from functools import wraps

import boto3
from huggingface_hub import Repository
from transformers import AutoModel

# Assume S3_BUCKET_NAME is your S3 bucket where models will be backed up
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "my-model-backup-bucket")

# Setup Boto3 client
s3_client = boto3.client(
    "s3", endpoint_url=os.environ.get("S3_ENDPOINT_URL", "http://localhost:4566")
)


def patch_repository_push():
    original_push = Repository.push_to_hub

    @wraps(original_push)
    def push_to_hub_patched(self, *args, **kwargs):
        # Perform the original push to Hub operation
        result = original_push(self, *args, **kwargs)
        # Add your logic to backup to S3 here
        return result

    Repository.push_to_hub = push_to_hub_patched


def patch_from_pretrained():
    original_from_pretrained = AutoModel.from_pretrained

    @wraps(original_from_pretrained)
    def from_pretrained_patched(*args, **kwargs):
        try:
            # Try the original from_pretrained function
            return original_from_pretrained(*args, **kwargs)
        except Exception as e:
            print(e)
            # If it fails, try downloading from S3
            # s3_client.download_file(...)
            pass

    AutoModel.from_pretrained = from_pretrained_patched

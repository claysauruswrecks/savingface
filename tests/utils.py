"""Test utils."""


def delete_bucket_contents(bucket_name, s3_client):
    """Empty bucket. If the bucket uses versioning, delete all versions of all objects."""
    try:
        versions = s3_client.list_object_versions(Bucket=bucket_name)
        delete_markers = versions.get("DeleteMarkers", [])
        versions = versions.get("Versions", [])
        objects = [
            {"Key": v["Key"], "VersionId": v["VersionId"]}
            for v in versions + delete_markers
        ]
        for obj in objects:
            s3_client.delete_object(
                Bucket=bucket_name, Key=obj["Key"], VersionId=obj["VersionId"]
            )
    except s3_client.exceptions.NoSuchBucket:
        # If the bucket does not exist, ignore the error
        pass

    # Now, delete any remaining objects in the bucket.
    objects = s3_client.list_objects_v2(Bucket=bucket_name).get("Contents", [])
    for obj in objects:
        s3_client.delete_object(Bucket=bucket_name, Key=obj["Key"])

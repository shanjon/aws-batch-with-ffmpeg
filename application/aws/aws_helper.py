# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
import os

import boto3
from botocore.exceptions import ClientError
from ec2_metadata import ec2_metadata


def s3_key_exist(client, bucket, key):
    """Return True if exist, else None."""
    try:
        client.head_object(Bucket=bucket, Key=key)
    except ClientError as exc:
        if exc.response["Error"]["Code"] != "404":
            return False
    return True


def detect_running_region():
    """Dynamically determine the region."""
    easy_checks = [
        # check if set through ENV vars
        os.environ.get("AWS_REGION"),
        os.environ.get("AWS_DEFAULT_REGION"),
        # else check if set in config or in boto already
        boto3.DEFAULT_SESSION.region_name if boto3.DEFAULT_SESSION else None,
        boto3.Session().region_name,
    ]
    for region in easy_checks:
        if region:
            return region

    # else query the EC2 metadata API
    return ec2_metadata.region

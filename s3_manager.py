import botostubs
import boto3

class S3Manager:

    def __init__(self, endpoint_url=None):
        self.s3_client = boto3.client('s3', endpoint_url=endpoint_url) # type: botostubs.S3

    def upload_object(self, bucket_name, key, body):
        self.s3_client.put_object(Bucket=bucket_name, Key=key, Body=body)
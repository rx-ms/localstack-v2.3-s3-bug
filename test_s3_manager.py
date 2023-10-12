import pytest
import os
from s3_manager import S3Manager
from urllib import parse

bucket_name = "simple-versioned-bucket"

@pytest.fixture(scope="class")
def s3_manager():
    # Pointing to Localstack
    # Set dummy AWS credentials for LocalStack using os module
    os.environ['AWS_ACCESS_KEY_ID'] = 'test'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'
    return S3Manager(endpoint_url="http://localhost:4566")

@pytest.fixture(scope="function", autouse=True)
def clear_bucket_before_after_each_test(s3_manager):
    def clear_bucket():
        # List and delete all versions of all objects
        versions = s3_manager.s3_client.list_object_versions(Bucket=bucket_name)
        delete_list = []
        for version in versions.get('Versions', []):
            delete_list.append({'Key': version['Key'], 'VersionId': version['VersionId']})
        if delete_list:
            s3_manager.s3_client.delete_objects(Bucket=bucket_name, Delete={'Objects': delete_list})
    
    clear_bucket() # Clear the bucket before the test

    yield # Let the test execute

    clear_bucket() # Clear the bucket after the test

@pytest.mark.run(order=1)
def test_upload_object(s3_manager):
    key = "test-key"
    value = "test-value"
    s3_manager.upload_object(bucket_name, key, value)
    response = s3_manager.s3_client.get_object(Bucket=bucket_name, Key=key)
    assert response['Body'].read().decode() == value

@pytest.mark.run(order=2)
def test_buggy_upload_object(s3_manager):
    a_weird_key = """weird\\+/+test+key\\/=="""
    url_encoded_key = parse.quote(a_weird_key, safe='') # result is: weird%5C%2B%2F%2Btest%2Bkey%5C%2F%3D%3D
    print(url_encoded_key)
    value = "test-value"
    s3_manager.upload_object(bucket_name, url_encoded_key, value)
    response = s3_manager.s3_client.get_object(Bucket=bucket_name, Key=url_encoded_key)
    assert response['Body'].read().decode() == value


@pytest.mark.run(order=3)
def test_cleanup_verification(s3_manager):
    # This test will run after the above two tests
    # Check whether the cleanup method removed all versions of the two keys
    versions = s3_manager.s3_client.list_object_versions(Bucket=bucket_name)
    all_keys = [version['Key'] for version in versions.get('Versions', [])]
    
    assert "test-key" not in all_keys
    assert """weird%5C%2B%2F%2Btest%2Bkey%5C%2F%3D%3D""" not in all_keys
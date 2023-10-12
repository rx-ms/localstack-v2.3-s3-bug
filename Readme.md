# Sample Project to Identify Localstack Bug in S3 DELETE API

In Localstack v2.3.2's S3 implementation, there seems to be an issue when dealing with objects that have URL-encoded keys.

Specifically, when trying to delete a version of an object with a URL-encoded key, the operation does not succeed as expected.

## Test Demonstrating the Bug

### Test for Buggy Upload with URL-encoded Key:

- **Method**: `test_buggy_upload_object`
- **Description**: This test attempts to upload an object with a key that contains special characters. The key is then URL-encoded, resulting in a string like weird%5C%2B%2F%2Btest%2Bkey%5C%2F%3D%3D. The test checks if the object is successfully uploaded with the URL-encoded key.

### Test for Cleanup Verification:

- **Method**: `test_cleanup_verification`
- **Description**: This test runs after the above test and checks if the cleanup method has successfully removed all versions of the two keys (test-key and the URL-encoded key). The bug is evident when the cleanup method fails to remove the version with the URL-encoded key.

## Explanation

The issue seems to stem from the way Localstack handles URL-encoded keys.
While the upload operation works as expected, the delete operation does not recognize or handle the URL-encoded key correctly, leading to lingering versions of objects with such keys.

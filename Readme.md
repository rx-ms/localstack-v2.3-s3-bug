# Sample Project to Identify Localstack Bug in S3 DELETE API

In Localstack v2.3.2's S3 implementation, there's an issue when dealing with objects that have URL-encoded keys. Specifically, when trying to delete a version of an object with a URL-encoded key, the operation doesn't succeed as expected.

### **Tests Demonstrating the Bug**

1. **Test for Buggy Upload with URL-encoded Key**:

   - **Method**: [`test_buggy_upload_object`](https://github.com/rx-ms/localstack-v2.3-s3-bug/blob/main/test_s3_manager.py)
   - **Description**: This test attempts to upload an object with a key that contains special characters. The key is then URL-encoded. The test checks if the object is successfully uploaded with the URL-encoded key.

2. **Test for Cleanup Verification**:
   - **Method**: [`test_cleanup_verification`](https://github.com/rx-ms/localstack-v2.3-s3-bug/blob/main/test_s3_manager.py)
   - **Description**: This test runs after the above test and checks if the cleanup method has successfully removed all versions of the two keys. The bug is evident when the cleanup method fails to remove the version with the URL-encoded key.

---

## **Running the Project Locally**

### **Prerequisites**:

1. **Docker**: Ensure Docker is installed. If not, download and install from the [official Docker website](https://www.docker.com/get-started).
2. **LocalStack**: The project uses LocalStack v2.3.2 for local AWS cloud resources. Configuration is in the [`compose.yml`](https://github.com/rx-ms/localstack-v2.3-s3-bug/blob/main/compose.yml) file.
3. **AWS CDK**: The project uses AWS CDK. Install it using npm:
   ```bash
   npm install -g aws-cdk
   ```

### **Steps to Run**:

1. **Start LocalStack**: Navigate to the project root and run:

   ```bash
   docker-compose -f compose.yml up -d
   ```

2. **Bootstrap and Deploy with CDK**: Use the provided `Makefile` commands:

   - Bootstrap and deploy:
     ```bash
     make cdk-up
     ```
   - Bring down the deployed stack:
     ```bash
     make cdk-down
     ```
   - Clear residual volumes:
     ```bash
     make cdk-clear
     ```

3. **Run the Tests**: After setup, run the tests in `test_s3_manager.py` to reproduce the bug.

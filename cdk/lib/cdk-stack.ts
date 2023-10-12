import * as cdk from 'aws-cdk-lib';
import { BlockPublicAccess } from 'aws-cdk-lib/aws-s3';
import { Construct } from 'constructs';
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class CdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    /** A simple versioned s3 bucket */
    new cdk.aws_s3.Bucket(this, 'simple-bucket', {
      bucketName: 'simple-versioned-bucket',
      versioned: true,
      blockPublicAccess: BlockPublicAccess.BLOCK_ALL
    })
  }
}

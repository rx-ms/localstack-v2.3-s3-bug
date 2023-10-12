cdk-up:
	cd cdk && \
	npm ci --force && \
	npm test && \
	docker compose up -d && \
	CDK_DEFAULT_ACCOUNT=00000 CDK_DEFAULT_REGION=eu-east-1 cdklocal bootstrap && \
	CDK_DEFAULT_ACCOUNT=00000 CDK_DEFAULT_REGION=eu-east-1 cdklocal deploy --all
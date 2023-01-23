Simple project to test issue with was credentials in asf lambda provider.

Start localstack with:

```
LAMBDA_REMOTE_DOCKER=0 PROVIDER_OVERRIDE_LAMBDA=asf localstack start
```

Run tests:

```
export AWS_REGION=us-east-1
npm install -g aws-cdk-local aws-cdk
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
cdklocal bootstrap
cdklocal synth
cdklocal deploy
pytest tests
```

The test currently fails as the boto3 call to cognito fails with "The security token included in the request is invalid"

If instead localstack is started with:

```
LAMBDA_REMOTE_DOCKER=0 localstack start
```

The tests pass

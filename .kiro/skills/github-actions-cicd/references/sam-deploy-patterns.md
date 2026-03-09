# SAM Deploy Patterns

## Single Environment Deploy Job

```yaml
deploy:
  needs: [build, test]
  runs-on: ubuntu-latest
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
  permissions:
    id-token: write
    contents: read
  steps:
    - uses: actions/checkout@v4
    - uses: aws-actions/setup-sam@v2
    - uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
        aws-region: ${{ secrets.AWS_REGION }}
    - run: sam build
    - run: sam deploy --no-confirm-changeset --no-fail-on-empty-changeset
```

## Multi-Environment Deploy (Staging + Production)

Use GitHub Environments to separate configs:

```yaml
deploy-staging:
  needs: [build, test]
  if: github.ref == 'refs/heads/develop' && github.event_name == 'push'
  environment: staging
  runs-on: ubuntu-latest
  permissions:
    id-token: write
    contents: read
  steps:
    - uses: actions/checkout@v4
    - uses: aws-actions/setup-sam@v2
    - uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
        aws-region: ${{ secrets.AWS_REGION }}
    - run: sam build
    - run: sam deploy --config-env staging --no-confirm-changeset --no-fail-on-empty-changeset

deploy-production:
  needs: [build, test]
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
  environment: production
  runs-on: ubuntu-latest
  permissions:
    id-token: write
    contents: read
  steps:
    - uses: actions/checkout@v4
    - uses: aws-actions/setup-sam@v2
    - uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
        aws-region: ${{ secrets.AWS_REGION }}
    - run: sam build
    - run: sam deploy --config-env production --no-confirm-changeset --no-fail-on-empty-changeset
```

## samconfig.toml Example

```toml
version = 0.1

[default.deploy.parameters]
stack_name = "my-app"
resolve_s3 = true
capabilities = "CAPABILITY_IAM"
region = "us-east-1"

[staging.deploy.parameters]
stack_name = "my-app-staging"
resolve_s3 = true
capabilities = "CAPABILITY_IAM"
region = "us-east-1"
parameter_overrides = "Environment=staging"

[production.deploy.parameters]
stack_name = "my-app-production"
resolve_s3 = true
capabilities = "CAPABILITY_IAM"
region = "us-east-1"
parameter_overrides = "Environment=production"
```

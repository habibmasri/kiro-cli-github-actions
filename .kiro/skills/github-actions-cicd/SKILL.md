---
name: github-actions-cicd
description: Generate GitHub Actions CI/CD workflows for Python Lambda projects using SAM. Use when creating pipelines, adding CI/CD, generating workflow YAML, or deploying Lambda functions with GitHub Actions.
---

## Workflow Structure

Generate GitHub Actions workflows with three jobs:

1. **build** — Run `sam build` to compile the SAM application
2. **test** — Install dependencies and run `pytest`
3. **deploy** — Run `sam deploy` to deploy to AWS (only on push to `main`)

## Triggers

- `push` to `main` branch (full pipeline: build → test → deploy)
- `pull_request` to `main` branch (build → test only, no deploy)

## Technology Stack

- Python 3.12 (default), support matrix builds for 3.11 and 3.12
- AWS SAM CLI for build and deploy
- pytest for testing
- pip for dependency management

## AWS Authentication

Always use OIDC (OpenID Connect) for AWS credentials via `aws-actions/configure-aws-credentials`. Never use static access keys. The workflow should reference these secrets:
- `AWS_ROLE_TO_ASSUME` — IAM role ARN for OIDC
- `AWS_REGION` — target deployment region

## Caching

Use `actions/cache` for pip dependencies:
- Cache key: `pip-${{ runner.os }}-${{ hashFiles('**/requirements*.txt') }}`
- Cache path: `~/.cache/pip`

## SAM Deploy Configuration

- Use `samconfig.toml` for environment-specific deploy parameters
- Use `--no-confirm-changeset` and `--no-fail-on-empty-changeset` flags
- Reference `references/sam-deploy-patterns.md` for environment-specific patterns

## Environment Strategy

- `staging` environment: deploys on push to `develop` branch
- `production` environment: deploys on push to `main` branch
- Use GitHub Environments for environment-specific secrets and protection rules

## Best Practices

Reference `references/github-actions-best-practices.md` for:
- Matrix build configuration
- Caching strategies
- Security hardening
- Job dependency patterns

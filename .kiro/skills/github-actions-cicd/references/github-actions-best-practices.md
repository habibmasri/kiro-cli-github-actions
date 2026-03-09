# GitHub Actions Best Practices

## Matrix Builds

Test across multiple Python versions:

```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12"]
steps:
  - uses: actions/setup-python@v5
    with:
      python-version: ${{ matrix.python-version }}
```

## Pip Caching

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: pip-${{ runner.os }}-${{ hashFiles('**/requirements*.txt') }}
    restore-keys: |
      pip-${{ runner.os }}-
```

## Security Hardening

- Always pin action versions to full SHA or major version tags
- Use OIDC for AWS auth — never store static AWS keys as secrets
- Set minimum `permissions` per job instead of using defaults
- Use GitHub Environments with protection rules for production deploys

## Job Dependencies

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
  test:
    needs: build
    runs-on: ubuntu-latest
  deploy:
    needs: [build, test]
    runs-on: ubuntu-latest
```

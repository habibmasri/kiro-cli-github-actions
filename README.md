# Generating GitHub Actions Workflows with Kiro

A demo repo showing how to use [Kiro](https://kiro.dev) to generate a complete CI/CD pipeline in GitHub Actions for a Python Lambda project using AWS SAM.

## Project Structure

```
├── src/
│   └── app.py                # Lambda handler
├── tests/
│   └── test_app.py           # Unit tests
├── template.yaml             # SAM template
├── samconfig.toml            # SAM deploy config
└── .kiro/skills/
    └── github-actions-cicd/  # Kiro skill for generating workflows
```

## Local Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest
python -m pytest tests/ -v
```

## Deploy

```bash
sam build
sam deploy
```

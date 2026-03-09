import json
import sys
import os
from dataclasses import dataclass

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from app import lambda_handler


@dataclass
class FakeLambdaContext:
    function_name: str = "test"
    memory_limit_in_mb: int = 128
    invoked_function_arn: str = "arn:aws:lambda:us-east-1:123456789012:function:test"
    aws_request_id: str = "test-id"


def _make_event(method="GET", path="/"):
    return {"httpMethod": method, "path": path}


def test_root_returns_hello():
    result = lambda_handler(_make_event(path="/"), FakeLambdaContext())
    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["message"] == "Hello from Kiro-generated pipeline!"


def test_health_returns_healthy():
    result = lambda_handler(_make_event(path="/health"), FakeLambdaContext())
    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["status"] == "healthy"


def test_unknown_path_returns_404():
    result = lambda_handler(_make_event(path="/nope"), FakeLambdaContext())
    assert result["statusCode"] == 404

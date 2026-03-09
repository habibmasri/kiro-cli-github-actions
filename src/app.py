import json
from aws_lambda_powertools import Logger

logger = Logger()


@logger.inject_lambda_context
def lambda_handler(event, context):
    http_method = event.get("httpMethod", "GET")
    path = event.get("path", "/")

    if path == "/" and http_method == "GET":
        logger.info("Root endpoint called")
        return _response(200, {"message": "Hello from Kiro-generated pipeline!"})

    if path == "/health" and http_method == "GET":
        return _response(200, {"status": "healthy"})

    logger.warning("Path not found", extra={"path": path})
    return _response(404, {"error": "Not found"})


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }

from flask import current_app


def versioned_endpoint(endpoint: str) -> str:
    """Format endpoint with current API version.

    Args:
        endpoint (str): Endpoint

    Returns:
        str: Versioned endpoint
    """
    return "/".join([current_app.config["API_VERSION"], endpoint.lstrip("/")])

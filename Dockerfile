FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /code

COPY pyproject.toml .
COPY tests/deploy.feature tests/
COPY tests/test_deploy.py tests/

# Run the main command
CMD uv run poe ci

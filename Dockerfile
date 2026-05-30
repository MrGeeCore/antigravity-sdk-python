FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /workspace

# Install build tools
RUN apt-get update && apt-get install -y build-essential git curl && rm -rf /var/lib/apt/lists/*

# Upgrade packaging tools and install build helper
RUN python -m pip install --upgrade pip setuptools wheel build

# Copy project
COPY . /workspace

# Install test dependencies (pinned list). If it fails, at least install pytest.
RUN python -m pip install -r .kokoro/requirements-test.txt || python -m pip install pytest

# Install package from source
RUN python -m pip install .

# Run tests by default
CMD ["pytest", "-q"]

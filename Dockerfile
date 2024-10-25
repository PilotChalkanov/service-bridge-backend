FROM ubuntu:latest
LABEL authors="niko"

# Install ubuntu packages
# Install Ubuntu packages with specific Python version
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y build-essential make gcc git unzip wget python3.11 python3.11-dev python3-pip python-is-python3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set Python 3.11 as the default python3
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1


ENV PIP_DISABLE_PIP_VERSION_CHECK=on
#Install poetry
RUN pip3 install poetry
WORKDIR /app
COPY pyproject.toml /app/
#Install dependencies
RUN pip3 install cffi cryptography
RUN poetry config virtualenvs.create true \
    && poetry config virtualenvs.in-project false \
    && poetry install --no-interaction
COPY service_bridge .
EXPOSE 5000
#cache
CMD poetry run quart -e ./.env run -h 0.0.0.0 -p 5000



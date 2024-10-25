FROM ubuntu:latest
LABEL authors="niko"

# Install ubuntu packages
RUN apt-get update && \
    apt-get install -y build-essential make gcc git unzip wget python3-dev python3-pip python-is-python3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
#Install poetry
RUN pip3 install poetry
WORKDIR /service_bridge
COPY pyproject.toml /service_bridge/
#Install dependencies
RUN poetry config virtualenvs.create true \
    && poetry config virtualenvs.in-project false \
    && poetry install --no-interaction
COPY . .
EXPOSE 5000
CMD ["poetry", "run", "quart", "--host", "0.0.0.0"]

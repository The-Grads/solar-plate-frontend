FROM python:3.10.2-slim

# Build arguments
ARG UID

# Install base dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-jre \
    git \
    curl \
    wget \
    openssh-client

# Install GCC, Make, libpq-dev (for psicopg) and procps
RUN apt-get install -y gcc libpq-dev make graphviz procps gettext-base

# Install Postgres Client
RUN mkdir -p /usr/share/man/man1 \
    && mkdir -p /usr/share/man/man7 \
    && apt-get install -y postgresql-client

# Create python user 
RUN useradd -ms /bin/bash -u ${UID} python
WORKDIR /home/python/app/code
USER python

# Install pdm
RUN pip install -U pdm

# Define environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV MY_PYTHON_PACKAGES="/home/python/app/code/__pypackages__/3.10"
ENV PYTHONPATH="${PYTHONPATH}:${MY_PYTHON_PACKAGES}/bin:${MY_PYTHON_PACKAGES}/lib:/home/python/app/code"
ENV PATH="${PATH}:${MY_PYTHON_PACKAGES}/bin:/home/python/.local/bin"
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
RUN pdm config python.use_venv false

CMD [ "tail", "-f", "/dev/null" ]
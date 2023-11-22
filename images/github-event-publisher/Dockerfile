ARG PYTHON_VERSION

################################
# Install Linux OS (including Python)
################################

FROM python:${PYTHON_VERSION}-slim-bookworm

################################
# Install Poetry
################################

ARG POETRY_VERSION

RUN pip install poetry==${POETRY_VERSION}

################################
# Copy Files and Directories
################################

WORKDIR github-public-event-streaming
COPY .env base.env pyproject.toml poetry.lock ./
ADD src src
ADD .secrets .secrets
#  Poetry will complain if a README.md is not found
RUN touch README.md

# ################################
# # Install Project dependencies
# ################################

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN poetry install --without dev && rm -rf $POETRY_CACHE_DIR

# ################################
# # Run Script
# ################################

ENTRYPOINT ["poetry", "run", "python", "src/pubsub/publisher/publish_events.py"]
# Grace à https://sourcery.ai/blog/python-docker/
FROM python:3.9-slim-buster as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# App specific env
ENV SETTLE_DURATION=5
ENV INTAKE_DIR=/scanman/intake
ENV COMPLETED_DIR=/scanman/completed

FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy


FROM base AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends \
  netpbm \
  ghostscript \
  poppler-utils \
  imagemagick \
  unpaper \
  util-linux \
  tesseract-ocr \
  parallel \
  units \
  ssh \
  git \
  vim \
  bash \
  bc

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Create and switch to a new user
RUN useradd --create-home scanman
RUN mkdir /scanman && chown scanman scanman
USER scanman

WORKDIR /scanman

# Install application into container
COPY app /scanman/
RUN mkdir -p /scanman/intake
RUN mkdir -p /scanman/completed

# Run the application
#ENTRYPOINT ["python", "/scanman/scanman.py" ]
CMD [ "python", "/scanman/scanman.py" ]

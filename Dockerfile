# Grace à https://sourcery.ai/blog/python-docker/
FROM python:3.9-slim-buster as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# App specific env
ENV SETTLE_DURATION=5
ENV APP_ROOT=/scantool
ENV INTAKE_DIR=$APP_ROOT/intake
ENV COMPLETED_DIR=$APP_ROOT/completed

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
  ocrmypdf \ 
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
  curl \
  bc

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Create and switch to a new user
# disabling for now while I sort out how to handling permissions on the intake
# volume
#RUN useradd --create-home scantool
#RUN mkdir /scantool && chown scantool scantool
#USER scantool

RUN mkdir $APP_ROOT

WORKDIR $APP_ROOT

# Install application into container
COPY scantool $APP_ROOT/
RUN mkdir -p $INTAKE_DIR
RUN mkdir -p $COMPLETED_DIR

## HACK ALERT ##
#
# In some circumstances unpaper emits a warning to STDERR which is merged with STDOUT
# by ocrmypdf.  This causes the version check to fail and ocrmypdf to think that
# unpaper is not properly installed.  We will wrap the original binary in a script
# that can filter out the warning.
#
# https://github.com/ocrmypdf/OCRmyPDF/issues/1409
RUN mv /usr/bin/unpaper /usr/bin/unpaper-inner
COPY unpaper-wrapper.sh /usr/bin/unpaper
RUN chmod 755 /usr/bin/unpaper

# Run the application
CMD [ "python", "scantool.py" ]

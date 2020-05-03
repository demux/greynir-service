FROM pypy:3.6

ENV APP_DIR /app/

# Install system dependencies:
RUN pypy3 -m pip install --no-cache-dir -U \
        poetry \
        gunicorn

RUN mkdir ${APP_DIR}
WORKDIR ${APP_DIR}

# Install python dependencies:
ADD pyproject.toml poetry.lock ${APP_DIR}
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# NOTE: Make sure you create a .dockerignore file if any large
#       files or directories should be excluded
ADD . ${APP_DIR}

# Start supervisord
CMD ["gunicorn", "app:create_app()", "-w 4", "-b 0.0.0.0:80", "-t 300"]

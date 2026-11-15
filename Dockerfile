# upgrade: skip
FROM python:3.13-slim

# upgrade: pypi fastapi
ARG FASTAPI_VERSION=0.163.1
# upgrade: pypi uvicorn
ARG UVICORN_VERSION=0.54.0

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app

COPY requirements.txt .
RUN printf 'fastapi==%s\nuvicorn==%s\n' "$FASTAPI_VERSION" "$UVICORN_VERSION" > /tmp/pins.txt \
 && pip install --no-cache-dir -c /tmp/pins.txt -r requirements.txt

COPY . .
RUN useradd --create-home --uid 1000 app && chown -R app /app
USER app

CMD ["./start.sh"]

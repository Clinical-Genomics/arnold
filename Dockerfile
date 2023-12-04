FROM python:3.11-slim

LABEL base_image="python:3.11-slim"
LABEL about.home="https://github.com/Clinical-Genomics/arnold"
LABEL about.tags="CG Core database and API"


ENV GUNICORN_WORKERS=1
ENV GUNICORN_THREADS=1
ENV GUNICORN_BIND="0.0.0.0:8000"
ENV GUNICORN_TIMEOUT=400
ENV VERSION="v1"

ENV DB_URI="mongodb://localhost:27017/arnold-demo"
ENV DB_NAME="arnold-demo"

EXPOSE 8000

WORKDIR /home/worker/app
COPY . /home/worker/app

# Install app requirements
RUN pip install -r requirements.txt

# Install app
RUN pip install -e .

CMD gunicorn \
    --workers=$GUNICORN_WORKERS \
    --bind=$GUNICORN_BIND  \
    --threads=$GUNICORN_THREADS \
    --timeout=$GUNICORN_TIMEOUT \
    --proxy-protocol \
    --forwarded-allow-ips="10.0.2.100,127.0.0.1" \
    --log-syslog \
    --access-logfile - \
    --log-level="debug" \
    --worker-class=uvicorn.workers.UvicornWorker \
    arnold.api.api_$VERSION.api:app

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    REPO_ROOT=/srv/repo \
    VECTOR_DB_PATH=/srv/vector_db

WORKDIR /srv

COPY Agent/requirements.txt /srv/requirements.txt
RUN pip install --no-cache-dir -r /srv/requirements.txt

COPY . /srv/repo
WORKDIR /srv/repo/Agent

RUN chmod +x scripts/start.sh

EXPOSE 8000

CMD ["bash", "scripts/start.sh"]

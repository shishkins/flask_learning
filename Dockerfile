FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=TRUE

RUN apt-get update && apt-get install -y build-essential python3-dev \
    libldap2-dev libsasl2-dev slapd ldap-utils git

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY app /app
COPY manage.py .
COPY create_db.py .
RUN python create_db.py
COPY entrypoint.sh .
ENTRYPOINT ["bash", "entrypoint.sh"]
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    pkg-config \
    ca-certificates \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/odoo
COPY . /opt/odoo
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python3", "odoo-bin", "-c", "/opt/odoo/odoo.conf.production"]

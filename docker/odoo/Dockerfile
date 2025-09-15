FROM python:3.12-slim

# Install system deps required to build some python packages (psycopg2, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    pkg-config \
    ca-certificates \
    git \
    # Dependencies required to build python-ldap and other native extensions
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/odoo

# We don't copy the whole repo to avoid sending a large build context.
# Instead the repository is mounted at runtime via docker-compose volumes and
# dependencies are installed at container start using the mounted requirements.txt.
RUN pip install --upgrade pip

CMD ["bash", "-c", "pip install -r /opt/odoo/requirements.txt && python3 /opt/odoo/odoo-bin -c /opt/odoo/odoo.conf.production"]

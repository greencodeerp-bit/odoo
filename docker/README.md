# Docker deployment for Odoo (minimal)

This folder contains a minimal `docker-compose.yml` setup to run PostgreSQL + Odoo for testing/QA.

Files:
- `../docker-compose.yml`: Compose file that starts `db` (Postgres) and `odoo` (Python runner mounting repo).
- `../odoo.conf.production`: Example Odoo config for production-like run.

How to run (development/test only):

1. Copy environment variables if needed:

```bash
cp .env.example .env
# Edit .env to set POSTGRES_PASSWORD and ADMIN_PASS
```

2. Start the stack:

```bash
docker compose up -d --build
```

3. Wait for Odoo to start (logs):

```bash
docker compose logs -f odoo
```

4. Create the database (script will attempt to connect and create):

```bash
python3 scripts/create_db.py
```

Notes:
- This setup is intended for quick local testing and to bootstrap a DB. It is not production-hardened. For production use a proper image (Odoo docker images / build with pinned versions), a reverse-proxy (nginx), SSL, persistent storage and backup strategies.

# Despliegue de producción (docker-compose)

Este documento explica cómo levantar una instancia de Odoo en producción usando Docker Compose.

Requisitos:
- Docker Engine y Docker Compose v2 instalados en el servidor.
- Certificados SSL (puedes usar Let's Encrypt o proporcionar tus certificados en `deploy/nginx/certs`).

Archivos relevantes:
- `deploy/docker-compose.prod.yml` - stack de producción (Postgres, Odoo, Nginx como reverse proxy).
- `odoo.conf.production` - configuración de Odoo.
- `deploy/.env.prod.example` - ejemplo de variables de entorno.

Pasos rápidos:

1. Copia el `env`:

```bash
cp deploy/.env.prod.example .env
# Edita .env y cambia POSTGRES_PASSWORD y ADMIN_PASS
```

2. Crear directorios para certificados y Nginx config (si no existen):

```bash
mkdir -p deploy/nginx/conf.d deploy/nginx/certs
# Añade tu archivo de configuración en deploy/nginx/conf.d/odoo.conf
```

3. Construir y lanzar:

```bash
docker compose -f deploy/docker-compose.prod.yml --env-file .env up -d --build
```

4. Verificar servicios:

```bash
docker compose -f deploy/docker-compose.prod.yml ps
docker compose -f deploy/docker-compose.prod.yml logs -f odoo
```

Backups y mantenimiento recomendados:
- Programar backups periódicos de la base de datos (pg_dump) y del filestore (`odoo-filestore`).
- Monitorizar logs y pruebas de salud.

Seguridad:
- No expongas puertos como 8069 públicamente; exponer solo a través del reverse proxy (Nginx) con SSL.

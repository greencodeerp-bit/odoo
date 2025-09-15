## Configuración del Devcontainer y token de CI

Este repositorio publica una imagen base del devcontainer a GHCR y el workflow `auto-pin-devcontainer-digest` actualiza automáticamente el pin en `.devcontainer/devcontainer.json`.

Si tu organización o repositorio limita lo que `GITHUB_TOKEN` puede hacer (por ejemplo, no permite push/merge a ramas protegidas o no permite acceso a paquetes), crea un token personal (PAT) con los scopes mínimos recomendados y guárdalo como secret `DEVCONTAINER_PAT` en `Settings > Secrets` del repositorio.

Scopes recomendados para `DEVCONTAINER_PAT` (mínimos necesarios):

- `repo` (full control of private repositories) — necesario si el repositorio es privado y el workflow debe push/merge branches.
- `workflow` — para que el token pueda gestionar workflows cuando sea necesario.
- `write:packages` o `read:packages` — para acceder a GHCR si el repositorio las políticas lo requieren (normalmente `read:packages` basta para `docker pull`).

Notas de seguridad:
- Prefiere crear un token específico para CI (no uses tu token personal de uso interactivo). Limítalo al repositorio o a la organización cuando sea posible.
- Rota el token periódicamente.

Cómo crear el secret en GitHub (UI):

1. Ve a `https://github.com/<owner>/<repo>/settings/secrets` (ej: `https://github.com/greencodeerp-bit/odoo/settings/secrets`) y selecciona "New repository secret".
2. Nombre: `DEVCONTAINER_PAT`.
3. Value: pega el token PAT.

Uso y comportamiento esperado del workflow:

- El workflow `auto-pin-devcontainer-digest` ahora utiliza `secrets.DEVCONTAINER_PAT` si está presente; si no, usa `secrets.GITHUB_TOKEN` como fallback. Esto permite que el workflow pueda empujar/mergear y etiquetar PRs aun cuando `GITHUB_TOKEN` tenga permisos limitados.
- Flujo resumido:
  1. Se construye y publica la imagen base a GHCR (`:latest`).
  2. El workflow obtiene el `Docker-Content-Digest` de `:latest`.
  3. Actualiza `.devcontainer/devcontainer.json` para pinnear la imagen por digest.
  4. Crea un PR con la actualización y lo mergea (squash) automáticamente.
  5. Añade una entrada al changelog `doc/DEVCONTAINER_CHANGES.md` en una rama diaria `devcontainer/chlog-YYYY-MM-DD` y crea/mergea el PR correspondiente.

Comandos útiles para probar manualmente (local):

```bash
# Login gh CLI
gh auth login

# Login a GHCR usando el PAT (si lo tienes en variable CR_PAT)
echo "$DEVCONTAINER_PAT" | docker login ghcr.io -u $(gh api user --jq '.login') --password-stdin

# Pull de la imagen pinned (ejemplo)
docker pull ghcr.io/greencodeerp-bit/odoo-devcontainer-base@sha256:<digest>
```

Si ves errores de permisos en las acciones del workflow (push/merge/label/comment), asegúrate de que el secret `DEVCONTAINER_PAT` exista y tenga los scopes adecuados. Si la organización deshabilita `GITHUB_TOKEN` ciertas acciones a nivel org, el PAT es la forma habitual de dar permisos más amplios a un workflow.

Si quieres, puedo añadir instrucciones para crear el PAT con la CLI (`gh`), o cambiar el workflow para exponer pasos de diagnóstico más detallados.
# Devcontainer setup notes

Resumen:

- Durante la creación del devcontainer/Codespace se detectó `Python 3.12.1` y el paso de instalación de dependencias falló.
- Error observado: compilación fallida de `python-ldap` con mensaje `fatal error: lber.h: No such file or directory`.

Qué hice:

1. En el Codespace instalé las dependencias del sistema requeridas para compilar extensiones nativas: `build-essential`, `libldap2-dev`, `libsasl2-dev`, `libssl-dev`, `pkg-config`.
2. Reintenté `pip install -r requirements.txt` y la instalación finalizó correctamente.
3. Añadí un devcontainer (`.devcontainer/Dockerfile`) que instala dichas dependencias de sistema y un `devcontainer.json` con `postCreateCommand` para ejecutar `pip install -r requirements.txt` al crear el contenedor.
4. Añadí extensiones recomendadas (`ms-python.vscode-pylance`, `ms-azuretools.vscode-docker`) y moví `settings` bajo `customizations.vscode.settings`.

Recomendaciones:

- Mantener las dependencias del sistema necesarias en la imagen del devcontainer para evitar fallos en `pip` al compilar extensiones nativas.
- Evitar ejecutar `pip install` como `root` si se quiere mantener paquetes en el entorno de usuario; ajustar el `remoteUser` y paths según políticas del proyecto.
- Considerar usar ruedas precompiladas o versiones de dependencias compatibles con la versión de Python usada por la imagen para reducir compilaciones.

Acceso a la imagen publicada en GitHub Container Registry (GHCR)

- La imagen devcontainer se publica en: `ghcr.io/greencodeerp-bit/odoo-devcontainer-base`
- En el repo hemos fijado la referencia a un digest seguro en ` .devcontainer/devcontainer.json`:
	- `ghcr.io/greencodeerp-bit/odoo-devcontainer-base@sha256:bc6a3959eb92bba16f8dbe498ea5d1fa8660e17eb8579aad270cdfac3719e812`

Si la imagen es privada (no pública), los usuarios deberán autenticarse para poder `docker pull` o crear el devcontainer. Instrucciones rápidas:

1) Generar un Personal Access Token (PAT) en GitHub con el scope `read:packages` (o `packages:read`).

2) Login en GHCR con Docker:

```bash
# Reemplaza $CR_PAT por tu token o exporta en el entorno: export CR_PAT=ghp_... 
echo $CR_PAT | docker login ghcr.io -u <your-github-username> --password-stdin
```

3) Tirar la imagen explicitamente (opcional):

```bash
docker pull ghcr.io/greencodeerp-bit/odoo-devcontainer-base@sha256:bc6a3959eb92bba16f8dbe498ea5d1fa8660e17eb8579aad270cdfac3719e812
```

4) Si no quieres autenticar manualmente, VS Code/Remote - Containers puede usar las credenciales de `gh` si has hecho `gh auth login` y `gh auth refresh` (según configuración local).

Nota: recomendamos usar la referencia por digest para estabilidad y reproducibilidad. Si se desea un comportamiento de actualización controlada, se puede mantener `:latest` pero con la política de publicar versiones y releases.

Dónde mirar si vuelve a ocurrir:

- Logs de creación del Codespace / Devcontainer (View Creation Log en VS Code: `Cmd/Ctrl+Shift+P -> View Creation Log`).
- Configuración de la plataforma (Codespaces/devcontainer templates) si hay políticas externas que ejecutan `postCreateCommand` fuera del repo.

Contacto:

Si quieres que automatice más ajustes (p. ej. añadir más extensiones, ajustar rutas de Python para CI, o crear una imagen base personalizada), puedo hacerlo.

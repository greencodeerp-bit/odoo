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

Dónde mirar si vuelve a ocurrir:

- Logs de creación del Codespace / Devcontainer (View Creation Log en VS Code: `Cmd/Ctrl+Shift+P -> View Creation Log`).
- Configuración de la plataforma (Codespaces/devcontainer templates) si hay políticas externas que ejecutan `postCreateCommand` fuera del repo.

Contacto:

Si quieres que automatice más ajustes (p. ej. añadir más extensiones, ajustar rutas de Python para CI, o crear una imagen base personalizada), puedo hacerlo.

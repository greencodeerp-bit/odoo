FROM mcr.microsoft.com/vscode/devcontainers/base:0-focal

# Instalar dependencias del sistema necesarias para compilar extensiones nativas
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libldap2-dev \
        libsasl2-dev \
        libssl-dev \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo (el contexto del repo estará montado por Codespaces/devcontainer)
WORKDIR /workspaces/odoo

# Establecer usuario por defecto
ARG USERNAME=vscode
USER ${USERNAME}

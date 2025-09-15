FROM mcr.microsoft.com/vscode/devcontainers/base:0-focal

LABEL org.opencontainers.image.title="odoo-devcontainer-base"
LABEL org.opencontainers.image.description="Base image for Odoo development with build deps for python-ldap and common native libs preinstalled."
LABEL org.opencontainers.image.licenses="MIT"

# Instalar dependencias del sistema necesarias para compilar extensiones nativas
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libldap2-dev \
        libsasl2-dev \
        libssl-dev \
        pkg-config \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Crear un usuario no-root (mantener compatibilidad con devcontainers)
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd -s /bin/bash --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME} || true

USER ${USERNAME}
WORKDIR /workspaces/odoo

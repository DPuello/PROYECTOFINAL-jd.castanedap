#!/bin/bash
# Actualizar los paquetes del sistema
echo "Actualizando paquetes del sistema..."
sudo apt-get update -y

# Instalar las dependencias necesarias para Flask y MySQLdb
echo "Instalando dependencias del sistema..."
sudo apt-get install -y \
    python3-dev \
    python3-venv \
    build-essential \
    libmysqlclient-dev \
    default-libmysqlclient-dev

# Instalar dependencias opcionales (si hay problemas con otros paquetes Flask)
echo "Instalando dependencias opcionales..."
sudo apt-get install -y libssl-dev libffi-dev
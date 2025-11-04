#!/bin/bash

# Script para build e push da imagem Docker
# Uso: ./build-and-push-docker.sh

set -e  # Para em caso de erro

IMAGE_NAME="desnecesauron/classificador-golpes-ptbr"

echo "=========================================="
echo "BUILD E PUSH DA IMAGEM DOCKER"
echo "=========================================="
echo "Imagem: $IMAGE_NAME"
echo "=========================================="

# 1. Build da imagem
echo ""
echo "📦 Fazendo build da imagem..."
docker build -t $IMAGE_NAME .

echo ""
echo "✓ Build concluído!"

# 2. Listar imagens
echo ""
echo "📋 Imagem criada:"
docker images | grep classificador-golpes-ptbr

# 3. Push para Docker Hub
echo ""
read -p "Deseja fazer push para o Docker Hub? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo ""
    echo "🚀 Fazendo push da imagem..."
    docker push $IMAGE_NAME

    echo ""
    echo "✓ Push concluído!"
    echo ""
    echo "=========================================="
    echo "IMAGEM DISPONÍVEL EM:"
    echo "  docker pull $IMAGE_NAME"
    echo "=========================================="
else
    echo ""
    echo "Push cancelado pelo usuário."
fi

echo ""
echo "Para testar localmente:"
echo "  docker run -p 5000:5000 $IMAGE_NAME"

#!/bin/bash
# SODA v1.8 - Tool Setup Script
# Installs CLI tools and Kernel dependencies.

set -e # Exit on error

echo "🚀 Iniciando SODA Tool Setup..."

# 1. OpenSpec CLI (The Law)
if ! command -v openspec &> /dev/null; then
    echo "📦 Instalando Fission-AI OpenSpec..."
    npm install -g @fission-ai/openspec@latest
else
    echo "✅ OpenSpec já instalado."
fi

# 2. Antigravity Kit CLI (Optionally used for scaffolding)
if ! command -v ag-kit &> /dev/null; then
    echo "📦 Instalando Antigravity Kit..."
    # Assumindo instalação via pip ou npm conforme documentação (ajustar se necessário)
    # Por enquanto, placeholder se não houver pacote público simples
    echo "⚠️ Ag-Kit CLI: Instalação manual requerida ou via repositório."
else
    echo "✅ Ag-Kit já instalado."
fi

# 3. SODA Kernel Dependencies (The Engine)
echo "🐍 Instalando Dependências do Kernel Python..."
if [ -f "pyproject.toml" ]; then
    pip install -e .
else
    echo "❌ pyproject.toml não encontrado na raiz de execução."
fi

echo "🎉 Setup concluído! O Arsenal está pronto."

#!/bin/bash
# Script para configurar Perplexity API Key (sem expor segredos)
if [ -z "$1" ]; then
  echo "Uso: ./setup_perplexity.sh <PERPLEXITY_API_KEY>"
  exit 1
fi
export PERPLEXITY_API_KEY="$1"
echo "✅ PERPLEXITY_API_KEY configurada para a sessão atual."
echo ""
echo "Para persistir, adicione ao seu ~/.bashrc ou ~/.zshrc:"
echo "export PERPLEXITY_API_KEY=\"$1\""
echo ""
echo "Ou crie um arquivo .env na pasta cypherguy com:"
echo "PERPLEXITY_API_KEY=$1"

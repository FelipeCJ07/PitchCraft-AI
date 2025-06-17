#!/bin/bash

# PitchCraft AI - Script de Instalação Automatizada
# Este script configura automaticamente o ambiente de desenvolvimento

set -e

echo "🚀 Iniciando instalação do PitchCraft AI..."

# Verificar pré-requisitos
echo "📋 Verificando pré-requisitos..."

# Verificar Python
if ! command -v python3.11 &> /dev/null; then
    echo "❌ Python 3.11 não encontrado. Por favor, instale Python 3.11+"
    exit 1
fi

# Verificar Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Por favor, instale Node.js 20+"
    exit 1
fi

# Verificar pnpm
if ! command -v pnpm &> /dev/null; then
    echo "📦 Instalando pnpm..."
    npm install -g pnpm
fi

echo "✅ Pré-requisitos verificados!"

# Configurar Backend
echo "🔧 Configurando Backend..."
cd backend

# Criar ambiente virtual
echo "📦 Criando ambiente virtual Python..."
python3.11 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
echo "📦 Instalando dependências Python..."
pip install --upgrade pip
pip install -r requirements.txt

# Criar arquivo .env se não existir
if [ ! -f .env ]; then
    echo "📝 Criando arquivo .env..."
    cp .env.example .env
    echo "⚠️  IMPORTANTE: Configure suas chaves de API no arquivo backend/.env"
fi

cd ..

# Configurar Frontend
echo "🎨 Configurando Frontend..."
cd frontend

# Instalar dependências
echo "📦 Instalando dependências Node.js..."
pnpm install

cd ..

# Criar diretórios necessários
echo "📁 Criando estrutura de diretórios..."
mkdir -p logs
mkdir -p uploads
mkdir -p backups

# Configurar permissões
chmod +x install.sh
chmod +x start.sh

echo "🎉 Instalação concluída com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo "1. Configure suas chaves de API no arquivo backend/.env"
echo "2. Execute './start.sh' para iniciar a aplicação"
echo "3. Acesse http://localhost:5174 para usar a aplicação"
echo ""
echo "📖 Consulte o README.md para mais informações"
echo "📚 Manual do usuário: MANUAL_USUARIO.md"
echo "🔧 Documentação técnica: DOCUMENTACAO_TECNICA.md"


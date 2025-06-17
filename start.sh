#!/bin/bash

# PitchCraft AI - Script de Inicialização
# Este script inicia todos os serviços necessários

set -e

echo "🚀 Iniciando PitchCraft AI..."

# Função para verificar se uma porta está em uso
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Porta $1 já está em uso"
        return 1
    fi
    return 0
}

# Verificar portas
echo "🔍 Verificando portas disponíveis..."
if ! check_port 5000; then
    echo "❌ Backend não pode iniciar - porta 5000 ocupada"
    exit 1
fi

if ! check_port 5173; then
    echo "⚠️  Porta 5173 ocupada, tentando 5174..."
fi

# Iniciar Backend
echo "🔧 Iniciando Backend..."
cd backend

# Ativar ambiente virtual
source venv/bin/activate

# Verificar se .env existe
if [ ! -f .env ]; then
    echo "❌ Arquivo .env não encontrado. Execute ./install.sh primeiro"
    exit 1
fi

# Iniciar servidor Flask em background
echo "🌐 Iniciando servidor Flask na porta 5000..."
python src/main.py &
BACKEND_PID=$!

cd ..

# Aguardar backend inicializar
echo "⏳ Aguardando backend inicializar..."
sleep 5

# Verificar se backend está rodando
if ! curl -s http://localhost:5000/api/health > /dev/null; then
    echo "❌ Backend falhou ao inicializar"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

echo "✅ Backend iniciado com sucesso!"

# Iniciar Frontend
echo "🎨 Iniciando Frontend..."
cd frontend

# Iniciar servidor Vite
echo "🌐 Iniciando servidor Vite..."
pnpm run dev --host &
FRONTEND_PID=$!

cd ..

# Aguardar frontend inicializar
echo "⏳ Aguardando frontend inicializar..."
sleep 10

echo "🎉 PitchCraft AI iniciado com sucesso!"
echo ""
echo "📱 Aplicação disponível em:"
echo "   Frontend: http://localhost:5173 ou http://localhost:5174"
echo "   Backend:  http://localhost:5000"
echo ""
echo "📊 Endpoints da API:"
echo "   Health Check: http://localhost:5000/api/health"
echo "   Projetos:     http://localhost:5000/api/projects"
echo ""
echo "🛑 Para parar a aplicação, pressione Ctrl+C"

# Função para cleanup ao sair
cleanup() {
    echo ""
    echo "🛑 Parando serviços..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo "✅ Serviços parados"
    exit 0
}

# Capturar sinais para cleanup
trap cleanup SIGINT SIGTERM

# Manter script rodando
wait


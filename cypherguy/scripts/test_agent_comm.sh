#!/bin/bash

# Script para testar comunicação HTTP entre agents

echo "🧪 TESTANDO COMUNICAÇÃO ENTRE AGENTS"
echo "===================================="
echo ""

BASE_URL="http://localhost"

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para testar health de um agent
test_health() {
    local name=$1
    local port=$2
    
    echo -n "Testando $name (port $port)... "
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL:$port/health" 2>/dev/null)
    
    if [ "$response" = "200" ]; then
        echo -e "${GREEN}✅ OK${NC}"
        return 0
    else
        echo -e "${RED}❌ FALHOU (HTTP $response)${NC}"
        return 1
    fi
}

# Testar health de todos os agents
echo "1️⃣  TESTANDO HEALTH DOS AGENTS"
echo "------------------------------"
test_health "IntakeAgent " 8101
test_health "PolicyAgent " 8102
test_health "ComputeAgent" 8103
test_health "ExecutorAgent" 8104
echo ""

# Testar fluxo completo de crédito
echo "2️⃣  TESTANDO FLUXO COMPLETO (CREDIT)"
echo "------------------------------------"
echo "Enviando request para IntakeAgent..."
echo ""

curl -X POST "$BASE_URL:8101/process_credit" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user_123",
    "amount": 5000,
    "token": "USDC",
    "collateral": "SOL"
  }' \
  -w "\n\nHTTP Status: %{http_code}\n" \
  2>/dev/null | python3 -m json.tool 2>/dev/null || echo "(Response não é JSON válido)"

echo ""
echo "3️⃣  VERIFICANDO LOGS"
echo "--------------------"
echo "Últimas 10 linhas de cada agent:"
echo ""

if [ -f "../logs/intake_agent.log" ]; then
    echo -e "${YELLOW}[IntakeAgent]${NC}"
    tail -5 ../logs/intake_agent.log 2>/dev/null || echo "  (log não encontrado)"
    echo ""
fi

if [ -f "../logs/policy_agent.log" ]; then
    echo -e "${YELLOW}[PolicyAgent]${NC}"
    tail -5 ../logs/policy_agent.log 2>/dev/null || echo "  (log não encontrado)"
    echo ""
fi

if [ -f "../logs/compute_agent.log" ]; then
    echo -e "${YELLOW}[ComputeAgent]${NC}"
    tail -5 ../logs/compute_agent.log 2>/dev/null || echo "  (log não encontrado)"
    echo ""
fi

if [ -f "../logs/executor_agent.log" ]; then
    echo -e "${YELLOW}[ExecutorAgent]${NC}"
    tail -5 ../logs/executor_agent.log 2>/dev/null || echo "  (log não encontrado)"
    echo ""
fi

echo "===================================="
echo "✅ Teste completo!"
echo ""
echo "💡 Dica: Para ver logs em tempo real durante requests:"
echo "   Terminal 1: tail -f logs/intake_agent.log"
echo "   Terminal 2: tail -f logs/policy_agent.log"
echo "   Terminal 3: tail -f logs/compute_agent.log"
echo "   Terminal 4: tail -f logs/executor_agent.log"
echo ""


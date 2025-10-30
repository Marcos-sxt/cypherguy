#!/bin/bash

echo "🚀 TESTANDO AGENTS COM TOOLS REAIS"
echo "=================================="
echo ""

# Criar diretório de logs se não existir
mkdir -p logs

# Limpar logs antigos
echo "🧹 Limpando logs antigos..."
rm -f logs/*.log

echo ""
echo "📥 Iniciando Agents..."
echo "--------------------"

# Iniciar IntakeAgent
echo "Starting IntakeAgent (port 8101)..."
cd "/home/user/Documents/SOLANA CYPHERPUNK/cypherguy"
nohup python3 agents/intake_agent.py > logs/intake_agent.log 2>&1 &
INTAKE_PID=$!
echo "  PID: $INTAKE_PID"

# Iniciar PolicyAgent
echo "Starting PolicyAgent (port 8102)..."
nohup python3 agents/policy_agent.py > logs/policy_agent.log 2>&1 &
POLICY_PID=$!
echo "  PID: $POLICY_PID"

# Iniciar ComputeAgent (COM TOOLS!)
echo "Starting ComputeAgent (port 8103) WITH TOOLS..."
nohup python3 agents/compute_agent.py > logs/compute_agent.log 2>&1 &
COMPUTE_PID=$!
echo "  PID: $COMPUTE_PID"

# Iniciar ExecutorAgent
echo "Starting ExecutorAgent (port 8104)..."
nohup python3 agents/executor_agent.py > logs/executor_agent.log 2>&1 &
EXECUTOR_PID=$!
echo "  PID: $EXECUTOR_PID"

echo ""
echo "⏳ Aguardando inicialização dos agents (10 segundos)..."
sleep 10

echo ""
echo "📊 Verificando agents rodando..."
echo "--------------------"
ps aux | grep -E "intake_agent.py|policy_agent.py|compute_agent.py|executor_agent.py" | grep -v grep

echo ""
echo "🏥 TESTANDO HEALTH CHECKS"
echo "=================================="
echo ""

# Health check de cada agent
AGENTS=("IntakeAgent:8101" "PolicyAgent:8102" "ComputeAgent:8103" "ExecutorAgent:8104")
ALL_HEALTHY=true

for agent_info in "${AGENTS[@]}"; do
    AGENT_NAME=$(echo "$agent_info" | cut -d':' -f1)
    AGENT_PORT=$(echo "$agent_info" | cut -d':' -f2)
    
    echo -n "Testing $AGENT_NAME... "
    RESPONSE=$(curl -s http://localhost:$AGENT_PORT/health 2>/dev/null)
    
    if echo "$RESPONSE" | grep -q '"status".*"healthy"' 2>/dev/null; then
        echo "✅ OK"
    else
        echo "❌ FAILED"
        echo "   Response: $RESPONSE"
        ALL_HEALTHY=false
    fi
done

if [ "$ALL_HEALTHY" = false ]; then
    echo ""
    echo "⚠️  Alguns agents não estão saudáveis."
    echo "Verifique os logs:"
    echo "  tail -f logs/*.log"
    exit 1
fi

echo ""
echo "🧪 TESTANDO FLUXO COMPLETO COM TOOLS"
echo "=================================="
echo ""

# Test 1: Request simples
echo "Test 1: Credit Request (sem wallet)"
echo "------------------------------------"
curl -s -X POST "http://localhost:8101/process_credit" \
    -H "Content-Type: application/json" \
    -d '{
        "user_id": "test_user_123",
        "amount": 5000.0,
        "token": "USDC",
        "collateral": "SOL"
    }' | python3 -m json.tool

echo ""
echo ""

# Test 2: Request com wallet address (para tools usarem)
echo "Test 2: Credit Request (com wallet - tools usarão isso)"
echo "--------------------------------------------------------"
curl -s -X POST "http://localhost:8101/process_credit" \
    -H "Content-Type: application/json" \
    -d '{
        "user_id": "11111111111111111111111111111111",
        "amount": 10000.0,
        "token": "USDC",
        "collateral": "SOL"
    }' | python3 -m json.tool

echo ""
echo ""
echo "📜 VERIFICANDO LOGS (últimas 20 linhas de cada agent)"
echo "=================================="
echo ""

echo "--- IntakeAgent Log ---"
tail -n 20 logs/intake_agent.log
echo ""

echo "--- PolicyAgent Log ---"
tail -n 20 logs/policy_agent.log
echo ""

echo "--- ComputeAgent Log (DEVE MOSTRAR TOOLS!) ---"
tail -n 20 logs/compute_agent.log
echo ""

echo "--- ExecutorAgent Log ---"
tail -n 20 logs/executor_agent.log
echo ""

echo "=================================="
echo "✅ TESTE COMPLETO!"
echo ""
echo "💡 Para ver logs em tempo real:"
echo "   tail -f logs/compute_agent.log  # Ver tools em ação"
echo ""
echo "💡 Para parar os agents:"
echo "   pkill -f 'python.*agent.py'"
echo ""


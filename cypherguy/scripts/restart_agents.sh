#!/bin/bash

# Script para reiniciar todos os agents com HTTP endpoints

echo "🔄 Reiniciando Agents com HTTP Communication..."
echo ""

# Para agents antigos
echo "⏹️  Parando agents antigos..."
pkill -f "intake_agent.py"
pkill -f "policy_agent.py"
pkill -f "compute_agent.py"
pkill -f "executor_agent.py"
sleep 2

# Limpar logs antigos (opcional)
# rm -f agents/*.log

echo ""
echo "🚀 Iniciando agents com HTTP endpoints..."
echo ""

# Diretório base
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$BASE_DIR"

# Ativar venv
source ../venv/bin/activate

# Iniciar Intake Agent (porta uAgent: 8001, HTTP: 8101)
echo "📥 Starting IntakeAgent (uAgent:8001, HTTP:8101)..."
nohup python agents/intake_agent.py > logs/intake_agent.log 2>&1 &
INTAKE_PID=$!
echo "   PID: $INTAKE_PID"
sleep 2

# Iniciar Policy Agent (porta uAgent: 8002, HTTP: 8102)
echo "🛡️  Starting PolicyAgent (uAgent:8002, HTTP:8102)..."
nohup python agents/policy_agent.py > logs/policy_agent.log 2>&1 &
POLICY_PID=$!
echo "   PID: $POLICY_PID"
sleep 2

# Iniciar Compute Agent (porta uAgent: 8003, HTTP: 8103)
echo "🧮 Starting ComputeAgent (uAgent:8003, HTTP:8103)..."
nohup python agents/compute_agent.py > logs/compute_agent.log 2>&1 &
COMPUTE_PID=$!
echo "   PID: $COMPUTE_PID"
sleep 2

# Iniciar Executor Agent (porta uAgent: 8004, HTTP: 8104)
echo "⛓️  Starting ExecutorAgent (uAgent:8004, HTTP:8104)..."
nohup python agents/executor_agent.py > logs/executor_agent.log 2>&1 &
EXECUTOR_PID=$!
echo "   PID: $EXECUTOR_PID"
sleep 3

echo ""
echo "✅ Todos os agents foram iniciados!"
echo ""
echo "📊 Verificando status..."
echo ""

# Verificar se os processos estão rodando
ps aux | grep -E "(intake_agent|policy_agent|compute_agent|executor_agent)" | grep -v grep

echo ""
echo "🔍 Para ver logs em tempo real:"
echo "   tail -f logs/intake_agent.log"
echo "   tail -f logs/policy_agent.log"
echo "   tail -f logs/compute_agent.log"
echo "   tail -f logs/executor_agent.log"
echo ""
echo "🧪 Para testar a comunicação:"
echo "   ./scripts/test_agent_comm.sh"
echo ""


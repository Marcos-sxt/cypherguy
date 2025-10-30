#!/bin/bash
# scripts/start_agents.sh - Iniciar todos os agents CypherGuy

echo "🚀 Starting CypherGuy Agents..."
echo "================================"

# Navegar para o diretório correto
cd "$(dirname "$0")/.." || exit

# Verificar se uagents está instalado
if ! python -c "import uagents" 2>/dev/null; then
    echo "❌ ERROR: uagents not installed!"
    echo "Run: pip install uagents"
    exit 1
fi

echo "✅ uagents installed"
echo ""

# Start AgentIntake (port 8001)
echo "🦸 Starting AgentIntake (port 8001)..."
python agents/intake_agent.py &
INTAKE_PID=$!
echo "   PID: $INTAKE_PID"
sleep 3

# Start AgentPolicy (port 8002)
echo "🛡️  Starting AgentPolicy (port 8002)..."
python agents/policy_agent.py &
POLICY_PID=$!
echo "   PID: $POLICY_PID"
sleep 3

# Start AgentCompute (port 8003)
echo "🧮 Starting AgentCompute (port 8003)..."
python agents/compute_agent.py &
COMPUTE_PID=$!
echo "   PID: $COMPUTE_PID"
sleep 3

# Start AgentExecutor (port 8004)
echo "⛓️  Starting AgentExecutor (port 8004)..."
python agents/executor_agent.py &
EXECUTOR_PID=$!
echo "   PID: $EXECUTOR_PID"
sleep 2

echo ""
echo "================================"
echo "🎉 All agents started!"
echo "================================"
echo "Agent PIDs:"
echo "  - AgentIntake:   $INTAKE_PID"
echo "  - AgentPolicy:   $POLICY_PID"
echo "  - AgentCompute:  $COMPUTE_PID"
echo "  - AgentExecutor: $EXECUTOR_PID"
echo ""
echo "Ports:"
echo "  - AgentIntake:   http://localhost:8001"
echo "  - AgentPolicy:   http://localhost:8002"
echo "  - AgentCompute:  http://localhost:8003"
echo "  - AgentExecutor: http://localhost:8004"
echo ""
echo "To stop all agents, run: ./scripts/stop_agents.sh"
echo "To view logs: tail -f ~/.uagents/*/agent.log"
echo ""

# Save PIDs to file for easy stopping
echo "$INTAKE_PID" > /tmp/cypherguy_intake.pid
echo "$POLICY_PID" > /tmp/cypherguy_policy.pid
echo "$COMPUTE_PID" > /tmp/cypherguy_compute.pid
echo "$EXECUTOR_PID" > /tmp/cypherguy_executor.pid

echo "✅ PIDs saved to /tmp/cypherguy_*.pid"
echo ""
echo "Press Ctrl+C to stop monitoring (agents will keep running)"
echo "Monitoring agent output..."
echo "================================"

# Wait for all background processes
wait


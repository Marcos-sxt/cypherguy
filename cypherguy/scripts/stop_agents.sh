#!/bin/bash
# scripts/stop_agents.sh - Parar todos os agents CypherGuy

echo "🛑 Stopping CypherGuy Agents..."
echo "================================"

# Method 1: Kill by PID files
if [ -f /tmp/cypherguy_intake.pid ]; then
    INTAKE_PID=$(cat /tmp/cypherguy_intake.pid)
    echo "Stopping AgentIntake (PID: $INTAKE_PID)..."
    kill -9 "$INTAKE_PID" 2>/dev/null && echo "  ✅ Stopped" || echo "  ⚠️  Already stopped"
    rm /tmp/cypherguy_intake.pid
fi

if [ -f /tmp/cypherguy_policy.pid ]; then
    POLICY_PID=$(cat /tmp/cypherguy_policy.pid)
    echo "Stopping AgentPolicy (PID: $POLICY_PID)..."
    kill -9 "$POLICY_PID" 2>/dev/null && echo "  ✅ Stopped" || echo "  ⚠️  Already stopped"
    rm /tmp/cypherguy_policy.pid
fi

if [ -f /tmp/cypherguy_compute.pid ]; then
    COMPUTE_PID=$(cat /tmp/cypherguy_compute.pid)
    echo "Stopping AgentCompute (PID: $COMPUTE_PID)..."
    kill -9 "$COMPUTE_PID" 2>/dev/null && echo "  ✅ Stopped" || echo "  ⚠️  Already stopped"
    rm /tmp/cypherguy_compute.pid
fi

if [ -f /tmp/cypherguy_executor.pid ]; then
    EXECUTOR_PID=$(cat /tmp/cypherguy_executor.pid)
    echo "Stopping AgentExecutor (PID: $EXECUTOR_PID)..."
    kill -9 "$EXECUTOR_PID" 2>/dev/null && echo "  ✅ Stopped" || echo "  ⚠️  Already stopped"
    rm /tmp/cypherguy_executor.pid
fi

# Method 2: Kill by port (backup)
echo ""
echo "Checking for agents on ports..."
lsof -ti:8001 | xargs kill -9 2>/dev/null && echo "  Port 8001 freed" || echo "  Port 8001 already free"
lsof -ti:8002 | xargs kill -9 2>/dev/null && echo "  Port 8002 freed" || echo "  Port 8002 already free"
lsof -ti:8003 | xargs kill -9 2>/dev/null && echo "  Port 8003 freed" || echo "  Port 8003 already free"
lsof -ti:8004 | xargs kill -9 2>/dev/null && echo "  Port 8004 freed" || echo "  Port 8004 already free"

echo ""
echo "================================"
echo "✅ All agents stopped!"
echo "================================"


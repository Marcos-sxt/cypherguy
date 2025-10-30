#!/bin/bash
# scripts/check_agents.sh - Verificar status dos agents

echo "🔍 Checking CypherGuy Agents Status..."
echo "======================================"
echo ""

# Function to check if process is running
check_process() {
    local name=$1
    local port=$2
    local pid_file=$3
    
    echo -n "🔍 $name (port $port): "
    
    if lsof -i:$port >/dev/null 2>&1; then
        PID=$(lsof -ti:$port)
        echo "✅ RUNNING (PID: $PID)"
        return 0
    else
        echo "❌ NOT RUNNING"
        return 1
    fi
}

# Check all agents
check_process "AgentIntake  " 8001 "/tmp/cypherguy_intake.pid"
check_process "AgentPolicy  " 8002 "/tmp/cypherguy_policy.pid"
check_process "AgentCompute " 8003 "/tmp/cypherguy_compute.pid"
check_process "AgentExecutor" 8004 "/tmp/cypherguy_executor.pid"

echo ""
echo "======================================"

# Check if uagents is installed
echo ""
echo "📦 Checking dependencies..."
if python -c "import uagents" 2>/dev/null; then
    VERSION=$(python -c "import uagents; print(uagents.__version__)" 2>/dev/null)
    echo "✅ uagents installed (version: $VERSION)"
else
    echo "❌ uagents NOT installed"
fi

# Check logs directory
echo ""
echo "📝 Log locations:"
if [ -d ~/.uagents ]; then
    echo "✅ ~/.uagents/ exists"
    ls -la ~/.uagents/ 2>/dev/null | grep "^d" | tail -n +2 | awk '{print "   - " $NF}'
else
    echo "⚠️  No logs directory yet (agents haven't run)"
fi

echo ""
echo "======================================"
echo "💡 Quick commands:"
echo "   Start:   ./scripts/start_agents.sh"
echo "   Stop:    ./scripts/stop_agents.sh"
echo "   Logs:    tail -f ~/.uagents/*/agent.log"
echo "======================================"


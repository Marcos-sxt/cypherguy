#!/bin/bash

# 🧪 CypherGuy - Full System Test
# Tests all components: Agents, Backend API, and connectivity

set -e

echo "🧪 =========================================="
echo "   CypherGuy Full System Test"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test Results
TESTS_PASSED=0
TESTS_FAILED=0

# Helper functions
pass() {
    echo -e "${GREEN}✅ PASS${NC}: $1"
    ((TESTS_PASSED++))
}

fail() {
    echo -e "${RED}❌ FAIL${NC}: $1"
    ((TESTS_FAILED++))
}

info() {
    echo -e "${YELLOW}ℹ️  INFO${NC}: $1"
}

# ========================================
# 1. Check Agents
# ========================================
echo "📍 Test 1: Checking uAgents Status"
echo "-----------------------------------"

check_agent_port() {
    local port=$1
    local name=$2
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        pass "$name is running on port $port"
        return 0
    else
        fail "$name is NOT running on port $port"
        return 1
    fi
}

check_agent_port 8001 "AgentIntake"
check_agent_port 8002 "AgentPolicy"
check_agent_port 8003 "AgentCompute"
check_agent_port 8004 "AgentExecutor"

echo ""

# ========================================
# 2. Check Backend API
# ========================================
echo "📍 Test 2: Checking Backend API"
echo "-----------------------------------"

if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    pass "Backend API is running on port 8000"
    
    # Test root endpoint
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/)
    if [ "$response" -eq 200 ]; then
        pass "Backend root endpoint responds with 200"
    else
        fail "Backend root endpoint returned $response"
    fi
else
    fail "Backend API is NOT running on port 8000"
    info "Start with: cd backend && python main.py"
fi

echo ""

# ========================================
# 3. Test Credit Endpoint
# ========================================
echo "📍 Test 3: Testing Credit Endpoint"
echo "-----------------------------------"

if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    response=$(curl -s -X POST http://localhost:8000/credit \
        -H "Content-Type: application/json" \
        -d '{"user_id": "test_user", "amount": 1000, "token": "USDC", "collateral": 1500}')
    
    if echo "$response" | grep -q "approved"; then
        pass "Credit endpoint responds correctly"
        info "Response: $(echo $response | jq -c '.')"
    else
        fail "Credit endpoint response invalid"
    fi
else
    info "Skipping (backend not running)"
fi

echo ""

# ========================================
# 4. Test RWA Endpoint
# ========================================
echo "📍 Test 4: Testing RWA Endpoint"
echo "-----------------------------------"

if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    response=$(curl -s -X POST http://localhost:8000/rwa \
        -H "Content-Type: application/json" \
        -d '{"user_id": "test_user", "token_id": "RWA-001", "amount": 5000}')
    
    if echo "$response" | grep -q "compliant"; then
        pass "RWA endpoint responds correctly"
        info "Response: $(echo $response | jq -c '.')"
    else
        fail "RWA endpoint response invalid"
    fi
else
    info "Skipping (backend not running)"
fi

echo ""

# ========================================
# 5. Test Trade Endpoint
# ========================================
echo "📍 Test 5: Testing Trade Endpoint"
echo "-----------------------------------"

if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    response=$(curl -s -X POST http://localhost:8000/trade \
        -H "Content-Type: application/json" \
        -d '{"user_id": "test_user", "order_type": "buy", "amount": 0.5, "price": 50000}')
    
    if echo "$response" | grep -q "matched"; then
        pass "Trade endpoint responds correctly"
        info "Response: $(echo $response | jq -c '.')"
    else
        fail "Trade endpoint response invalid"
    fi
else
    info "Skipping (backend not running)"
fi

echo ""

# ========================================
# 6. Test Automation Endpoint
# ========================================
echo "📍 Test 6: Testing Automation Endpoint"
echo "-----------------------------------"

if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    response=$(curl -s -X POST http://localhost:8000/automation \
        -H "Content-Type: application/json" \
        -d '{"user_id": "test_user", "portfolio_value": 10000, "strategy": "yield_farming"}')
    
    if echo "$response" | grep -q "executed"; then
        pass "Automation endpoint responds correctly"
        info "Response: $(echo $response | jq -c '.')"
    else
        fail "Automation endpoint response invalid"
    fi
else
    info "Skipping (backend not running)"
fi

echo ""

# ========================================
# 7. Check Mobile App
# ========================================
echo "📍 Test 7: Checking Mobile App"
echo "-----------------------------------"

if [ -d "mobile" ] && [ -f "mobile/package.json" ]; then
    pass "Mobile app directory exists"
    
    # Check TypeScript compilation
    cd mobile
    if npx tsc --noEmit 2>&1 | grep -q "error"; then
        fail "TypeScript compilation has errors"
    else
        pass "TypeScript compilation successful"
    fi
    cd ..
else
    fail "Mobile app directory not found"
fi

echo ""

# ========================================
# Summary
# ========================================
echo "=========================================="
echo "📊 TEST SUMMARY"
echo "=========================================="
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED!${NC}"
    echo "✅ System is ready for demo!"
    exit 0
else
    echo -e "${RED}⚠️  SOME TESTS FAILED${NC}"
    echo "Please check the failures above."
    echo ""
    echo "Quick fixes:"
    echo "  - Start agents: ./scripts/start_agents.sh"
    echo "  - Start backend: cd backend && python main.py"
    echo "  - Check logs: tail -f ~/.uagents/*/agent.log"
    exit 1
fi


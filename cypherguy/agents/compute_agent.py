"""
AgentCompute - Computação privada (Arcium MPC mockado)
COM TOOLS REAIS para dados blockchain
"""

from uagents import Agent, Context, Model, Protocol
from typing import Dict, Any
import logging
import random
import hashlib
from fastapi import FastAPI
from pydantic import BaseModel as PydanticBaseModel
import uvicorn
import threading
import sys
import os

# Add parent directory to path to import tools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import tools
from tools.base import ToolRegistry
from tools.solana_tools import SolanaRPCTool
from tools.defi_tools import JupiterPriceTool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# TOOLS INITIALIZATION
# ============================================================================

# Initialize tool registry
tools = ToolRegistry()

# Register tools
try:
    tools.register(SolanaRPCTool())
    logger.info("✅ Solana RPC Tool registered")
except Exception as e:
    logger.warning(f"⚠️ Failed to register Solana RPC Tool: {e}")

try:
    tools.register(JupiterPriceTool(fallback_mode=False))  # Use REAL Jupiter API!
    logger.info("✅ Jupiter Price Tool registered (REAL API mode)")
except Exception as e:
    logger.warning(f"⚠️ Failed to register Jupiter Price Tool: {e}")

logger.info(f"🔧 Tools available: {len(tools)} tools")

# FastAPI app para endpoints HTTP
http_app = FastAPI(title="ComputeAgent HTTP API")

# Pydantic models para HTTP endpoints  
class HTTPComputeRequest(PydanticBaseModel):
    user_id: str
    amount: float = None
    token: str = None
    collateral: str = None
    property_value: float = None
    location: str = None
    property_type: str = None
    sell_amount: float = None
    sell_token: str = None
    buy_token: str = None
    portfolio_value: float = None
    strategy: str = None

# ============================================================================
# MESSAGE MODELS
# ============================================================================

class ComputeRequest(Model):
    """Requisição de computação"""
    request_type: str  # credit, rwa, trade, automation
    user_id: str
    data: Dict[str, Any]

class ComputeResponse(Model):
    """Resposta de computação"""
    success: bool
    result: Dict[str, Any]
    computation_hash: str
    mxe_id: str

# ============================================================================
# AGENT DEFINITION
# ============================================================================

compute_agent = Agent(
    name="compute_agent",
    seed="cypherguy_compute_seed_2025_secure",
    port=8003,
    endpoint=["http://localhost:8003/submit"]
)

@compute_agent.on_event("startup")
async def on_startup(ctx: Context):
    """Inicialização do agente"""
    ctx.logger.info(f"🧮 AgentCompute iniciado!")
    ctx.logger.info(f"📍 Address: {compute_agent.address}")
    ctx.logger.info(f"🔐 Arcium MPC (MOCK) ready")

# ============================================================================
# COMPUTE PROTOCOL
# ============================================================================

compute_protocol = Protocol(name="PrivateComputation", version="1.0")

@compute_protocol.on_message(model=ComputeRequest)
async def handle_compute(ctx: Context, sender: str, msg: ComputeRequest):
    """Handle computation requests"""
    ctx.logger.info(f"🔐 Computing (MPC): {msg.request_type}")
    
    # Realizar computação baseada no tipo
    if msg.request_type == "credit":
        result = compute_credit_score(msg.data)
    elif msg.request_type == "rwa":
        result = compute_rwa_validation(msg.data)
    elif msg.request_type == "trade":
        result = compute_order_matching(msg.data)
    elif msg.request_type == "automation":
        result = compute_portfolio_optimization(msg.data)
    else:
        result = {"success": False, "data": {}}
    
    # Gerar hash de computação (proof)
    computation_hash = generate_computation_hash(msg.request_type, msg.data, result)
    
    # Criar resposta
    response = ComputeResponse(
        success=result["success"],
        result=result["data"],
        computation_hash=computation_hash,
        mxe_id=f"mxe_{msg.request_type}_{random.randint(1000, 9999)}"
    )
    
    await ctx.send(sender, response)
    ctx.logger.info(f"✅ Computação concluída: {msg.request_type}")

compute_agent.include(compute_protocol)

# ============================================================================
# COMPUTE FUNCTIONS (Mock Arcium MPC)
# ============================================================================

async def compute_credit_score_with_tools(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computar credit score usando TOOLS REAIS
    Consulta blockchain e preços reais quando disponível
    """
    amount = data.get("amount", 0)
    collateral_type = data.get("collateral", "SOL")
    wallet_address = data.get("wallet_address")  # Optional
    
    logger.info(f"🧮 Computing credit score WITH TOOLS")
    logger.info(f"   Amount: ${amount}")
    logger.info(f"   Collateral: {collateral_type}")
    logger.info(f"   Wallet: {wallet_address or 'Not provided'}")
    
    # Initialize scoring factors
    base_score = 600
    factors = []
    
    # Factor 1: Get collateral price (REAL)
    try:
        price_result = await tools.execute(
            "jupiter_price",
            token=collateral_type
        )
        
        if price_result.get("success"):
            collateral_price = price_result.get("price_usd", 0)
            collateral_value = (amount * 0.5) * collateral_price  # Assuming 50% LTV
            
            logger.info(f"✅ {collateral_type} price: ${collateral_price:.2f} (source: {price_result.get('source')})")
            logger.info(f"✅ Collateral value: ${collateral_value:.2f}")
            
            # Score based on collateral value
            if collateral_value >= amount * 1.5:
                collateral_score = 150
            elif collateral_value >= amount:
                collateral_score = 100
            elif collateral_value >= amount * 0.5:
                collateral_score = 50
            else:
                collateral_score = 0
            
            base_score += collateral_score
            factors.append({
                "factor": "collateral_value",
                "value": collateral_value,
                "score": collateral_score
            })
    except Exception as e:
        logger.warning(f"⚠️ Could not get collateral price: {e}")
    
    # Factor 2: Wallet balance (if wallet provided)
    if wallet_address and tools.has_tool("solana_rpc"):
        try:
            balance_result = await tools.execute(
                "solana_rpc",
                action="get_balance",
                wallet_address=wallet_address
            )
            
            if balance_result.get("success"):
                balance_sol = balance_result.get("balance_sol", 0)
                logger.info(f"✅ Wallet balance: {balance_sol:.4f} SOL")
                
                # Score based on balance
                if balance_sol > 100:
                    balance_score = 100
                elif balance_sol > 10:
                    balance_score = 75
                elif balance_sol > 1:
                    balance_score = 50
                else:
                    balance_score = 25
                
                base_score += balance_score
                factors.append({
                    "factor": "wallet_balance",
                    "value": balance_sol,
                    "score": balance_score
                })
        except Exception as e:
            logger.warning(f"⚠️ Could not get wallet balance: {e}")
    
    # Cap score at 850
    final_score = min(850, base_score)
    
    # Calculate risk level and rates
    if final_score >= 750:
        risk_level = "low"
        rate = 5.5
        max_loan = amount * 1.5
    elif final_score >= 650:
        risk_level = "medium"
        rate = 8.5
        max_loan = amount * 1.2
    else:
        risk_level = "high"
        rate = 12.5
        max_loan = amount
    
    logger.info(f"🎯 Final credit score: {final_score} ({risk_level} risk, {rate}% APR)")
    
    return {
        "success": True,
        "data": {
            "credit_score": round(final_score, 2),
            "interest_rate": rate,
            "max_loan_amount": max_loan,
            "risk_level": risk_level,
            "factors": factors,
            "data_source": "real_tools" if factors else "mock"
        }
    }

def compute_credit_score(data: Dict[str, Any]) -> Dict[str, Any]:
    """Computar credit score usando MPC (MOCK) - Fallback sync version"""
    amount = data.get("amount", 0)
    
    # Mock credit scoring algorithm
    base_score = 700
    amount_factor = min(amount / 10000, 100)
    credit_score = base_score + amount_factor
    
    # Mock interest rate calculation
    if credit_score >= 800:
        rate = 5.5
    elif credit_score >= 700:
        rate = 7.5
    else:
        rate = 10.0
    
    return {
        "success": True,
        "data": {
            "credit_score": round(credit_score, 2),
            "interest_rate": rate,
            "max_loan_amount": amount * 1.2,
            "risk_level": "low" if credit_score >= 750 else "medium",
            "data_source": "mock"
        }
    }

def compute_rwa_validation(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validar RWA compliance usando MPC (MOCK)"""
    property_value = data.get("property_value", 0)
    
    # Mock validation
    compliance_score = 85 + random.randint(0, 15)
    
    return {
        "success": True,
        "data": {
            "compliance_score": compliance_score,
            "validated": compliance_score >= 75,
            "token_supply": int(property_value / 100),
            "fractional_ownership": True
        }
    }

def compute_order_matching(data: Dict[str, Any]) -> Dict[str, Any]:
    """Match orders in dark pool usando MPC (MOCK)"""
    sell_amount = data.get("sell_amount", 0)
    sell_token = data.get("sell_token", "")
    
    # Mock price discovery
    base_price = 95.0 if sell_token == "SOL" else 1.0
    price_variation = random.uniform(-2.0, 2.0)
    match_price = base_price + price_variation
    
    return {
        "success": True,
        "data": {
            "matched": True,
            "match_price": round(match_price, 2),
            "counterparty_id": f"counterparty_{random.randint(1000, 9999)}",
            "execution_time": "2s",
            "privacy_preserved": True
        }
    }

def compute_portfolio_optimization(data: Dict[str, Any]) -> Dict[str, Any]:
    """Otimizar portfolio usando MPC (MOCK)"""
    strategy = data.get("strategy", "yield_farming")
    
    # Mock optimization algorithm
    if strategy == "yield_farming":
        allocation = {
            "SOL_lending": 0.4,
            "USDC_lending": 0.3,
            "LP_providing": 0.2,
            "Staking": 0.1
        }
        expected_apy = 12.5
    else:
        allocation = {
            "SOL": 0.5,
            "USDC": 0.3,
            "BTC": 0.1,
            "ETH": 0.1
        }
        expected_apy = 8.0
    
    return {
        "success": True,
        "data": {
            "optimal_allocation": allocation,
            "expected_apy": expected_apy,
            "rebalance_needed": True,
            "estimated_gas": 0.002
        }
    }

def generate_computation_hash(request_type: str, data: dict, result: dict) -> str:
    """Gerar hash proof da computação"""
    content = f"{request_type}_{data}_{result}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]

# ============================================================================
# HTTP ENDPOINTS (Para comunicação entre agents)
# ============================================================================

@http_app.post("/compute_credit")
async def http_compute_credit(request: HTTPComputeRequest):
    """Compute credit score and forward to executor - NOW WITH REAL TOOLS!"""
    logger.info(f"🧮 HTTP: Computing credit for {request.user_id}: ${request.amount}")
    
    # Usar computação COM TOOLS REAIS
    try:
        compute_result = await compute_credit_score_with_tools({
            "amount": request.amount,
            "collateral": request.collateral,
            "wallet_address": request.user_id if request.user_id.startswith("agent") == False else None  # Use user_id as wallet if it's not an agent address
        })
        logger.info(f"✅ Computation complete WITH TOOLS: score={compute_result['data']['credit_score']}, rate={compute_result['data']['interest_rate']}%")
        logger.info(f"📊 Data source: {compute_result['data'].get('data_source', 'unknown')}")
    except Exception as e:
        logger.warning(f"⚠️ Error using tools, falling back to mock: {e}")
        # Fallback para versão mock se tools falharem
        compute_result = compute_credit_score({
            "amount": request.amount,
            "collateral": request.collateral
        })
        logger.info(f"✅ Computation complete (FALLBACK): score={compute_result['data']['credit_score']}, rate={compute_result['data']['interest_rate']}%")
    
    # Enviar para executor agent via HTTP
    import aiohttp
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:8104/execute_credit",
                json={
                    "user_id": request.user_id,
                    "amount": request.amount,
                    "token": request.token,
                    "collateral": request.collateral,
                    "credit_score": compute_result['data']['credit_score'],
                    "interest_rate": compute_result['data']['interest_rate']
                }
            ) as response:
                executor_result = await response.json()
                logger.info(f"✅ Executor response: {executor_result}")
                return executor_result
    except Exception as e:
        logger.error(f"❌ Error calling executor agent: {e}")
        return {
            "success": False,
            "approved": False,
            "message": f"Execution failed: {str(e)}"
        }

@http_app.post("/compute_rwa")
async def http_compute_rwa(request: HTTPComputeRequest):
    """Compute RWA token parameters and forward to executor"""
    logger.info(f"🧮 HTTP: Computing RWA for {request.user_id}: ${request.property_value}")
    
    compute_result = compute_rwa_compliance({
        "property_value": request.property_value,
        "location": request.location,
        "property_type": request.property_type
    })
    
    logger.info(f"✅ Computation complete: compliance_score={compute_result['data']['compliance_score']}")
    
    import aiohttp
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:8104/execute_rwa",
                json={
                    "user_id": request.user_id,
                    "property_value": request.property_value,
                    "location": request.location,
                    "property_type": request.property_type,
                    "token_supply": compute_result['data']['token_supply'],
                    "compliance_score": compute_result['data']['compliance_score']
                }
            ) as response:
                executor_result = await response.json()
                logger.info(f"✅ Executor response: {executor_result}")
                return executor_result
    except Exception as e:
        logger.error(f"❌ Error calling executor agent: {e}")
        return {
            "success": False,
            "approved": False,
            "message": f"Execution failed: {str(e)}"
        }

@http_app.post("/compute_trade")
async def http_compute_trade(request: HTTPComputeRequest):
    """Compute trade match and forward to executor"""
    logger.info(f"🧮 HTTP: Computing trade for {request.user_id}: {request.sell_amount} {request.sell_token}")
    
    compute_result = compute_trade_match({
        "sell_amount": request.sell_amount,
        "sell_token": request.sell_token,
        "buy_token": request.buy_token
    })
    
    logger.info(f"✅ Computation complete: match_price=${compute_result['data']['match_price']}")
    
    import aiohttp
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:8104/execute_trade",
                json={
                    "user_id": request.user_id,
                    "sell_amount": request.sell_amount,
                    "sell_token": request.sell_token,
                    "buy_token": request.buy_token,
                    "match_price": compute_result['data']['match_price'],
                    "counterparty": compute_result['data']['counterparty']
                }
            ) as response:
                executor_result = await response.json()
                logger.info(f"✅ Executor response: {executor_result}")
                return executor_result
    except Exception as e:
        logger.error(f"❌ Error calling executor agent: {e}")
        return {
            "success": False,
            "matched": False,
            "message": f"Execution failed: {str(e)}"
        }

@http_app.post("/compute_automation")
async def http_compute_automation(request: HTTPComputeRequest):
    """Compute portfolio optimization and forward to executor"""
    logger.info(f"🧮 HTTP: Computing automation for {request.user_id}: {request.strategy}")
    
    compute_result = compute_portfolio_optimization({
        "portfolio_value": request.portfolio_value,
        "strategy": request.strategy
    })
    
    logger.info(f"✅ Computation complete: expected_apy={compute_result['data']['expected_apy']}%")
    
    import aiohttp
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:8104/execute_automation",
                json={
                    "user_id": request.user_id,
                    "portfolio_value": request.portfolio_value,
                    "strategy": request.strategy,
                    "optimal_allocation": compute_result['data']['optimal_allocation'],
                    "expected_apy": compute_result['data']['expected_apy']
                }
            ) as response:
                executor_result = await response.json()
                logger.info(f"✅ Executor response: {executor_result}")
                return executor_result
    except Exception as e:
        logger.error(f"❌ Error calling executor agent: {e}")
        return {
            "success": False,
            "approved": False,
            "message": f"Execution failed: {str(e)}"
        }

@http_app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "agent": "compute"}

# ============================================================================
# RUN AGENT + HTTP SERVER
# ============================================================================

def run_http_server():
    """Rodar HTTP server em thread separada"""
    uvicorn.run(http_app, host="0.0.0.0", port=8103, log_level="info")

if __name__ == "__main__":
    logger.info("🧮 Starting AgentCompute...")
    logger.info("🌐 HTTP server will run on port 8103")
    
    # Iniciar HTTP server em thread
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()
    
    # Rodar uAgent
    compute_agent.run()


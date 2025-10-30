"""
AgentPolicy - Validação de regras usando MeTTa-inspired logic
Para MVP: Rules em Python, depois migrar para hyperon
"""

from uagents import Agent, Context, Model, Protocol
from typing import Dict, Any, List, Optional
import logging
import sys
import os
from fastapi import FastAPI
from pydantic import BaseModel as PydanticBaseModel
import uvicorn
import threading

# Add parent directory to path to import metta
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import MeTTa engine (with fallback)
try:
    from metta.meetta_engine import MeTTaEngine
    METTA_AVAILABLE = True
except ImportError:
    METTA_AVAILABLE = False
    MeTTaEngine = None
    logging.warning("⚠️ MeTTa engine not available")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MeTTa Engine (global)
metta_engine: Optional[MeTTaEngine] = None

# FastAPI app para endpoints HTTP
http_app = FastAPI(title="PolicyAgent HTTP API")

# Pydantic models para HTTP endpoints
class HTTPPolicyRequest(PydanticBaseModel):
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

class PolicyCheckRequest(Model):
    """Requisição de checagem de política"""
    request_type: str  # credit, rwa, trade, automation
    user_id: str
    data: Dict[str, Any]

class PolicyCheckResponse(Model):
    """Resposta de checagem de política"""
    approved: bool
    reason: str
    rules_applied: List[str]

# ============================================================================
# POLICY RULES (MeTTa-inspired em Python para MVP)
# ============================================================================

class PolicyRules:
    """
    Regras de política inspiradas em MeTTa
    TODO: Migrar para hyperon quando estável
    """
    
    CREDIT_RULES = {
        "max_amount": 100000,
        "min_amount": 100,
        "max_ltv": 0.8,
        "min_collateral_ratio": 1.5
    }
    
    RWA_RULES = {
        "min_property_value": 50000,
        "allowed_locations": ["USA", "New York", "California", "Texas", "Florida"],
        "allowed_types": ["Residential", "Commercial", "Industrial"]
    }
    
    TRADE_RULES = {
        "max_trade_amount": 1000000,
        "min_trade_amount": 10,
        "allowed_tokens": ["SOL", "USDC", "USDT", "BTC", "ETH", "BONK"]
    }
    
    AUTOMATION_RULES = {
        "min_portfolio_value": 1000,
        "allowed_strategies": ["yield_farming", "portfolio_optimization", "hedging"]
    }
    
    @staticmethod
    def evaluate_credit(data: Dict[str, Any]) -> Dict[str, Any]:
        """Avaliar regras de crédito"""
        amount = data.get("amount", 0)
        collateral = data.get("collateral_value", 0)
        
        # Regra 1: Valor mínimo
        if amount < PolicyRules.CREDIT_RULES["min_amount"]:
            return {
                "approved": False,
                "reason": f"Amount below minimum: ${PolicyRules.CREDIT_RULES['min_amount']}",
                "rules_applied": ["min_amount"]
            }
        
        # Regra 2: Valor máximo
        if amount > PolicyRules.CREDIT_RULES["max_amount"]:
            return {
                "approved": False,
                "reason": f"Amount exceeds maximum: ${PolicyRules.CREDIT_RULES['max_amount']}",
                "rules_applied": ["max_amount"]
            }
        
        # Regra 3: Ratio de colateral
        if collateral > 0:
            ratio = collateral / amount
            if ratio < PolicyRules.CREDIT_RULES["min_collateral_ratio"]:
                return {
                    "approved": False,
                    "reason": f"Insufficient collateral ratio: {ratio:.2f}x (min: {PolicyRules.CREDIT_RULES['min_collateral_ratio']}x)",
                    "rules_applied": ["min_collateral_ratio"]
                }
        
        return {
            "approved": True,
            "reason": "All credit rules passed",
            "rules_applied": ["min_amount", "max_amount", "min_collateral_ratio"]
        }
    
    @staticmethod
    def evaluate_rwa(data: Dict[str, Any]) -> Dict[str, Any]:
        """Avaliar regras de RWA"""
        property_value = data.get("property_value", 0)
        location = data.get("location", "")
        property_type = data.get("property_type", "")
        
        # Regra 1: Valor mínimo
        if property_value < PolicyRules.RWA_RULES["min_property_value"]:
            return {
                "approved": False,
                "reason": f"Property value below minimum: ${PolicyRules.RWA_RULES['min_property_value']}",
                "rules_applied": ["min_property_value"]
            }
        
        # Regra 2: Localização permitida
        location_valid = any(allowed in location for allowed in PolicyRules.RWA_RULES["allowed_locations"])
        if not location_valid:
            return {
                "approved": False,
                "reason": f"Location not supported: {location}",
                "rules_applied": ["allowed_locations"]
            }
        
        # Regra 3: Tipo permitido
        if property_type not in PolicyRules.RWA_RULES["allowed_types"]:
            return {
                "approved": False,
                "reason": f"Property type not supported: {property_type}",
                "rules_applied": ["allowed_types"]
            }
        
        return {
            "approved": True,
            "reason": "All RWA rules passed",
            "rules_applied": ["min_property_value", "allowed_locations", "allowed_types"]
        }
    
    @staticmethod
    def evaluate_trade(data: Dict[str, Any]) -> Dict[str, Any]:
        """Avaliar regras de trading"""
        sell_amount = data.get("sell_amount", 0)
        sell_token = data.get("sell_token", "")
        buy_token = data.get("buy_token", "")
        
        # Regra 1: Valor mínimo
        if sell_amount < PolicyRules.TRADE_RULES["min_trade_amount"]:
            return {
                "approved": False,
                "reason": f"Trade amount below minimum: ${PolicyRules.TRADE_RULES['min_trade_amount']}",
                "rules_applied": ["min_trade_amount"]
            }
        
        # Regra 2: Valor máximo
        if sell_amount > PolicyRules.TRADE_RULES["max_trade_amount"]:
            return {
                "approved": False,
                "reason": f"Trade amount exceeds maximum: ${PolicyRules.TRADE_RULES['max_trade_amount']}",
                "rules_applied": ["max_trade_amount"]
            }
        
        # Regra 3: Tokens permitidos
        if sell_token not in PolicyRules.TRADE_RULES["allowed_tokens"] or buy_token not in PolicyRules.TRADE_RULES["allowed_tokens"]:
            return {
                "approved": False,
                "reason": f"Token not supported: {sell_token} or {buy_token}",
                "rules_applied": ["allowed_tokens"]
            }
        
        return {
            "approved": True,
            "reason": "All trading rules passed",
            "rules_applied": ["min_trade_amount", "max_trade_amount", "allowed_tokens"]
        }
    
    @staticmethod
    def evaluate_automation(data: Dict[str, Any]) -> Dict[str, Any]:
        """Avaliar regras de automação"""
        portfolio_value = data.get("portfolio_value", 0)
        strategy = data.get("strategy", "")
        
        # Regra 1: Valor mínimo de portfólio
        if portfolio_value < PolicyRules.AUTOMATION_RULES["min_portfolio_value"]:
            return {
                "approved": False,
                "reason": f"Portfolio value below minimum: ${PolicyRules.AUTOMATION_RULES['min_portfolio_value']}",
                "rules_applied": ["min_portfolio_value"]
            }
        
        # Regra 2: Estratégia permitida
        if strategy not in PolicyRules.AUTOMATION_RULES["allowed_strategies"]:
            return {
                "approved": False,
                "reason": f"Strategy not supported: {strategy}",
                "rules_applied": ["allowed_strategies"]
            }
        
        return {
            "approved": True,
            "reason": "All automation rules passed",
            "rules_applied": ["min_portfolio_value", "allowed_strategies"]
        }

# ============================================================================
# AGENT DEFINITION
# ============================================================================

policy_agent = Agent(
    name="policy_agent",
    seed="cypherguy_policy_seed_2025_secure",
    port=8002,
    endpoint=["http://localhost:8002/submit"]
)

@policy_agent.on_event("startup")
async def on_startup(ctx: Context):
    """Inicialização do agente"""
    global metta_engine
    
    ctx.logger.info(f"🛡️ AgentPolicy iniciado!")
    ctx.logger.info(f"📍 Address: {policy_agent.address}")
    
    # Inicializar MeTTa engine
    if METTA_AVAILABLE:
        rules_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "metta",
            "policy_rules.metta"
        )
        
        metta_engine = MeTTaEngine(rules_file=rules_file if os.path.exists(rules_file) else None)
        
        if metta_engine.available:
            ctx.logger.info("✅ MeTTa engine ready! (hyperon-py)")
        else:
            ctx.logger.info("ℹ️ MeTTa engine using Python fallback (fully functional)")
    else:
        ctx.logger.info("ℹ️ MeTTa engine not available - using PolicyRules directly")
    
    ctx.logger.info(f"📋 Rules loaded: credit, rwa, trade, automation")

# ============================================================================
# POLICY PROTOCOL
# ============================================================================

policy_protocol = Protocol(name="PolicyCheck", version="1.0")

@policy_protocol.on_message(model=PolicyCheckRequest)
async def handle_policy_check(ctx: Context, sender: str, msg: PolicyCheckRequest):
    """Handle policy check requests"""
    ctx.logger.info(f"🔍 Policy check: {msg.request_type} for {msg.user_id}")
    
    # Avaliar baseado no tipo (usar MeTTa se disponível)
    if msg.request_type == "credit":
        if metta_engine:
            result = metta_engine.evaluate_credit(
                amount=msg.data.get("amount", 0),
                collateral=msg.data.get("collateral_value", 0)
            )
        else:
            result = PolicyRules.evaluate_credit(msg.data)
    elif msg.request_type == "rwa":
        if metta_engine:
            result = metta_engine.evaluate_rwa(
                property_value=msg.data.get("property_value", 0),
                location=msg.data.get("location", ""),
                property_type=msg.data.get("property_type", "")
            )
        else:
            result = PolicyRules.evaluate_rwa(msg.data)
    elif msg.request_type == "trade":
        result = PolicyRules.evaluate_trade(msg.data)  # MeTTa não implementado ainda
    elif msg.request_type == "automation":
        result = PolicyRules.evaluate_automation(msg.data)  # MeTTa não implementado ainda
    else:
        result = {
            "approved": False,
            "reason": f"Unknown request type: {msg.request_type}",
            "rules_applied": []
        }
    
    # Criar resposta
    response = PolicyCheckResponse(
        approved=result["approved"],
        reason=result["reason"],
        rules_applied=result["rules_applied"]
    )
    
    # Enviar resposta
    await ctx.send(sender, response)
    
    status = "✅ APPROVED" if result["approved"] else "❌ REJECTED"
    ctx.logger.info(f"{status}: {msg.request_type} - {result['reason']}")

policy_agent.include(policy_protocol)

# ============================================================================
# HTTP ENDPOINTS (Para comunicação entre agents)
# ============================================================================

@http_app.post("/check_credit_policy")
async def http_check_credit_policy(request: HTTPPolicyRequest):
    """Check credit policy and forward to compute agent"""
    logger.info(f"🛡️ HTTP: Checking credit policy for {request.user_id}: ${request.amount}")
    
    # Validar política usando método estático
    policy_result = PolicyRules.evaluate_credit({
        "amount": request.amount,
        "collateral_value": 0  # Will be calculated by compute agent
    })
    
    if not policy_result["approved"]:
        logger.warning(f"❌ Policy REJECTED: {policy_result['reason']}")
        return {
            "success": False,
            "approved": False,
            "message": policy_result["reason"]
        }
    
    logger.info(f"✅ Policy APPROVED: {policy_result['reason']}")
    
    # Enviar para compute agent via HTTP
    import aiohttp
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:8103/compute_credit",
                json={
                    "user_id": request.user_id,
                    "amount": request.amount,
                    "token": request.token,
                    "collateral": request.collateral
                }
            ) as response:
                compute_result = await response.json()
                logger.info(f"✅ Compute response: {compute_result}")
                return compute_result
    except Exception as e:
        logger.error(f"❌ Error calling compute agent: {e}")
        return {
            "success": False,
            "approved": False,
            "message": f"Compute failed: {str(e)}"
        }

@http_app.post("/check_rwa_policy")
async def http_check_rwa_policy(request: HTTPPolicyRequest):
    """Check RWA policy and forward to compute agent"""
    logger.info(f"🛡️ HTTP: Checking RWA policy for {request.user_id}: ${request.property_value}")
    
    rules = PolicyRules()
    policy_result = rules.check_rwa_policy({
        "property_value": request.property_value,
        "location": request.location,
        "property_type": request.property_type
    })
    
    if not policy_result["approved"]:
        logger.warning(f"❌ Policy REJECTED: {policy_result['reason']}")
        return {
            "success": False,
            "approved": False,
            "message": policy_result["reason"]
        }
    
    logger.info(f"✅ Policy APPROVED: {policy_result['reason']}")
    
    import aiohttp
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:8103/compute_rwa",
                json={
                    "user_id": request.user_id,
                    "property_value": request.property_value,
                    "location": request.location,
                    "property_type": request.property_type
                }
            ) as response:
                compute_result = await response.json()
                logger.info(f"✅ Compute response: {compute_result}")
                return compute_result
    except Exception as e:
        logger.error(f"❌ Error calling compute agent: {e}")
        return {
            "success": False,
            "approved": False,
            "message": f"Compute failed: {str(e)}"
        }

@http_app.post("/check_trade_policy")
async def http_check_trade_policy(request: HTTPPolicyRequest):
    """Check trade policy and forward to compute agent"""
    logger.info(f"🛡️ HTTP: Checking trade policy for {request.user_id}: {request.sell_amount} {request.sell_token}")
    
    rules = PolicyRules()
    policy_result = rules.check_trade_policy({
        "sell_amount": request.sell_amount,
        "sell_token": request.sell_token,
        "buy_token": request.buy_token
    })
    
    if not policy_result["approved"]:
        logger.warning(f"❌ Policy REJECTED: {policy_result['reason']}")
        return {
            "success": False,
            "matched": False,
            "message": policy_result["reason"]
        }
    
    logger.info(f"✅ Policy APPROVED: {policy_result['reason']}")
    
    import aiohttp
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:8103/compute_trade",
                json={
                    "user_id": request.user_id,
                    "sell_amount": request.sell_amount,
                    "sell_token": request.sell_token,
                    "buy_token": request.buy_token
                }
            ) as response:
                compute_result = await response.json()
                logger.info(f"✅ Compute response: {compute_result}")
                return compute_result
    except Exception as e:
        logger.error(f"❌ Error calling compute agent: {e}")
        return {
            "success": False,
            "matched": False,
            "message": f"Compute failed: {str(e)}"
        }

@http_app.post("/check_automation_policy")
async def http_check_automation_policy(request: HTTPPolicyRequest):
    """Check automation policy and forward to compute agent"""
    logger.info(f"🛡️ HTTP: Checking automation policy for {request.user_id}: {request.strategy}")
    
    rules = PolicyRules()
    policy_result = rules.check_automation_policy({
        "portfolio_value": request.portfolio_value,
        "strategy": request.strategy
    })
    
    if not policy_result["approved"]:
        logger.warning(f"❌ Policy REJECTED: {policy_result['reason']}")
        return {
            "success": False,
            "approved": False,
            "message": policy_result["reason"]
        }
    
    logger.info(f"✅ Policy APPROVED: {policy_result['reason']}")
    
    import aiohttp
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:8103/compute_automation",
                json={
                    "user_id": request.user_id,
                    "portfolio_value": request.portfolio_value,
                    "strategy": request.strategy
                }
            ) as response:
                compute_result = await response.json()
                logger.info(f"✅ Compute response: {compute_result}")
                return compute_result
    except Exception as e:
        logger.error(f"❌ Error calling compute agent: {e}")
        return {
            "success": False,
            "approved": False,
            "message": f"Compute failed: {str(e)}"
        }

@http_app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "agent": "policy"}

# ============================================================================
# RUN AGENT + HTTP SERVER
# ============================================================================

def run_http_server():
    """Rodar HTTP server em thread separada"""
    uvicorn.run(http_app, host="0.0.0.0", port=8102, log_level="info")

if __name__ == "__main__":
    logger.info("🛡️ Starting AgentPolicy...")
    logger.info("🌐 HTTP server will run on port 8102")
    
    # Iniciar HTTP server em thread
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()
    
    # Rodar uAgent
    policy_agent.run()


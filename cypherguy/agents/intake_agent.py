"""
AgentIntake - Responsável por autenticação e parsing de requisições
Usa uAgents SDK oficial da Fetch.ai
WITH ASI:One Chat Protocol Support
"""

from uagents import Agent, Context, Model, Protocol
from typing import Dict, Any, Optional
import asyncio
import logging
import hashlib
import time
import re
from datetime import datetime, timezone
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel as PydanticBaseModel
import uvicorn
import threading
import os
import httpx
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ASI:One Chat Protocol imports
try:
    from uagents_core.contrib.protocols.chat import (
        ChatMessage,
        ChatAcknowledgement,
        StartSessionContent,
        TextContent,
        EndSessionContent,
        chat_protocol_spec,
    )
    CHAT_AVAILABLE = True
except ImportError:
    logger.warning("⚠️ Chat protocol not available - install uagents_core")
    CHAT_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app para endpoints HTTP
http_app = FastAPI(title="IntakeAgent HTTP API")

# Pydantic models para HTTP endpoints
class HTTPCreditRequest(PydanticBaseModel):
    user_id: str
    amount: float
    token: str
    collateral: str

class HTTPRWARequest(PydanticBaseModel):
    user_id: str
    property_value: float
    location: str
    property_type: str

class HTTPTradeRequest(PydanticBaseModel):
    user_id: str
    sell_amount: float
    sell_token: str
    buy_token: str

class HTTPAutomationRequest(PydanticBaseModel):
    user_id: str
    portfolio_value: float
    strategy: str

# ============================================================================
# MESSAGE MODELS (Pydantic para type safety)
# ============================================================================

class AuthRequest(Model):
    """Requisição de autenticação"""
    user_id: str
    wallet_address: str
    signature: str
    timestamp: int

class AuthResponse(Model):
    """Resposta de autenticação"""
    success: bool
    user_id: str
    session_token: str
    message: str

class CreditRequest(Model):
    """Requisição de crédito"""
    user_id: str
    amount: float
    token: str
    collateral: str
    session_token: str

class RWARequest(Model):
    """Requisição de tokenização RWA"""
    user_id: str
    property_value: float
    location: str
    property_type: str
    session_token: str

class TradeRequest(Model):
    """Requisição de trade"""
    user_id: str
    sell_amount: float
    sell_token: str
    buy_token: str
    session_token: str

class AutomationRequest(Model):
    """Requisição de automação"""
    user_id: str
    portfolio_value: float
    strategy: str
    session_token: str

# ============================================================================
# AGENT DEFINITION
# ============================================================================

# Criar AgentIntake
# Note: mailbox=True requires removing explicit endpoint (Agentverse handles routing)
intake_agent = Agent(
    name="intake_agent",
    seed="cypherguy_intake_seed_2025_secure",  # TODO: Move to env var
    port=8001,
    # endpoint=["http://localhost:8001/submit"],  # Removed: conflicts with mailbox=True
    mailbox=True  # Connect to Agentverse Mailbox for public discovery
)

# Storage para sessões e contexto de chat
@intake_agent.on_event("startup")
async def on_startup(ctx: Context):
    """Inicialização do agente"""
    ctx.logger.info(f"🚀 AgentIntake iniciado!")
    ctx.logger.info(f"📍 Address: {intake_agent.address}")
    ctx.logger.info(f"🔗 Endpoint: {intake_agent._endpoints}")
    
    # Inicializar storage
    # Chat context: armazena estado da conversa por usuário (sender address)
    chat_context = ctx.storage.get("chat_context") or {}
    ctx.storage.set("chat_context", chat_context)
    if not ctx.storage.get("sessions"):
        ctx.storage.set("sessions", {})
    
    if not ctx.storage.get("requests_count"):
        ctx.storage.set("requests_count", 0)

# ============================================================================
# AUTHENTICATION PROTOCOL
# ============================================================================

auth_protocol = Protocol(name="Authentication", version="1.0")

@auth_protocol.on_message(model=AuthRequest)
async def handle_auth(ctx: Context, sender: str, msg: AuthRequest):
    """Handle authentication requests"""
    ctx.logger.info(f"🔐 Auth request from {msg.user_id}")
    
    # Validar assinatura (simplificado para MVP)
    is_valid = len(msg.wallet_address) >= 32 and len(msg.signature) > 0
    
    if is_valid:
        # Gerar session token
        session_data = f"{msg.user_id}_{msg.wallet_address}_{time.time()}"
        session_token = hashlib.sha256(session_data.encode()).hexdigest()
        
        # Armazenar sessão
        sessions = ctx.storage.get("sessions") or {}
        sessions[session_token] = {
            "user_id": msg.user_id,
            "wallet_address": msg.wallet_address,
            "created_at": time.time()
        }
        ctx.storage.set("sessions", sessions)
        
        # Enviar resposta
        response = AuthResponse(
            success=True,
            user_id=msg.user_id,
            session_token=session_token,
            message="Authentication successful"
        )
    else:
        response = AuthResponse(
            success=False,
            user_id=msg.user_id,
            session_token="",
            message="Invalid signature"
        )
    
    await ctx.send(sender, response)
    ctx.logger.info(f"✅ Auth {'successful' if is_valid else 'failed'}: {msg.user_id}")

# Incluir protocol no agent
intake_agent.include(auth_protocol)

# ============================================================================
# CREDIT PROTOCOL
# ============================================================================

credit_protocol = Protocol(name="CreditIntake", version="1.0")

@credit_protocol.on_message(model=CreditRequest)
async def handle_credit_request(ctx: Context, sender: str, msg: CreditRequest):
    """Handle credit requests"""
    ctx.logger.info(f"💳 Credit request from {msg.user_id}: ${msg.amount}")
    
    # Validar sessão
    sessions = ctx.storage.get("sessions") or {}
    if msg.session_token not in sessions:
        ctx.logger.error(f"❌ Invalid session token")
        return
    
    # Incrementar contador
    count = ctx.storage.get("requests_count") or 0
    ctx.storage.set("requests_count", count + 1)
    
    # Validar request
    if msg.amount <= 0:
        ctx.logger.error(f"❌ Invalid amount: {msg.amount}")
        return
    
    # Armazenar request
    request_id = f"credit_{count + 1}"
    requests = ctx.storage.get("credit_requests") or {}
    requests[request_id] = {
        "user_id": msg.user_id,
        "amount": msg.amount,
        "token": msg.token,
        "collateral": msg.collateral,
        "status": "pending",
        "timestamp": time.time()
    }
    ctx.storage.set("credit_requests", requests)
    
    ctx.logger.info(f"📝 Credit request stored: {request_id}")
    
    # TODO: Enviar para PolicyAgent
    # POLICY_AGENT_ADDRESS = "agent1qpolicy..."
    # await ctx.send(POLICY_AGENT_ADDRESS, PolicyCheckRequest(...))

intake_agent.include(credit_protocol)

# ============================================================================
# RWA PROTOCOL
# ============================================================================

rwa_protocol = Protocol(name="RWAIntake", version="1.0")

@rwa_protocol.on_message(model=RWARequest)
async def handle_rwa_request(ctx: Context, sender: str, msg: RWARequest):
    """Handle RWA tokenization requests"""
    ctx.logger.info(f"🏢 RWA request from {msg.user_id}: ${msg.property_value}")
    
    # Validar sessão
    sessions = ctx.storage.get("sessions") or {}
    if msg.session_token not in sessions:
        ctx.logger.error(f"❌ Invalid session token")
        return
    
    # Incrementar contador
    count = ctx.storage.get("requests_count") or 0
    ctx.storage.set("requests_count", count + 1)
    
    # Armazenar request
    request_id = f"rwa_{count + 1}"
    requests = ctx.storage.get("rwa_requests") or {}
    requests[request_id] = {
        "user_id": msg.user_id,
        "property_value": msg.property_value,
        "location": msg.location,
        "property_type": msg.property_type,
        "status": "pending",
        "timestamp": time.time()
    }
    ctx.storage.set("rwa_requests", requests)
    
    ctx.logger.info(f"📝 RWA request stored: {request_id}")

intake_agent.include(rwa_protocol)

# ============================================================================
# TRADING PROTOCOL
# ============================================================================

trading_protocol = Protocol(name="TradingIntake", version="1.0")

@trading_protocol.on_message(model=TradeRequest)
async def handle_trade_request(ctx: Context, sender: str, msg: TradeRequest):
    """Handle trading requests"""
    ctx.logger.info(f"🌑 Trade request from {msg.user_id}: {msg.sell_amount} {msg.sell_token}")
    
    # Validar sessão
    sessions = ctx.storage.get("sessions") or {}
    if msg.session_token not in sessions:
        ctx.logger.error(f"❌ Invalid session token")
        return
    
    # Incrementar contador
    count = ctx.storage.get("requests_count") or 0
    ctx.storage.set("requests_count", count + 1)
    
    # Armazenar request
    request_id = f"trade_{count + 1}"
    requests = ctx.storage.get("trade_requests") or {}
    requests[request_id] = {
        "user_id": msg.user_id,
        "sell_amount": msg.sell_amount,
        "sell_token": msg.sell_token,
        "buy_token": msg.buy_token,
        "status": "pending",
        "timestamp": time.time()
    }
    ctx.storage.set("trade_requests", requests)
    
    ctx.logger.info(f"📝 Trade request stored: {request_id}")

intake_agent.include(trading_protocol)

# ============================================================================
# AUTOMATION PROTOCOL
# ============================================================================

automation_protocol = Protocol(name="AutomationIntake", version="1.0")

@automation_protocol.on_message(model=AutomationRequest)
async def handle_automation_request(ctx: Context, sender: str, msg: AutomationRequest):
    """Handle automation requests"""
    ctx.logger.info(f"🤖 Automation request from {msg.user_id}: {msg.strategy}")
    
    # Validar sessão
    sessions = ctx.storage.get("sessions") or {}
    if msg.session_token not in sessions:
        ctx.logger.error(f"❌ Invalid session token")
        return
    
    # Incrementar contador
    count = ctx.storage.get("requests_count") or 0
    ctx.storage.set("requests_count", count + 1)
    
    # Armazenar request
    request_id = f"automation_{count + 1}"
    requests = ctx.storage.get("automation_requests") or {}
    requests[request_id] = {
        "user_id": msg.user_id,
        "portfolio_value": msg.portfolio_value,
        "strategy": msg.strategy,
        "status": "pending",
        "timestamp": time.time()
    }
    ctx.storage.set("automation_requests", requests)
    
    ctx.logger.info(f"📝 Automation request stored: {request_id}")

intake_agent.include(automation_protocol)

# ============================================================================
# HTTP ENDPOINTS (Para comunicação do backend)
# ============================================================================

# Storage compartilhado entre HTTP e uAgent
http_responses = {}

@http_app.post("/process_credit")
async def http_process_credit(request: HTTPCreditRequest):
    """
    HTTP endpoint para processar requisições de crédito
    Este endpoint recebe do backend e encaminha para policy agent
    """
    logger.info(f"🔵 HTTP: Credit request from {request.user_id}: ${request.amount}")
    
    # Validações básicas
    if request.amount < 100 or request.amount > 100000:
        return {
            "success": False,
            "approved": False,
            "message": "Amount must be between $100 and $100,000"
        }
    
    # Enviar para policy agent via HTTP
    import aiohttp
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:8102/check_credit_policy",
                json={
                    "user_id": request.user_id,
                    "amount": request.amount,
                    "token": request.token,
                    "collateral": request.collateral
                }
            ) as response:
                policy_result = await response.json()
                logger.info(f"✅ Policy response: {policy_result}")
                return policy_result
    except Exception as e:
        logger.error(f"❌ Error calling policy agent: {e}")
        return {
            "success": False,
            "approved": False,
            "message": f"Policy check failed: {str(e)}"
        }

@http_app.post("/process_rwa")
async def http_process_rwa(request: HTTPRWARequest):
    """HTTP endpoint para processar requisições de RWA"""
    logger.info(f"🔵 HTTP: RWA request from {request.user_id}: ${request.property_value}")
    
    if request.property_value < 50000:
        return {
            "success": False,
            "approved": False,
            "message": "Property value must be at least $50,000"
        }
    
    import aiohttp
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:8102/check_rwa_policy",
                json={
                    "user_id": request.user_id,
                    "property_value": request.property_value,
                    "location": request.location,
                    "property_type": request.property_type
                }
            ) as response:
                policy_result = await response.json()
                logger.info(f"✅ Policy response: {policy_result}")
                return policy_result
    except Exception as e:
        logger.error(f"❌ Error calling policy agent: {e}")
        return {
            "success": False,
            "approved": False,
            "message": f"Policy check failed: {str(e)}"
        }

@http_app.post("/process_trade")
async def http_process_trade(request: HTTPTradeRequest):
    """HTTP endpoint para processar requisições de trade"""
    logger.info(f"🔵 HTTP: Trade request from {request.user_id}: {request.sell_amount} {request.sell_token}")
    
    import aiohttp
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:8102/check_trade_policy",
                json={
                    "user_id": request.user_id,
                    "sell_amount": request.sell_amount,
                    "sell_token": request.sell_token,
                    "buy_token": request.buy_token
                }
            ) as response:
                policy_result = await response.json()
                logger.info(f"✅ Policy response: {policy_result}")
                return policy_result
    except Exception as e:
        logger.error(f"❌ Error calling policy agent: {e}")
        return {
            "success": False,
            "matched": False,
            "message": f"Policy check failed: {str(e)}"
        }

@http_app.post("/process_automation")
async def http_process_automation(request: HTTPAutomationRequest):
    """HTTP endpoint para processar requisições de automação"""
    logger.info(f"🔵 HTTP: Automation request from {request.user_id}: {request.strategy}")
    
    if request.portfolio_value < 1000:
        return {
            "success": False,
            "approved": False,
            "message": "Portfolio must be at least $1,000"
        }
    
    import aiohttp
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:8102/check_automation_policy",
                json={
                    "user_id": request.user_id,
                    "portfolio_value": request.portfolio_value,
                    "strategy": request.strategy
                }
            ) as response:
                policy_result = await response.json()
                logger.info(f"✅ Policy response: {policy_result}")
                return policy_result
    except Exception as e:
        logger.error(f"❌ Error calling policy agent: {e}")
        return {
            "success": False,
            "approved": False,
            "message": f"Policy check failed: {str(e)}"
        }

@http_app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "agent": "intake"}

# ============================================================================
# ASI:ONE CHAT PROTOCOL (For ASI Alliance Hackathon)
# ============================================================================

if CHAT_AVAILABLE:
    # Initialize chat protocol with ASI:One spec
    chat_proto = Protocol(spec=chat_protocol_spec)
    
    async def parse_intent_with_perplexity(text: str, api_key: str) -> Optional[str]:
        """Use Perplexity to understand user intent when pattern matching fails"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                # Try multiple models in order of preference
                models = [
                    "llama-3.1-sonar-small-128k-online",
                    "sonar-small-online",
                    "llama-3.1-sonar-small-128k",
                    "mistral-7b-instruct"
                ]
                
                for model in models:
                    try:
                        response = await client.post(
                            "https://api.perplexity.ai/chat/completions",
                            headers={
                                "Authorization": f"Bearer {api_key}",
                                "Content-Type": "application/json"
                            },
                            json={
                                "model": model,
                                "messages": [
                                    {
                                        "role": "system",
                                        "content": "You are a DeFi assistant intent classifier. Classify user messages into one of: 'credit' (for loans/borrowing), 'rwa' (for tokenization), 'trade' (for trading/swapping), 'automation' (for portfolio management). Respond with ONLY the category name, nothing else."
                                    },
                                    {
                                        "role": "user",
                                        "content": text
                                    }
                                ],
                                "temperature": 0.1,
                                "max_tokens": 10
                            }
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            intent = result["choices"][0]["message"]["content"].strip().lower()
                            # Clean intent (remove extra words)
                            intent = intent.split()[0] if intent.split() else intent
                            if intent in ["credit", "rwa", "trade", "automation"]:
                                logger.info(f"🤖 Perplexity ({model}) detected intent: {intent}")
                                return intent
                            # If response is not valid, try next model
                        elif response.status_code == 400:
                            # Model might not exist, try next
                            logger.debug(f"Model {model} returned 400, trying next...")
                            continue
                        else:
                            logger.warning(f"Perplexity API returned {response.status_code}: {response.text[:200]}")
                    except Exception as model_error:
                        logger.debug(f"Error with model {model}: {model_error}")
                        continue
                
                return None
        except Exception as e:
            logger.warning(f"⚠️ Perplexity API error: {e}")
            return None
    
    def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
        """Utility function to wrap plain text into a ChatMessage"""
        content = [TextContent(type="text", text=text)]
        if end_session:
            content.append(EndSessionContent(type="end-session"))
        return ChatMessage(
            timestamp=datetime.now(timezone.utc),
            msg_id=uuid4(),
            content=content,
        )
    
    @chat_proto.on_message(ChatMessage)
    async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
        """Handle incoming chat messages from ASI:One"""
        ctx.logger.info(f"💬 Chat message from {sender}")
        
        # Always send back an acknowledgement
        await ctx.send(
            sender,
            ChatAcknowledgement(
                timestamp=datetime.now(timezone.utc),
                acknowledged_msg_id=msg.msg_id
            )
        )
        
        # Process each content item
        for item in msg.content:
            # Session start
            if isinstance(item, StartSessionContent):
                ctx.logger.info(f"🔵 Chat session started with {sender}")
                welcome_msg = create_text_chat(
                    "👋 Hi! I'm CypherGuy, your DeFi assistant!\n\n"
                    "I can help you with:\n"
                    "💳 Private DeFi Credit\n"
                    "🏢 RWA Tokenization\n"
                    "🌑 Dark Pool Trading\n"
                    "🤖 DeFi Automation\n\n"
                    "What would you like to do?"
                )
                await ctx.send(sender, welcome_msg)
            
            # Plain text message
            elif isinstance(item, TextContent):
                ctx.logger.info(f"💬 Text from {sender}: {item.text}")
                
                # Get conversation context for this user
                chat_context = ctx.storage.get("chat_context") or {}
                user_context = chat_context.get(sender, {"state": "idle", "intent": None})
                
                # Parse user intent (simple NLP)
                text_lower = item.text.lower()
                
                # Extract numbers from text
                numbers = re.findall(r'\d+', item.text)
                amounts = [int(n) for n in numbers if int(n) > 0]
                
                # Check for token mentions
                tokens = []
                for token in ["usdc", "sol", "eth", "usdt", "btc"]:
                    if token in text_lower:
                        tokens.append(token.upper())
                
                # Intent detection (normalize common typos/variations)
                # Replace common variations
                normalized_text = text_lower.replace("do borrow", "borrow").replace("to borrow", "borrow")
                
                if any(word in normalized_text for word in ["credit", "loan", "borrow"]) or user_context.get("intent") == "credit":
                    # User wants credit - update context
                    if user_context.get("intent") != "credit":
                        user_context = {"state": "credit_amount", "intent": "credit", "amount": None, "collateral": None}
                        response = create_text_chat(
                            "💳 I can help you get a private DeFi loan!\n\n"
                            "I'll need:\n"
                            "- Amount (USDC)\n"
                            "- Collateral type\n\n"
                            "Your credit score will be calculated privately using MPC. "
                            "How much would you like to borrow?"
                        )
                    else:
                        # User is responding with amount/collateral
                        if amounts and user_context.get("amount") is None:
                            user_context["amount"] = amounts[0]
                            user_context["state"] = "credit_collateral"
                            if tokens:
                                user_context["collateral"] = tokens[0]
                                # Got everything, process request
                                user_context["state"] = "processing"
                                response = create_text_chat(
                                    f"✅ Got it! Processing your request:\n\n"
                                    f"💰 Amount: {user_context['amount']} USDC\n"
                                    f"🔒 Collateral: {user_context.get('collateral', 'Not specified')}\n\n"
                                    f"🔍 Checking your credit policy...\n"
                                    f"📊 Calculating credit score...\n\n"
                                    f"This may take a moment. I'll contact PolicyAgent and ComputeAgent for you!"
                                )
                                user_context = {"state": "idle", "intent": None}  # Reset
                            else:
                                response = create_text_chat(
                                    f"✅ Amount: {user_context['amount']} USDC\n\n"
                                    "What collateral would you like to use?\n"
                                    "(e.g., SOL, ETH, USDC)"
                                )
                        elif tokens and user_context.get("collateral") is None:
                            user_context["collateral"] = tokens[0]
                            if user_context.get("amount"):
                                # Got everything
                                user_context["state"] = "processing"
                                response = create_text_chat(
                                    f"✅ Processing your request:\n\n"
                                    f"💰 Amount: {user_context['amount']} USDC\n"
                                    f"🔒 Collateral: {user_context['collateral']}\n\n"
                                    f"🔍 Checking credit policy...\n"
                                    f"📊 Calculating credit score...\n\n"
                                    f"Processing via PolicyAgent → ComputeAgent → ExecutorAgent!"
                                )
                                user_context = {"state": "idle", "intent": None}  # Reset
                            else:
                                response = create_text_chat(
                                    f"✅ Collateral: {user_context['collateral']}\n\n"
                                    "How much USDC would you like to borrow?"
                                )
                        elif amounts and tokens:
                            # User provided both at once
                            user_context = {"state": "processing", "intent": "credit", "amount": amounts[0], "collateral": tokens[0]}
                            response = create_text_chat(
                                f"✅ Perfect! Processing your request:\n\n"
                                f"💰 Amount: {amounts[0]} USDC\n"
                                f"🔒 Collateral: {tokens[0]}\n\n"
                                f"🔍 Checking credit policy...\n"
                                f"📊 Calculating credit score...\n\n"
                                f"Processing through our agent network!"
                            )
                            user_context = {"state": "idle", "intent": None}  # Reset
                        else:
                            amount_str = f"{user_context.get('amount')} USDC ✅" if user_context.get('amount') else "❓ Not provided yet"
                            collateral_str = f"{user_context.get('collateral')} ✅" if user_context.get('collateral') else "❓ Not provided yet"
                            response = create_text_chat(
                                f"I need:\n"
                                f"- Amount: {amount_str}\n"
                                f"- Collateral: {collateral_str}\n\n"
                                f"What's missing?"
                            )
                    
                    # Save updated context
                    chat_context[sender] = user_context
                    ctx.storage.set("chat_context", chat_context)
                
                elif any(word in text_lower for word in ["rwa", "tokenize", "property", "asset"]):
                    response = create_text_chat(
                        "🏢 I can help tokenize your real-world assets!\n\n"
                        "I'll need:\n"
                        "- Property value\n"
                        "- Location\n"
                        "- Property type\n\n"
                        "I'll check compliance rules automatically. "
                        "What asset would you like to tokenize?"
                    )
                
                elif any(word in text_lower for word in ["trade", "swap", "exchange"]):
                    response = create_text_chat(
                        "🌑 I can help you trade privately in a dark pool!\n\n"
                        "I'll need:\n"
                        "- Amount to sell\n"
                        "- Tokens (from/to)\n\n"
                        "Your order will be matched privately without moving the market. "
                        "What would you like to trade?"
                    )
                
                elif any(word in text_lower for word in ["automat", "optimize", "manage"]):
                    response = create_text_chat(
                        "🤖 I can automatically optimize your portfolio!\n\n"
                        "I'll need:\n"
                        "- Portfolio value\n"
                        "- Strategy (yield farming, balanced, etc)\n\n"
                        "I'll monitor markets 24/7 and rebalance for best yields. "
                        "What strategy interests you?"
                    )
                
                elif any(word in text_lower for word in ["help", "what", "how"]):
                    response = create_text_chat(
                        "🦸 I'm CypherGuy - your personal DeFi assistant!\n\n"
                        "I help you with complex DeFi operations using AI agents:\n\n"
                        "💳 **Private DeFi Credit** - Get loans without revealing your portfolio\n"
                        "🏢 **RWA Compliance** - Tokenize real-world assets following regulations\n"
                        "🌑 **Dark Pool Trading** - Trade large amounts privately\n"
                        "🤖 **DeFi Automation** - Auto-optimize for best yields\n\n"
                        "Just tell me what you need!"
                    )
                
                else:
                    # Fallback - check if user is in middle of a conversation
                    if user_context.get("intent") == "credit":
                        # User is responding to credit flow but message unclear
                        if amounts:
                            response = create_text_chat(f"Is that {amounts[0]} USDC? If so, what collateral would you like to use?")
                        else:
                            amount_str = f"{user_context.get('amount')} USDC ✅" if user_context.get('amount') else "❓ Not provided yet"
                            collateral_str = f"{user_context.get('collateral')} ✅" if user_context.get('collateral') else "❓ Not provided yet"
                            response = create_text_chat(
                                f"I need:\n"
                                f"- Amount: {amount_str}\n"
                                f"- Collateral: {collateral_str}\n\n"
                                f"Could you specify what's missing?"
                            )
                    else:
                        # Try Perplexity if available (optional LLM enhancement)
                        perplexity_key = os.getenv("PERPLEXITY_API_KEY")
                        if perplexity_key:
                            try:
                                intent = await parse_intent_with_perplexity(item.text, perplexity_key)
                                if intent:
                                    ctx.logger.info(f"🤖 Perplexity detected intent: {intent}")
                                    # Re-process with detected intent
                                    if intent == "credit":
                                        user_context = {"state": "credit_amount", "intent": "credit", "amount": amounts[0] if amounts else None, "collateral": tokens[0] if tokens else None}
                                        chat_context[sender] = user_context
                                        ctx.storage.set("chat_context", chat_context)
                                        if amounts and tokens:
                                            response = create_text_chat(
                                                f"✅ I understand! Processing:\n\n"
                                                f"💰 Amount: {amounts[0]} USDC\n"
                                                f"🔒 Collateral: {tokens[0]}\n\n"
                                                f"🔍 Checking credit policy..."
                                            )
                                        elif amounts:
                                            response = create_text_chat(
                                                f"✅ Amount: {amounts[0]} USDC\n\n"
                                                "What collateral would you like to use?\n"
                                                "(e.g., SOL, ETH, USDC)"
                                            )
                                        else:
                                            response = create_text_chat(
                                                "💳 I can help you get a private DeFi loan!\n\n"
                                                "How much USDC would you like to borrow?"
                                            )
                                    else:
                                        response = create_text_chat(
                                            f"I see you're interested in {intent}. Let me help you with that!"
                                        )
                                else:
                                    raise ValueError("No intent detected")
                            except Exception as e:
                                ctx.logger.warning(f"⚠️ Perplexity parsing failed: {e}, using fallback")
                                response = create_text_chat(
                                    "I can help with:\n"
                                    "💳 Credit/Loans\n"
                                    "🏢 RWA Tokenization\n"
                                    "🌑 Private Trading\n"
                                    "🤖 Portfolio Automation\n\n"
                                    "Which one interests you?"
                                )
                        else:
                            # No Perplexity - use simple fallback
                            response = create_text_chat(
                                "I can help with:\n"
                                "💳 Credit/Loans\n"
                                "🏢 RWA Tokenization\n"
                                "🌑 Private Trading\n"
                                "🤖 Portfolio Automation\n\n"
                                "Which one interests you?"
                            )
                
                await ctx.send(sender, response)
            
            # Session end
            elif isinstance(item, EndSessionContent):
                ctx.logger.info(f"🔵 Chat session ended with {sender}")
                goodbye_msg = create_text_chat(
                    "👋 Thanks for using CypherGuy! Come back anytime you need DeFi help!",
                    end_session=True
                )
                await ctx.send(sender, goodbye_msg)
            
            # Unexpected content
            else:
                ctx.logger.warning(f"⚠️ Unexpected content type from {sender}")
    
    @chat_proto.on_message(ChatAcknowledgement)
    async def handle_chat_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
        """Handle acknowledgements for messages we sent"""
        ctx.logger.info(f"✅ Chat ack from {sender} for msg {msg.acknowledged_msg_id}")
    
    # Include chat protocol and publish manifest to Agentverse
    intake_agent.include(chat_proto, publish_manifest=True)
    logger.info("💬 ASI:One Chat Protocol enabled!")
else:
    logger.warning("⚠️ ASI:One Chat Protocol not available - install uagents_core")

# ============================================================================
# RUN AGENT + HTTP SERVER
# ============================================================================

def run_http_server():
    """Rodar HTTP server em thread separada"""
    import os
    port = int(os.getenv("PORT", "8101"))  # Usar $PORT do Render ou default 8101
    uvicorn.run(http_app, host="0.0.0.0", port=port, log_level="info")

if __name__ == "__main__":
    logger.info("🦸 Starting AgentIntake...")
    logger.info("🌐 HTTP server will run on port 8101")
    
    # Iniciar HTTP server em thread
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()
    
    # Rodar uAgent
    intake_agent.run()


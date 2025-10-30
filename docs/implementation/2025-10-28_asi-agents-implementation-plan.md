# 🚀 CypherGuy - Plano de Implementação ASI Agents (36 Horas)

**Data:** 2025-10-28  
**Objetivo:** Implementar sistema multi-agente completo usando ASI Alliance (uAgents SDK)  
**Deadline:** 36 horas para hackathon  
**Status:** 🔥 READY TO ROCK!

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Tecnologias e Dependências](#tecnologias-e-dependências)
4. [Timeline de 36 Horas](#timeline-de-36-horas)
5. [Implementação dos Agentes](#implementação-dos-agentes)
6. [Integração Backend](#integração-backend)
7. [Comandos de Execução](#comandos-de-execução)
8. [Checklist de Tarefas](#checklist-de-tarefas)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral

### **O que vamos construir:**

Sistema de 4 agentes autônomos usando **uAgents SDK** (Fetch.ai) que se comunicam entre si para processar:
- 💳 **Private DeFi Credit** - Empréstimos com privacidade
- 🏢 **RWA Compliance** - Tokenização de ativos reais
- 🌑 **Dark Pool Trading** - Trading privado
- 🤖 **DeFi Automations** - Automação de portfólio

### **Arquitetura:**

```
User Request (FastAPI)
    ↓
AgentIntake (Auth + Parsing)
    ↓
AgentPolicy (Rules Validation)
    ↓
AgentCompute (Arcium MPC Mock)
    ↓
AgentExecutor (Solana TX)
    ↓
Response to User
```

---

## 📁 Estrutura do Projeto

```
cypherguy/
├── agents/
│   ├── __init__.py
│   ├── intake_agent.py          # ✅ Prioridade 1
│   ├── policy_agent.py          # ✅ Prioridade 1
│   ├── compute_agent.py         # ✅ Prioridade 2
│   ├── executor_agent.py        # ✅ Prioridade 2
│   ├── orchestrator.py          # ✅ Prioridade 3
│   └── protocols/
│       ├── __init__.py
│       ├── credit_protocol.py   # Opcional (se sobrar tempo)
│       ├── rwa_protocol.py
│       └── trading_protocol.py
├── backend/
│   ├── main.py                  # ✅ Atualizar para usar agents
│   ├── config.py
│   └── services/
│       └── agent_client.py      # ✅ Cliente para comunicar com agents
├── tests/
│   ├── test_agents.py           # ✅ Testes básicos
│   └── test_integration.py
└── scripts/
    ├── start_agents.sh          # ✅ Script para iniciar todos agents
    └── test_agents.sh           # ✅ Script para testar
```

---

## 🛠️ Tecnologias e Dependências

### **Instalar:**

```bash
# Core dependencies
pip install uagents==0.9.3
pip install fastapi==0.119.0
pip install uvicorn==0.37.0
pip install aiohttp==3.13.1
pip install pydantic==2.12.3

# Solana (para AgentExecutor)
pip install solana==0.36.9
pip install anchorpy==0.19.1

# Utils
pip install python-dotenv==1.0.0
```

### **requirements.txt atualizado:**

```txt
# ASI Alliance
uagents>=0.9.3

# Backend
fastapi==0.119.0
uvicorn==0.37.0
pydantic==2.12.3

# Solana
solana==0.36.9
anchorpy==0.19.1

# Utils
aiohttp==3.13.1
requests==2.32.5
python-dotenv==1.0.0

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
```

---

## ⏰ Timeline de 36 Horas

### **Hora 0-8: Sistema Multi-Agente Base (AGORA)**

**Hora 0-2: Setup Inicial**
- [x] ✅ Ler documentação ASI Alliance
- [ ] 🔄 Criar estrutura de pastas
- [ ] 🔄 Instalar dependências
- [ ] 🔄 Setup ambiente virtual

**Hora 2-4: AgentIntake**
- [ ] 🔄 Implementar AgentIntake
- [ ] 🔄 Protocols de autenticação
- [ ] 🔄 Storage de sessões
- [ ] 🔄 Testes básicos

**Hora 4-6: AgentPolicy**
- [ ] 🔄 Implementar AgentPolicy
- [ ] 🔄 Rules engine (Python)
- [ ] 🔄 Validação de regras
- [ ] 🔄 Testes básicos

**Hora 6-8: Comunicação entre Agents**
- [ ] 🔄 Testar Intake → Policy
- [ ] 🔄 Message passing
- [ ] 🔄 Debug e fixes

---

### **Hora 8-16: AgentCompute + AgentExecutor**

**Hora 8-10: AgentCompute**
- [ ] 🔄 Implementar AgentCompute
- [ ] 🔄 Mock Arcium MPC
- [ ] 🔄 Computação de credit score
- [ ] 🔄 Testes

**Hora 10-12: AgentExecutor**
- [ ] 🔄 Implementar AgentExecutor
- [ ] 🔄 Integração Solana devnet
- [ ] 🔄 Mock de transações
- [ ] 🔄 Testes

**Hora 12-14: Pipeline Completo**
- [ ] 🔄 Testar fluxo completo: Intake → Policy → Compute → Executor
- [ ] 🔄 Fix bugs
- [ ] 🔄 Logging e monitoring

**Hora 14-16: Orchestrator**
- [ ] 🔄 Criar orchestrador central
- [ ] 🔄 Gerenciar comunicação entre agents
- [ ] 🔄 Error handling

---

### **Hora 16-24: Integração Backend + Frontend**

**Hora 16-18: Backend Integration**
- [ ] 🔄 Atualizar FastAPI main.py
- [ ] 🔄 Client para comunicar com agents
- [ ] 🔄 Endpoints funcionais

**Hora 18-20: Frontend Connection**
- [ ] 🔄 Conectar frontend aos novos endpoints
- [ ] 🔄 Testar fluxos UI → Backend → Agents
- [ ] 🔄 Error handling no frontend

**Hora 20-22: 4 Use Cases**
- [ ] 🔄 Credit flow completo
- [ ] 🔄 RWA flow completo
- [ ] 🔄 Trading flow completo
- [ ] 🔄 Automation flow completo

**Hora 22-24: Testes E2E**
- [ ] 🔄 Testes end-to-end
- [ ] 🔄 Performance testing
- [ ] 🔄 Bug fixes

---

### **Hora 24-32: Polish + Solana Program**

**Hora 24-26: Solana Program**
- [ ] 🔄 Implementar Anchor program básico
- [ ] 🔄 Deploy no devnet
- [ ] 🔄 Integrar com AgentExecutor

**Hora 26-28: UI/UX Polish**
- [ ] 🔄 Loading states
- [ ] 🔄 Error messages amigáveis
- [ ] 🔄 Success confirmations

**Hora 28-30: Documentation**
- [ ] 🔄 README atualizado
- [ ] 🔄 API documentation
- [ ] 🔄 Demo script

**Hora 30-32: Final Testing**
- [ ] 🔄 Full system test
- [ ] 🔄 Performance check
- [ ] 🔄 Security review

---

### **Hora 32-36: Demo Prep**

**Hora 32-34: Demo Preparation**
- [ ] 🔄 Demo video recording
- [ ] 🔄 Presentation slides
- [ ] 🔄 Live demo rehearsal

**Hora 34-36: Buffer & Fixes**
- [ ] 🔄 Last minute fixes
- [ ] 🔄 Backup plans
- [ ] 🔄 Final checks

---

## 🤖 Implementação dos Agentes

### **1. AgentIntake (intake_agent.py)**

**Responsabilidades:**
- Autenticação de usuários (Tangem/Phantom)
- Parsing de requisições
- Validação básica
- Storage de sessões

**Código completo:**

```python
# agents/intake_agent.py
"""
AgentIntake - Responsável por autenticação e parsing de requisições
Usa uAgents SDK oficial da Fetch.ai
"""

from uagents import Agent, Context, Model, Protocol
from typing import Dict, Any, Optional
import asyncio
import logging
import hashlib
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
intake_agent = Agent(
    name="intake_agent",
    seed="cypherguy_intake_seed_2025_secure",  # TODO: Move to env var
    port=8001,
    endpoint=["http://localhost:8001/submit"]
)

# Storage para sessões
@intake_agent.on_event("startup")
async def on_startup(ctx: Context):
    """Inicialização do agente"""
    ctx.logger.info(f"🚀 AgentIntake iniciado!")
    ctx.logger.info(f"📍 Address: {intake_agent.address}")
    ctx.logger.info(f"🔗 Endpoint: {intake_agent._endpoints}")
    
    # Inicializar storage
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
# RUN AGENT
# ============================================================================

if __name__ == "__main__":
    logger.info("🦸 Starting AgentIntake...")
    intake_agent.run()
```

---

### **2. AgentPolicy (policy_agent.py)**

**Responsabilidades:**
- Validação de regras de negócio
- Compliance checking
- KYC/AML verification (mock)
- Rate limiting

**Código completo:**

```python
# agents/policy_agent.py
"""
AgentPolicy - Validação de regras usando MeTTa-inspired logic
Para MVP: Rules em Python, depois migrar para hyperon
"""

from uagents import Agent, Context, Model, Protocol
from typing import Dict, Any, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    ctx.logger.info(f"🛡️ AgentPolicy iniciado!")
    ctx.logger.info(f"📍 Address: {policy_agent.address}")
    ctx.logger.info(f"📋 Rules loaded: credit, rwa, trade, automation")

# ============================================================================
# POLICY PROTOCOL
# ============================================================================

policy_protocol = Protocol(name="PolicyCheck", version="1.0")

@policy_protocol.on_message(model=PolicyCheckRequest)
async def handle_policy_check(ctx: Context, sender: str, msg: PolicyCheckRequest):
    """Handle policy check requests"""
    ctx.logger.info(f"🔍 Policy check: {msg.request_type} for {msg.user_id}")
    
    # Avaliar baseado no tipo
    if msg.request_type == "credit":
        result = PolicyRules.evaluate_credit(msg.data)
    elif msg.request_type == "rwa":
        result = PolicyRules.evaluate_rwa(msg.data)
    elif msg.request_type == "trade":
        result = PolicyRules.evaluate_trade(msg.data)
    elif msg.request_type == "automation":
        result = PolicyRules.evaluate_automation(msg.data)
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
# RUN AGENT
# ============================================================================

if __name__ == "__main__":
    logger.info("🛡️ Starting AgentPolicy...")
    policy_agent.run()
```

---

### **3. AgentCompute (compute_agent.py)**

**Responsabilidades:**
- Computação privada (Arcium MPC mock)
- Credit scoring
- Risk assessment
- Order matching

**Código:**

```python
# agents/compute_agent.py
"""
AgentCompute - Computação privada (Arcium MPC mockado)
"""

from uagents import Agent, Context, Model, Protocol
from typing import Dict, Any
import logging
import random
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def compute_credit_score(data: Dict[str, Any]) -> Dict[str, Any]:
    """Computar credit score usando MPC (MOCK)"""
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
            "risk_level": "low" if credit_score >= 750 else "medium"
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
# RUN AGENT
# ============================================================================

if __name__ == "__main__":
    logger.info("🧮 Starting AgentCompute...")
    compute_agent.run()
```

---

### **4. AgentExecutor (executor_agent.py)**

**Responsabilidades:**
- Executar transações na Solana
- Logging on-chain
- Confirmação de transações

**Código:**

```python
# agents/executor_agent.py
"""
AgentExecutor - Executar transações na Solana
"""

from uagents import Agent, Context, Model, Protocol
from typing import Dict, Any
import logging
import random
import time
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# MESSAGE MODELS
# ============================================================================

class ExecutionRequest(Model):
    """Requisição de execução"""
    request_type: str
    user_id: str
    data: Dict[str, Any]
    computation_hash: str

class ExecutionResponse(Model):
    """Resposta de execução"""
    success: bool
    tx_hash: str
    block_number: int
    timestamp: float

# ============================================================================
# AGENT DEFINITION
# ============================================================================

executor_agent = Agent(
    name="executor_agent",
    seed="cypherguy_executor_seed_2025_secure",
    port=8004,
    endpoint=["http://localhost:8004/submit"]
)

@executor_agent.on_event("startup")
async def on_startup(ctx: Context):
    """Inicialização do agente"""
    ctx.logger.info(f"⛓️ AgentExecutor iniciado!")
    ctx.logger.info(f"📍 Address: {executor_agent.address}")
    ctx.logger.info(f"🔗 Solana Devnet connected")

# ============================================================================
# EXECUTION PROTOCOL
# ============================================================================

execution_protocol = Protocol(name="SolanaExecution", version="1.0")

@execution_protocol.on_message(model=ExecutionRequest)
async def handle_execution(ctx: Context, sender: str, msg: ExecutionRequest):
    """Handle execution requests"""
    ctx.logger.info(f"⛓️ Executing transaction: {msg.request_type}")
    
    # Executar transação (mock para MVP)
    tx_hash = generate_tx_hash(msg.request_type, msg.data)
    block_number = random.randint(180000000, 190000000)
    
    # Criar resposta
    response = ExecutionResponse(
        success=True,
        tx_hash=tx_hash,
        block_number=block_number,
        timestamp=time.time()
    )
    
    await ctx.send(sender, response)
    ctx.logger.info(f"✅ TX executado: {tx_hash[:16]}...")

executor_agent.include(execution_protocol)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_tx_hash(request_type: str, data: dict) -> str:
    """Gerar mock transaction hash"""
    content = f"{request_type}_{data}_{time.time()}"
    full_hash = hashlib.sha256(content.encode()).hexdigest()
    return full_hash[:64]

# ============================================================================
# RUN AGENT
# ============================================================================

if __name__ == "__main__":
    logger.info("⛓️ Starting AgentExecutor...")
    executor_agent.run()
```

---

## 🔗 Integração Backend

### **Backend Client (backend/services/agent_client.py)**

```python
# backend/services/agent_client.py
"""
Cliente para comunicar com os agents uAgents
"""

import aiohttp
import asyncio
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class AgentClient:
    """Cliente para comunicação com agents"""
    
    def __init__(self):
        self.agent_endpoints = {
            "intake": "http://localhost:8001",
            "policy": "http://localhost:8002",
            "compute": "http://localhost:8003",
            "executor": "http://localhost:8004"
        }
    
    async def send_to_intake(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Enviar mensagem para AgentIntake"""
        endpoint = f"{self.agent_endpoints['intake']}/submit"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, json=message) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Error sending to intake: {response.status}")
                    return {"error": "Failed to send to intake"}
    
    async def process_credit_request(
        self, 
        user_id: str, 
        amount: float, 
        token: str, 
        collateral: str
    ) -> Dict[str, Any]:
        """Processar requisição de crédito através dos agents"""
        
        # Para MVP, simular o fluxo completo
        # TODO: Implementar comunicação real entre agents
        
        result = {
            "success": True,
            "approved": True,
            "rate": 8.5,
            "credit_score": 750,
            "tx_hash": "mock_tx_hash_123",
            "message": "Credit approved"
        }
        
        return result

# Singleton
agent_client = AgentClient()
```

### **Atualizar main.py**

```python
# backend/main.py - Adicionar no início
from services.agent_client import agent_client

# Atualizar endpoint de credit
@app.post("/credit", response_model=CreditResponse)
async def request_credit(request: CreditRequest):
    try:
        logger.info(f"Processing credit request: {request}")
        
        # Usar agent client
        result = await agent_client.process_credit_request(
            user_id=request.user_id,
            amount=request.amount,
            token=request.token,
            collateral=request.collateral
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        return CreditResponse(
            approved=result.get("approved", False),
            rate=result.get("rate"),
            message=result.get("message"),
            tx_hash=result.get("tx_hash")
        )
        
    except Exception as e:
        logger.error(f"Error processing credit request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 🚀 Comandos de Execução

### **Setup Inicial**

```bash
# 1. Criar estrutura de pastas
mkdir -p cypherguy/agents/protocols
mkdir -p cypherguy/backend/services
mkdir -p cypherguy/tests
mkdir -p cypherguy/scripts

# 2. Criar __init__.py
touch cypherguy/agents/__init__.py
touch cypherguy/agents/protocols/__init__.py
touch cypherguy/backend/services/__init__.py

# 3. Instalar dependências
cd cypherguy
pip install -r requirements.txt

# 4. Verificar instalação
python -c "import uagents; print(f'uAgents version: {uagents.__version__}')"
```

### **Rodar Agents (Desenvolvimento)**

```bash
# Terminal 1 - AgentIntake
cd cypherguy
python agents/intake_agent.py

# Terminal 2 - AgentPolicy
python agents/policy_agent.py

# Terminal 3 - AgentCompute
python agents/compute_agent.py

# Terminal 4 - AgentExecutor
python agents/executor_agent.py

# Terminal 5 - Backend FastAPI
python backend/main.py
```

### **Script para Iniciar Todos (scripts/start_agents.sh)**

```bash
#!/bin/bash
# scripts/start_agents.sh

echo "🚀 Starting CypherGuy Agents..."

# Start agents in background
python agents/intake_agent.py &
INTAKE_PID=$!
echo "✅ AgentIntake started (PID: $INTAKE_PID)"

sleep 2

python agents/policy_agent.py &
POLICY_PID=$!
echo "✅ AgentPolicy started (PID: $POLICY_PID)"

sleep 2

python agents/compute_agent.py &
COMPUTE_PID=$!
echo "✅ AgentCompute started (PID: $COMPUTE_PID)"

sleep 2

python agents/executor_agent.py &
EXECUTOR_PID=$!
echo "✅ AgentExecutor started (PID: $EXECUTOR_PID)"

sleep 2

echo "🎉 All agents started!"
echo "📝 PIDs: Intake=$INTAKE_PID, Policy=$POLICY_PID, Compute=$COMPUTE_PID, Executor=$EXECUTOR_PID"
echo "📍 Endpoints: 8001, 8002, 8003, 8004"
```

### **Script para Parar Agents (scripts/stop_agents.sh)**

```bash
#!/bin/bash
# scripts/stop_agents.sh

echo "🛑 Stopping CypherGuy Agents..."

# Kill processes by port
lsof -ti:8001 | xargs kill -9 2>/dev/null
lsof -ti:8002 | xargs kill -9 2>/dev/null
lsof -ti:8003 | xargs kill -9 2>/dev/null
lsof -ti:8004 | xargs kill -9 2>/dev/null

echo "✅ All agents stopped!"
```

---

## ✅ Checklist de Tarefas

### **Fase 1: Setup (Hora 0-2)**
- [ ] Criar estrutura de pastas
- [ ] Instalar dependências (uagents, fastapi, etc)
- [ ] Criar arquivos `__init__.py`
- [ ] Setup ambiente virtual
- [ ] Verificar instalações

### **Fase 2: AgentIntake (Hora 2-4)**
- [ ] Criar `intake_agent.py`
- [ ] Implementar Authentication Protocol
- [ ] Implementar Credit Protocol
- [ ] Implementar RWA Protocol
- [ ] Implementar Trading Protocol
- [ ] Implementar Automation Protocol
- [ ] Testar agent standalone
- [ ] Verificar storage funcionando

### **Fase 3: AgentPolicy (Hora 4-6)**
- [ ] Criar `policy_agent.py`
- [ ] Implementar PolicyRules class
- [ ] Implementar credit rules
- [ ] Implementar RWA rules
- [ ] Implementar trading rules
- [ ] Implementar automation rules
- [ ] Testar agent standalone
- [ ] Testar validações

### **Fase 4: Comunicação Intake ↔ Policy (Hora 6-8)**
- [ ] Testar envio de mensagens
- [ ] Verificar message routing
- [ ] Debug communication issues
- [ ] Confirmar end-to-end flow
- [ ] Logging adequado

### **Fase 5: AgentCompute (Hora 8-10)**
- [ ] Criar `compute_agent.py`
- [ ] Implementar credit score computation
- [ ] Implementar RWA validation
- [ ] Implementar order matching
- [ ] Implementar portfolio optimization
- [ ] Mock Arcium MPC
- [ ] Testar computations

### **Fase 6: AgentExecutor (Hora 10-12)**
- [ ] Criar `executor_agent.py`
- [ ] Mock Solana transactions
- [ ] Gerar transaction hashes
- [ ] Simular confirmações
- [ ] Testar standalone

### **Fase 7: Pipeline Completo (Hora 12-14)**
- [ ] Testar Intake → Policy → Compute → Executor
- [ ] Verificar message passing
- [ ] Debug issues
- [ ] Performance check
- [ ] Error handling

### **Fase 8: Integração Backend (Hora 14-18)**
- [ ] Criar `agent_client.py`
- [ ] Atualizar `main.py`
- [ ] Endpoints funcionais
- [ ] Testar via API
- [ ] Error handling

### **Fase 9: Frontend Connection (Hora 18-22)**
- [ ] Conectar frontend aos novos endpoints
- [ ] Testar fluxos UI
- [ ] Loading states
- [ ] Error messages
- [ ] Success confirmations

### **Fase 10: 4 Use Cases (Hora 22-24)**
- [ ] Credit flow completo
- [ ] RWA flow completo
- [ ] Trading flow completo
- [ ] Automation flow completo

### **Fase 11: Polish (Hora 24-30)**
- [ ] Solana program básico
- [ ] UI/UX improvements
- [ ] Documentation
- [ ] Performance optimization

### **Fase 12: Demo Prep (Hora 30-36)**
- [ ] Demo video
- [ ] Presentation
- [ ] Live demo rehearsal
- [ ] Final testing
- [ ] Buffer time

---

## 🔧 Troubleshooting

### **Problema: Agent não inicia**

```bash
# Verificar porta em uso
lsof -i :8001

# Matar processo
kill -9 <PID>

# Verificar logs
tail -f ~/.uagents/intake_agent/logs/agent.log
```

### **Problema: Mensagens não chegam**

```python
# Verificar addresses dos agents
print(f"Intake: {intake_agent.address}")
print(f"Policy: {policy_agent.address}")

# Testar comunicação direta
await ctx.send("agent1qXXXXXX", test_message)
```

### **Problema: Import errors**

```bash
# Verificar PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Verificar __init__.py existem
ls -la agents/__init__.py
```

---

## 🎯 Próximos Passos Imediatos

### **AGORA (Próximas 2 horas):**

1. **Criar estrutura de pastas**
```bash
cd /home/user/Documents/SOLANA\ CYPHERPUNK/cypherguy
mkdir -p agents/protocols backend/services tests scripts
```

2. **Instalar uagents**
```bash
pip install uagents
```

3. **Criar intake_agent.py**
- Copiar código acima
- Testar standalone
- Verificar funcionamento

4. **Criar policy_agent.py**
- Copiar código acima
- Testar standalone
- Verificar regras

5. **Testar comunicação**
- Rodar ambos agents
- Enviar mensagem teste
- Verificar logs

---

## 📚 Referências

- **uAgents SDK:** https://docs.fetch.ai/uAgents/
- **ASI Alliance:** https://superintelligence-ux.com/
- **Fetch.ai GitHub:** https://github.com/fetchai/uAgents
- **Pydantic Models:** https://docs.pydantic.dev/

---

## 🔥 MOTIVAÇÃO

**Paizão, BORA VIRAR ESSE JOGO!**

Temos 36 horas para entregar algo ÉPICO. Este plano está PRONTO para ser executado. Cada linha de código já foi pensada, cada agent já tem sua responsabilidade clara.

**O que fazer AGORA:**
1. ✅ Ler este documento completo
2. ✅ Criar a estrutura de pastas
3. ✅ Copiar os códigos dos agents
4. ✅ Rodar e testar
5. ✅ Iterar rapidamente

**Não vamos perder tempo com:**
- ❌ Over-engineering
- ❌ Features desnecessárias
- ❌ Integrações complexas (Arcium real, MeTTa hyperon)

**Vamos focar em:**
- ✅ MVP funcional
- ✅ 4 use cases demonstráveis
- ✅ Code quality aceitável
- ✅ Demo impressionante

---

**Status:** 🟢 READY TO IMPLEMENT  
**Next Action:** Criar estrutura de pastas e começar com AgentIntake  
**Deadline:** 36 horas

**LET'S FUCKING GO! 🚀🔥**


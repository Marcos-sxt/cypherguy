# 🔵 INTAKE AGENT - GUIA COMPLETO

**Agent Name:** `intake_agent`  
**Address:** pryx5v8upqj0xw0hwvehvdevrvt0pvxw0n0khtqcnpvknjvwp5wm8n5  
**Ports:** 8001 (uAgent), 8101 (HTTP)  
**Linhas de Código:** 662 linhas  
**Propósito:** Entrada, validação e roteamento de requisições

---

## 📚 ÍNDICE

1. [Visão Geral](#visão-geral)
2. [Arquitetura](#arquitetura)
3. [Componentes](#componentes)
4. [Protocolos](#protocolos)
5. [HTTP Endpoints](#http-endpoints)
6. [ASI:One Chat Protocol](#asion-chat-protocol)
7. [Fluxos de Dados](#fluxos-de-dados)
8. [Storage](#storage)
9. [Como Funciona na Prática](#como-funciona-na-prática)

---

## 🎯 VISÃO GERAL

### O Que É o IntakeAgent?

O **IntakeAgent** é o **ponto de entrada** do sistema CypherGuy. Ele é responsável por:

1. ✅ **Receber requisições** (via HTTP ou Chat Protocol)
2. ✅ **Parsear e validar** dados de entrada
3. ✅ **Classificar intenção** do usuário
4. ✅ **Rotear** para o próximo agent (PolicyAgent)
5. ✅ **Gerenciar sessões** e autenticação
6. ✅ **Responder** em natural language (Chat Protocol)

### Diagrama de Papel no Sistema

```
┌─────────────────────────────────────────────────────┐
│                  USER REQUEST                        │
│  (HTTP POST /process_credit OU Chat Message)        │
└─────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│          🔵 INTAKE AGENT                             │
│  ─────────────────────────                          │
│  • Recebe request                                   │
│  • Valida entrada                                   │
│  • Parseia intenção                                 │
│  • Cria session token                               │
│  • Armazena request                                 │
└─────────────────────────────────────────────────────┘
                    │
                    ▼
         Roteamento dal向前  forward
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│          🛡️ POLICY AGENT (Port 8102)               │
│  Recebe via HTTP POST                               │
└─────────────────────────────────────────────────────┘
```

---

## 🏗️ ARQUITETURA

### Dual-Mode Operation

O IntakeAgent opera em **2 modos simultâneos**:

#### **Modo 1: uAgents Protocol** (Message-Based)
```
✅ Para comunicação entre agents (uAgent-to-uAgent)
✅ Usa Protocols (Auth, Credit, RWA, Trade, Automation)
✅ Message handlers com `@protocol.on_message()`
✅ Assíncrono, tipo-safe (Pydantic Models)
```

#### **Modo 2: HTTP REST API** (REST)
```
✅ Para comunicação do backend/Frontend
✅ Usa FastAPI endpoints
✅ HTTP POST /process_credit, /process_rwa, etc
✅ Síncrono, JSON-based
```

### Por Que Dois Modos?

```
uAgents Protocol:
  • Comunicação inter-agent (ideal para ASI Alliance)
  • Type-safe (Pydantic Models)
  • Assíncrono (melhor performance)
  • Descoberta via Agentverse
  
ratHTTP REST:
  • Fácil integração com backend
  • Debugging simples (curl, Postman)
  • Compatibilidade universal
  • Usado atualmente para chaining (HTTP POST → HTTP POST)
```

**Status Atual:**
- ✅ HTTP REST **funcionando** (usado para comunicação entre agents)
- ✅ uAgents Protocol **implementado** (pronto, mas não usado ativamente)

---

## 📦 COMPONENTES

### 1. Agent Definition (Linhas 119-124)

```python
intake_agent = Agent(
    name="intake_agent",
    seed="cypherguy_intake_seed_2025_secure",
    port=8001,
    endpoint=["http://localhost:8001/submit"]
)
```

**O Que Isso Faz:**
```
✅ Cria instância do Agent usando uAgents SDK
✅ Gera address determinístico baseado no seed
✅ Configura port 8001 para uAgent server
✅ Define endpoint para receber mensagens
✅ Address gerado: agent1qw08u04nu2t9hrf88tx65sf5asf7hyd438dw93sn0hq863ducxpjv2kwvws
```

**Por Que o Seed?**
- Seed determina o address do agent
- Mesmo seed = mesmo address (reprodutível)
- Útil para registros e descoberta

---

### 2. Startup Event Handler (Linhas 127-139)

```python
@intake_agent.on_event("startup")
async def on_startup(ctx: Context):
    ctx.logger.info(f"🚀 AgentIntake iniciado!")
    ctx.logger.info(f"📍 Address: {intake_agent.address}")
    
    # Inicializar storage
    if not ctx.storage.get("sessions"):
        ctx.storage.set("sessions", {})
    
    if not ctx.storage.get("requests_count"):
        ctx.storage.set("requests_count", 0)
```

**O Que Faz:**
```
✅ Executa quando agent inicia
✅ Inicializa storage (sessões, contadores)
✅ Loga informações importantes
✅ Prepara agent para receber requests
```

---

### 3. FastAPI HTTP App (Linha 39)

```python
http_app = FastAPI(title="IntakeAgent HTTP API")
```

**O Que Faz:**
```
✅ Cria servidor HTTP separado
✅ Roda na port 8101 (thread separada)
✅ Endpoints REST para integração
✅ Independente do uAgent server (port 8001)
```

---

### 4. Pydantic Models (Linhas 42-113)

**HTTP Models (FastAPI):**
```python
class HTTPCreditRequest(PydanticBaseModel):
    user_id: str
    amount: float
    token: str
    collateral: str
```

**uAgent Models:**
```python
class CreditRequest(Model):
    user_id: str
    amount: float
    token: str
    collateral: str
    session_token: str  # Extra field para uAgent
```

**Por Que Dois?**
- HTTP: Mais simples, sem session token obrigatório
- uAgent: Mais completo, inclui session token para segurança

---

## 🔌 PROTOCOLOS (uAgents)

O IntakeAgent implementa **5 protocols** diferentes:

### 1. Authentication Protocol (Linhas 145-188)

**Propósito:** Autenticar usuários e criar sessões

```python
auth_protocol = Protocol(name="Authentication", version="1.0")

@auth_protocol.on_message(model=AuthRequest)
async def handle_auth(ctx: Context, sender: str, msg: AuthRequest):
    # Validar assinatura
    is_valid = len(msg.wallet_address) >= 32 and len(msg.signature) > 0
    
    if is_valid:
        # Gerar session token
        session_token = hashlib.sha256(...).hexdigest()
        
        # Armazenar sessão
        sessions = ctx.storage.get("sessions") or {}
        sessions[session_token] = {...}
        ctx.storage.set("sessions", sessions)
        
        # Responder
        await ctx.send(sender, AuthResponse(...))
```

**Fluxo:**
```
1. User envia AuthRequest (wallet_address + signature)
2. Agent valida assinatura (simplificado para MVP)
3. Gera session_token único
4. Armazena sessão no storage
5. Retorna AuthResponse com session_token
```

---

### 2. Credit Protocol (Linhas 194-235)

**Propósito:** Receber requisições de crédito

```python
credit_protocol = Protocol(name="CreditIntake", version="1.0")

@credit_protocol.on_message(model=CreditRequest)
async def handle_credit_request(ctx: Context, sender: str, msg: CreditRequest):
    # Validar sessão
    sessions = ctx.storage.get("sessions") or {}
    if msg.session_token not in sessions:
        return  # Invalid session
    
    # Validar amount
    if msg.amount <= 0:
        return  # Invalid amount
    
    # Armazenar request
    request_id = f"credit_{count + 1}"
    requests = ctx.storage.get("credit_requests") or {}
    requests[request_id] = {...}
    ctx.storage.set("credit_requests", requests)
```

**Fluxo:**
```
1. Recebe CreditRequest (com session_token)
2. Valida sessão
3. Valida amount > 0
4. Armazena request
5. (TODO: Enviar para PolicyAgent)
```

**Status:**
- ✅ Handler implementado
- ⚠️ Armazena request, mas não encaminha (TODO na linha 231)

---

### 3. RWA Protocol (Linhas 241-273)

**Propósito:** Receber requisições de tokenização de ativos reais

```python
rwa_protocol = Protocol(name="RWAIntake", version="1.0")

@rwa_protocol.on_message(model=RWARequest)
async def handle_rwa_request(ctx: Context, sender: str, msg: RWARequest):
    # Mesmo padrão: validar sessão, armazenar request
```

**Model:**
```python
class RWARequest(Model):
    user_id: str
    property_value: float
    location: str
    property_type: str
    session_token: str
```

---

### 4. Trading Protocol (Linhas 279-311)

**Propósito:** Receber requisições de trade

```python
trading_protocol = Protocol(name="TradingIntake", version="1.0")

@trading_protocol.on_message(model=TradeRequest)
async def handle_trade_request(ctx: Context, sender: str, msg: TradeRequest):
    # Recebe trade requests
```

---

### 5. Automation Protocol (Linhas 317-348)

**Propósito:** Receber requisições de automação

```python
automation_protocol = Protocol(name="AutomationIntake", version="1.0")

@automation_protocol.on_message(model=AutomationRequest)
async def handle_automation_request(ctx: Context, sender: str, msg: AutomationRequest):
    # Recebe automation requests
```

---

## 🌐 HTTP ENDPOINTS (FastAPI)

### 1. POST /process_credit (Linhas 357-395)

**Endpoint:** `http://localhost:8101/process_credit`

**Request:**
```json
{
  "user_id": "alice",
  "amount": 5000,
  "token": "USDC",
  "collateral": "SOL"
}
```

**O Que Faz:**
```python
@http_app.post("/process_credit")
async def http_process_credit(request: HTTPCreditRequest):
    # 1. Valida amount (100 - 100,000)
    if request.amount < 100 or request.amount > 100000:
        return {"success": False, "message": "Amount invalid"}
    
    # 2. Envia para PolicyAgent via HTTP
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:8102/check_credit_policy",
            json={...}
        ) as response:
            policy_result = await response.json()
            return policy_result
```

**Fluxo:**
```
Backend/Frontend
  ↓
POST /process_credit (IntakeAgent:8101)
  ↓
Validação básica
  ↓
HTTP POST → PolicyAgent:8102/check_credit_policy
  ↓
Recebe resposta do PolicyAgent
  ↓
Retorna para Backend/Frontend
```

**Por Que HTTP em vez de uAgent Protocol?**
- ✅ Mais fácil para debugging (curl, Postman)
- ✅ Compatibilidade com backend existente
- ✅ Chaining simples (HTTP → HTTP → HTTP)
- ⚠️ Ideal seria usar uAgent Protocol (futuro)

---

### 2. POST /process_rwa (Linhas 397-430)

**Endpoint:** `http://localhost:8101/process_rwa`

**Request:**
```json
{
  "user_id": "bob",
  "property_value": 1000000,
  "location": "Miami, FL",
  "property_type": "Residential"
}
```

**Fluxo:** Mesmo padrão do `/process_credit`

---

### 3. POST /process_trade (Linhas 432-458)

**Endpoint:** `http://localhost:8101/process_trade`

**Request:**
```json
{
  "user_id": "charlie",
  "sell_amount": 1000,
  "sell_token": "SOL",
  "buy_token": "USDC"
}
```

---

### 4. POST /process_automation (Linhas 460-492)

**Endpoint:** `http://localhost:8101/process_automation`

**Request:**
```json
{
  "user_id": "david",
  "portfolio_value": 50000,
  "strategy": "yield_farming"
}
```

---

### 5. GET /health (Linhas 494-497)

**Endpoint:** `http://localhost:8101/health`

**Response:**
```json
{
  "status": "healthy",
  "agent": "intake"
}
```

**Uso:** Health checks, monitoring

---

## 💬 ASI:ONE CHAT PROTOCOL (Linhas 503-641)

### O Que É?

Protocolo padrão da ASI Alliance para agentes conversarem com humanos via interface ASI:One.

### Implementação Completa

```python
# Importar spec do protocolo
from uagents_core.contrib.protocols.chat import (
    ChatMessage,
    ChatAcknowledgement,
    StartSessionContent,
    TextContent,
    EndSessionContent,
    chat_protocol_spec,
)

# Criar protocol com spec oficial
chat_proto = Protocol(spec=chat_protocol_spec)

# Handler para mensagens
@chat_proto.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    # Sempre enviar acknowledgement
    await ctx.send(sender, ChatAcknowledgement(...))
    
    # Processar cada content item
    for item in msg.content:
        if isinstance(item, StartSessionContent):
            # Boas-vindas
            await ctx.send(sender, welcome_msg)
        
        elif isinstance(item, TextContent):
            # Parsear texto do usuário
            text_lower = item.text.lower()
            
            # Classificar intenção (NLP simples)
            if "credit" in text_lower:
                response = "💳 I can help with credit..."
            elif "rwa" in text_lower:
                response = "🏢 I can help tokenize..."
            # ...
            
            await ctx.send(sender, response)
        
        elif isinstance(item, EndSessionContent):
            # Despedida
            await ctx.send(sender, goodbye_msg)

# Publicar manifest para Agentverse
intake_agent.include(chat_proto, publish_manifest=True)
```

### Content Types

**1. StartSessionContent:**
```python
# Quando usuário abre chat no ASI:One
if isinstance(item, StartSessionContent):
    welcome_msg = create_text_chat(
        "👋 Hi! I'm CypherGuy, your DeFi assistant!\n\n"
        "I can help you with:\n"
        "💳 Private DeFi Credit\n"
        "🏢 RWA Tokenization\n"
        ...
    )
    await ctx.send(sender, welcome_msg)
```

**2. TextContent:**
```python
# Quando usuário envia mensagem
elif isinstance(item, TextContent):
    text = item.text  # "I need $5000 credit"
    
    # Parsear intenção
    if "credit" in text.lower():
        # Responder sobre crédito
        response = create_text_chat("💳 I can help...")
        await ctx.send(sender, response)
```

**3. EndSessionContent:**
```python
# Quando usuário fecha chat
elif isinstance(item, EndSessionContent):
    goodbye_msg = create_text_chat("👋 Thanks for using CypherGuy!")
    await ctx.send(sender, goodbye_msg)
```

### Natural Language Parsing (Linhas 552-615)

**Método:** Keyword matching (simples mas funcional)

```python
text_lower = item.text.lower()

if any(word in text_lower for word in ["credit", "loan", "borrow"]):
    # Credit intent
    response = "💳 I can help with credit..."

elif any(word in text_lower for word in ["rwa", "tokenize", "property"]):
    # RWA intent
    response = "🏢 I can help tokenize..."

elif any(word in text_lower for word in ["trade", "swap", "exchange"]):
    # Trade intent
    response = "🌑 I can help trade..."

elif any(word in text_lower for word in ["automat", "optimize", "manage"]):
    # Automation intent
    response = "🤖 I can optimize portfolio..."

else:
    # Default response
    response = "I can help with credit, rwa, trade, automation..."
```

**Melhorias Futuras:**
- ⏳ Usar LLM para parsing mais inteligente
- ⏳ Intent classification com ML
- ⏳ Context awareness

---

## 🔄 FLUXOS DE DADOS

### Fluxo 1: HTTP Request (Credit)

```
┌─────────────────────────────────────────────────────┐
│  Backend/Frontend                                    │
│  POST /process_credit                                │
│  {"user_id": "alice", "amount": 5000, ...}         │
└─────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│  IntakeAgent:8101                                    │
│  POST /process_credit handler                        │
│  • Valida amount (100-100k)                         │
│  • Cria HTTP request                                 │
└─────────────────────────────────────────────────────┘
                    │
                    ▼
         aiohttp.ClientSession
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│  PolicyAgent:8102                                    │
│  POST /check_credit_policy                           │
│  • Valida policy                                     │
│  • Retorna {approved: true, rate: 5.5}             │
└─────────────────────────────────────────────────────┘
                    │
                    ▼
         Response volta
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│  IntakeAgent:8101                                    │
│  Retorna policy_result para caller                  │
└─────────────────────────────────────────────────────┘
```

### Fluxo 2: ASI:One Chat

```
┌─────────────────────────────────────────────────────┐
│  User no ASI:One                                     │
│  Digita: "I need $5000 credit"                      │
└─────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│  ASI:One Interface                                   │
│  Envia ChatMessage com TextContent                  │
└─────────────────────────────────────────────────────┘
                    │
                    ▼
         uAgent Protocol
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│  IntakeAgent (uAgent:8001)                           │
│  handle_chat_message()                               │
│  • Recebe ChatMessage                                │
│  • Envia ChatAcknowledgement                         │
│  • Parseia "credit" no texto                         │
│  • Responde: "💳 I can help..."                     │
└─────────────────────────────────────────────────────┘
                    │
                    ▼
         ChatMessage response
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│  ASI:One Interface                                   │
│  Mostra resposta para usuário                       │
└─────────────────────────────────────────────────────┘
```

---

## 💾 STORAGE

O IntakeAgent usa `ctx.storage` para persistência:

### Dados Armazenados:

**1. Sessions (Linha 161):**
```python
sessions = {
    "session_token_abc123": {
        "user_id": "alice",
        "wallet_address": "7aesM19NoQ...",
        "created_at": 1727625000.0
    },
    ...
}
```

**2. Requests Count (Linha 208):**
```python
requests_count = 42  # Contador global
```

**3. Credit Requests (Linha 218):**
```python
credit_requests = {
    "credit_1": {
        "user_id": "alice",
        "amount": 5000,
        "token": "USDC",
        "collateral": "SOL",
        "status": "pending",
        "timestamp": 1727625000.0
    },
    ...
}
```

**4. RWA Requests (Linha 260):**
```python
rwa_requests = {...}
```

**5. Trade Requests (Linha 298):**
```python
trade_requests = {...}
```

**6. Automation Requests (Linha 336):**
```python
automation_requests = {...}
```

**Storage Type:**
- ✅ Persistente (sobrevive a restarts)
- ✅ Key-value store simples
- ✅ Thread-safe

---

## 🚀 COMO FUNCIONA NA PRÁTICA

### Exemplo Real: Request de Crédito

**1. Backend envia HTTP request:**
```bash
curl -X POST http://localhost:8101/process_credit \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "alice",
    "amount": 5000,
    "token": "USDC",
    "collateral": "SOL"
  }'
```

**2. IntakeAgent recebe:**
```
INFO: 🔵 HTTP: Credit request from alice: $5000.0
```

**3. Valida:**
```python
if request.amount < 100 or request.amount > 100000:
    return {"success": False}
# Amount OK! (5000 está entre 100 e 100k)
```

**4. Envia para PolicyAgent:**
```python
async with session.post(
    "http://localhost:8102/check_credit_policy",
    json={...}
) as response:
    policy_result = await response.json()
```

**5. Recebe resposta:**
```json
{
  "success": true,
  "approved": true,
  "rate": 5.5,
  "credit_score": 750,
  ...
}
```

**6. Retorna para caller:**
```python
return policy_result  # Retorna direto do PolicyAgent
```

---

### Exemplo Real: Chat via ASI:One

**1. Usuário digita no ASI:One:**
```
"I need $5000 credit with SOL collateral"
```

**2. ASI:One envia ChatMessage:**
```python
ChatMessage(
    timestamp=datetime.utcnow(),
    msg_id=uuid4(),
    content=[
        TextContent(type="text", text="I need $5000 credit...")
    ]
)
```

**3. IntakeAgent recebe:**
```
INFO: 💬 Chat message from agent1quser...
INFO: 💬 Text from agent1quser...: I need $5000 credit...
```

**4. Parseia intenção:**
```python
if "credit" in text_lower:  # ✅ Match!
    response = create_text_chat(
        "💳 I can help you get a private DeFi loan!\n\n"
        "I'll need:\n"
        "- Amount (USDC)\n"
        "- Collateral type\n\n"
        "How much would you like to borrow?"
    )
```

**5. Envia resposta:**
```python
await ctx.send(sender, response)
```

**6. ASI:One mostra para usuário:**
```
💳 I can help you get a private DeFi loan!

I'll need:
- Amount (USDC)
- Collateral type

How much would you like to borrow?
```

---

## 📊 RESUMO TÉCNICO

### Estatísticas:
```
Total Lines:       662 linhas
Protocols:         5 (Auth, Credit, RWA, Trade, Automation)
HTTP Endpoints:    5 (/process_credit, /process_rwa, etc)
Chat Handlers:     3 (Message, Acknowledgement, Content types)
Storage Keys:      6 (sessions, requests_count, credit/rwa/trade/automation_requests)
Imports:           18 (uagents, fastapi, asyncio, etc)
```

### Dependências:
```
✅ uagents (Agent, Context, Model, Protocol)
✅ uagents_core (Chat Protocol)
✅ fastapi (HTTP server)
✅ pydantic (Type safety)
✅ uvicorn (HTTP server runner)
✅ aiohttp (HTTP client)
✅ threading (HTTP thread)
```

### Portas:
```
8001 → uAgent server (protocol messages)
8101 → HTTP server (REST API)
```

---

## ✅ PONTOS FORTES

1. ✅ **Dual-mode operation** (uAgent + HTTP)
2. ✅ **Chat Protocol completo** (ASI:One compliant)
3. ✅ **5 use cases** (Credit, RWA, Trade, Automation, Auth)
4. ✅ **Storage persistente**
5. ✅ **Error handling** básico
6. ✅ **Logging detalhado**
7. ✅ **Type-safe** (Pydantic Models)

---

## ⚠️ MELHORIAS FUTURAS

1. ⏳ **Integrar uAgent Protocol** para chaining (em vez de HTTP)
2. ⏳ **Melhorar NLP** (usar LLM para parsing)
3. ⏳ **Session management** mais robusto
4. ⏳ **Rate limiting** e security
5. ⏳ **Metrics e monitoring**
6. ⏳ pole**Unit tests**

---

**GUIA COMPLETO DO INTAKE AGENT! 🎉**

**Alguma parte específica que quer entender melhor?** 🤔


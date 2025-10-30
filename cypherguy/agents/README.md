# 🤖 CypherGuy Multi-Agent System

Sistema de 4 agentes autônomos usando **uAgents SDK** (Fetch.ai / ASI Alliance).

---

## 📋 Agentes

### 1. **AgentIntake** (Port 8001)
- **Responsabilidade:** Autenticação e parsing de requisições
- **Arquivo:** `intake_agent.py`
- **Protocols:**
  - Authentication
  - CreditIntake
  - RWAIntake
  - TradingIntake
  - AutomationIntake

### 2. **AgentPolicy** (Port 8002)
- **Responsabilidade:** Validação de regras de negócio
- **Arquivo:** `policy_agent.py`
- **Protocols:**
  - PolicyCheck
- **Rules:** Credit, RWA, Trading, Automation

### 3. **AgentCompute** (Port 8003)
- **Responsabilidade:** Computação privada (Arcium MPC mock)
- **Arquivo:** `compute_agent.py`
- **Protocols:**
  - PrivateComputation
- **Functions:** Credit scoring, RWA validation, Order matching, Portfolio optimization

### 4. **AgentExecutor** (Port 8004)
- **Responsabilidade:** Executar transações Solana
- **Arquivo:** `executor_agent.py`
- **Protocols:**
  - SolanaExecution
- **Functions:** Transaction submission, confirmation

---

## 🚀 Como Usar

### **Método 1: Scripts (Recomendado)**

```bash
# Instalar dependências
pip install -r requirements.txt

# Iniciar todos agents
./scripts/start_agents.sh

# Verificar status
./scripts/check_agents.sh

# Parar todos agents
./scripts/stop_agents.sh
```

### **Método 2: Manual (Desenvolvimento)**

```bash
# Terminal 1 - AgentIntake
python agents/intake_agent.py

# Terminal 2 - AgentPolicy
python agents/policy_agent.py

# Terminal 3 - AgentCompute
python agents/compute_agent.py

# Terminal 4 - AgentExecutor
python agents/executor_agent.py
```

---

## 📝 Verificar que Está Funcionando

### **Checar processos:**
```bash
ps aux | grep agent
```

### **Checar portas:**
```bash
lsof -i :8001  # AgentIntake
lsof -i :8002  # AgentPolicy
lsof -i :8003  # AgentCompute
lsof -i :8004  # AgentExecutor
```

### **Ver logs:**
```bash
# Logs em tempo real
tail -f ~/.uagents/intake_agent/agent.log
tail -f ~/.uagents/policy_agent/agent.log
tail -f ~/.uagents/compute_agent/agent.log
tail -f ~/.uagents/executor_agent/agent.log

# Ver todos os logs
tail -f ~/.uagents/*/agent.log
```

---

## 🔗 Fluxo de Comunicação

```
User Request
    ↓
AgentIntake (Auth + Parsing)
    ↓
AgentPolicy (Rules Validation)
    ↓
AgentCompute (Private Computation)
    ↓
AgentExecutor (Solana TX)
    ↓
Response to User
```

---

## 🧪 Testes

### **Teste Individual:**
```bash
# Testar cada agent standalone
python agents/intake_agent.py
# Verificar nos logs: "AgentIntake iniciado!"
# Ctrl+C para parar
```

### **Teste Completo:**
```bash
# Rodar todos agents
./scripts/start_agents.sh

# Ver status
./scripts/check_agents.sh

# Testar via backend API
cd backend
python main.py
```

---

## 🐛 Troubleshooting

### **Erro: Port already in use**
```bash
# Matar processo na porta
lsof -ti:8001 | xargs kill -9
# ou
./scripts/stop_agents.sh
```

### **Erro: ModuleNotFoundError: No module named 'uagents'**
```bash
pip install uagents
```

### **Erro: Agent não inicia**
```bash
# Verificar logs
cat ~/.uagents/intake_agent/agent.log

# Verificar Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### **Erro: Agents não se comunicam**
```bash
# Copiar agent addresses dos logs quando iniciarem
# Atualizar addresses no código onde houver TODO

# Exemplo de log:
# "📍 Address: agent1q2kxet3vh0scsf0sm7y2erzz33cve6tv5uk63x64upw5g68fr0xzddfpz8"
```

---

## 📊 Status dos Agents

| Agent | Port | Status | Address |
|-------|------|--------|---------|
| AgentIntake | 8001 | ⏳ Pending | `agent1q...` |
| AgentPolicy | 8002 | ⏳ Pending | `agent1q...` |
| AgentCompute | 8003 | ⏳ Pending | `agent1q...` |
| AgentExecutor | 8004 | ⏳ Pending | `agent1q...` |

**Atualizar addresses acima depois de rodar agents pela primeira vez!**

---

## 🔑 Próximos Passos

### **Após agents rodarem:**
1. ✅ Copiar agent addresses dos logs
2. ✅ Atualizar `backend/services/agent_client.py` com addresses
3. ✅ Implementar comunicação real entre agents (atualmente mock)
4. ✅ Testar message passing
5. ✅ Integrar com backend FastAPI
6. ✅ Conectar frontend

### **Para comunicação real entre agents:**
```python
# No AgentIntake, enviar mensagem para PolicyAgent:
POLICY_AGENT_ADDRESS = "agent1q..."  # Copiar do log do PolicyAgent

await ctx.send(
    POLICY_AGENT_ADDRESS,
    PolicyCheckRequest(
        request_type="credit",
        user_id=msg.user_id,
        data={"amount": msg.amount, ...}
    )
)
```

---

## 📚 Referências

- **uAgents SDK:** https://docs.fetch.ai/uAgents/
- **ASI Alliance:** https://superintelligence-ux.com/
- **Fetch.ai GitHub:** https://github.com/fetchai/uAgents

---

**Status:** 🟢 Implementado e pronto para testar  
**Next:** Instalar deps e rodar agents!


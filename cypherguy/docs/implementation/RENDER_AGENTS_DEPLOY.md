# 🚀 Deploy dos 4 Agents no Render

Guia passo a passo para fazer deploy dos agents (Intake, Policy, Compute, Executor) no Render para torná-los públicos e descobertos pelo ASI:One.

> ⚠️ **CRÍTICO PARA HACKATHON:** "All agents must be registered on Agentverse with the Chat Protocol enabled to be discoverable through ASI:One."  
> Sem deploy público, não atendemos este critério!

---

## 📋 Visão Geral

Vamos criar **4 serviços separados no Render**, um para cada agent:

| Agent | Porta HTTP | URL |
|-------|------------|-----|
| **IntakeAgent** | 8101 | `https://intake-agent.onrender.com` |
| **PolicyAgent** | 8102 | `https://policy-agent.onrender.com` |
| **ComputeAgent** | 8103 | `https://compute-agent.onrender.com` |
| **ExecutorAgent** | 8104 | `https://executor-agent.onrender.com` |

**Custo:** Gratuito (Free tier do Render)

**Tempo:** ~30-45 minutos (para os 4 agents)

---

## ⚙️ Pré-requisitos

1. Conta no Render: https://render.com (GitHub login)
2. Repositório GitHub conectado
3. Requirements.txt no lugar certo (já temos em `backend/requirements.txt`)

---

## 🔧 Passo 1: Ajustar Agents para Render

Os agents precisam usar `$PORT` do Render ao invés de porta fixa.

### IntakeAgent

**Arquivo:** `agents/intake_agent.py`

**Alteração necessária:**
```python
# Na função run_http_server(), linha ~873
def run_http_server():
    """Rodar HTTP server em thread separada"""
    import os
    port = int(os.getenv("PORT", "8101"))  # Usar $PORT do Render ou default 8101
    uvicorn.run(http_app, host="0.0.0.0", port=port, log_level="info")
```

### PolicyAgent

**Arquivo:** `agents/policy_agent.py`

**Alteração necessária:**
```python
# Na função run_http_server(), linha ~527
def run_http_server():
    """Rodar HTTP server em thread separada"""
    import os
    port = int(os.getenv("PORT", "8102"))  # Usar $PORT do Render ou default 8102
    uvicorn.run(http_app, host="0.0.0.0", port=port, log_level="info")
```

### ComputeAgent

**Arquivo:** `agents/compute_agent.py`

**Alteração necessária:**
```python
# Na função run_http_server(), linha ~538
def run_http_server():
    """Rodar HTTP server em thread separada"""
    import os
    port = int(os.getenv("PORT", "8103"))  # Usar $PORT do Render ou default 8103
    uvicorn.run(http_app, host="0.0.0.0", port=port, log_level="info")
```

### ExecutorAgent

**Arquivo:** `agents/executor_agent.py`

**Alteração necessária:**
```python
# Na função run_http_server(), linha ~424
def run_http_server():
    """Rodar HTTP server em thread separada"""
    import os
    port = int(os.getenv("PORT", "8104"))  # Usar $PORT do Render ou default 8104
    uvicorn.run(http_app, host="0.0.0.0", port=port, log_level="info")
```

---

## 🔧 Passo 2: Criar requirements.txt para Agents

Os agents precisam de um `requirements.txt` na raiz do projeto ou no diretório `agents/`.

**Opção A:** Copiar `backend/requirements.txt` para `agents/requirements.txt`

**Opção B:** Usar o mesmo `requirements.txt` da raiz (se existir)

---

## 🚀 Passo 3: Criar 4 Serviços no Render

### Serviço 1: IntakeAgent

**Configurações no Render:**

- **Name:** `cypherguy-intake-agent`
- **Environment:** `Python 3`
- **Region:** `Oregon (US West)` (ou mais próximo)
- **Branch:** `main`
- **Root Directory:** `agents`
- **Build Command:** `pip install -r requirements.txt` (ou deixe em branco se o requirements.txt estiver em agents/)
- **Start Command:** `python intake_agent.py`  
  > **Nota:** Como o Root Directory é `agents/`, o Python já está na pasta correta. O `sys.path.insert` nos agents garante que os imports de `tools/` e `metta/` funcionem corretamente.
- **Instance Type:** `Free`

**Variáveis de Ambiente:**
```
PORT=8101
PERPLEXITY_API_KEY=your_key_here (opcional)
```

**Após deploy:**
- URL será: `https://cypherguy-intake-agent.onrender.com`
- Health check: `https://cypherguy-intake-agent.onrender.com/health`

---

### Serviço 2: PolicyAgent

**Configurações no Render:**

- **Name:** `cypherguy-policy-agent`
- **Environment:** `Python 3`
- **Region:** `Oregon (US West)`
- **Branch:** `main`
- **Root Directory:** `agents`
- **Build Command:** `pip install -r requirements.txt` (ou deixe em branco se o requirements.txt estiver em agents/)
- **Start Command:** `python policy_agent.py`  
  > **Nota:** O Render executa na pasta `agents/`, então `python policy_agent.py` funciona diretamente.
- **Instance Type:** `Free`

**Variáveis de Ambiente:**
```
PORT=8102
```

**Após deploy:**
- URL será: `https://cypherguy-policy-agent.onrender.com`
- Health check: `https://cypherguy-policy-agent.onrender.com/health`

---

### Serviço 3: ComputeAgent

**Configurações no Render:**

- **Name:** `cypherguy-compute-agent`
- **Environment:** `Python 3`
- **Region:** `Oregon (US West)`
- **Branch:** `main`
- **Root Directory:** `agents`
- **Build Command:** `pip install -r requirements.txt` (ou deixe em branco se o requirements.txt estiver em agents/)
- **Start Command:** `python compute_agent.py`  
  > **Nota:** Os imports de `tools/` são resolvidos automaticamente via `sys.path.insert` no início do arquivo.
- **Instance Type:** `Free`

**Variáveis de Ambiente:**
```
PORT=8103
```

**Após deploy:**
- URL será: `https://cypherguy-compute-agent.onrender.com`
- Health check: `https://cypherguy-compute-agent.onrender.com/health`

---

### Serviço 4: ExecutorAgent

**Configurações no Render:**

- **Name:** `cypherguy-executor-agent`
- **Environment:** `Python 3`
- **Region:** `Oregon (US West)`
- **Branch:** `main`
- **Root Directory:** `agents`
- **Build Command:** `pip install -r requirements.txt` (ou deixe em branco se o requirements.txt estiver em agents/)
- **Start Command:** `python executor_agent.py`  
  > **Nota:** Mesmo padrão dos outros agents - funciona com Root Directory `agents/`.
- **Instance Type:** `Free`

**Variáveis de Ambiente:**
```
PORT=8104
```

**Após deploy:**
- URL será: `https://cypherguy-executor-agent.onrender.com`
- Health check: `https://cypherguy-executor-agent.onrender.com/health`

---

## 🔗 Passo 4: Atualizar Backend

Após fazer deploy dos 4 agents, atualize as variáveis de ambiente do **backend** no Render:

```
CORS_ORIGINS=https://seu-frontend.vercel.app
AGENT_INTAKE_URL=https://cypherguy-intake-agent.onrender.com
AGENT_POLICY_URL=https://cypherguy-policy-agent.onrender.com
AGENT_COMPUTE_URL=https://cypherguy-compute-agent.onrender.com
AGENT_EXECUTOR_URL=https://cypherguy-executor-agent.onrender.com
HTTP_TIMEOUT_SECS=30
```

---

## 🧪 Passo 5: Testar

### Teste Individual de Cada Agent

```bash
# IntakeAgent
curl https://cypherguy-intake-agent.onrender.com/health

# PolicyAgent
curl https://cypherguy-policy-agent.onrender.com/health

# ComputeAgent
curl https://cypherguy-compute-agent.onrender.com/health

# ExecutorAgent
curl https://cypherguy-executor-agent.onrender.com/health
```

### Teste do Fluxo Completo

```bash
# Via Backend (que chama os agents)
curl -X POST https://cypherguy.onrender.com/credit \
  -H "Content-Type: application/json" \
  -d '{"user_id":"demo","amount":1000,"token":"USDC","collateral":"SOL"}'
```

---

## ⚠️ Problemas Comuns

### Erro: "ModuleNotFoundError: No module named 'backend'"

**Solução:** Os agents não devem importar `backend.settings`. Já está corrigido nos imports relativos.

### Erro: "Port already in use"

**Solução:** Render usa `$PORT` automaticamente. Não definir porta fixa.

### Erro: "Agents não se comunicam"

**Solução:** Verificar URLs nas variáveis de ambiente do backend.

### Erro: "Instance spun down"

**Solução:** Free tier do Render "spins down" após inatividade. Primeira requisição pode levar 50s+.

---

## 🎯 Para ASI:One Discovery

### IntakeAgent com mailbox=True

O IntakeAgent já tem `mailbox=True`, então:
1. Ele se conecta ao Agentverse Mailbox automaticamente
2. Publica o Chat Protocol no Almanac
3. Deve aparecer no ASI:One após deploy público

**Após deploy no Render:**
- O endpoint público será: `https://cypherguy-intake-agent.onrender.com`
- O Agentverse Mailbox vai registrar este endpoint
- O ASI:One vai conseguir descobrir e conectar

---

## 📝 Checklist de Deploy

### Para cada Agent:
- [ ] Criar serviço no Render
- [ ] Configurar Root Directory: `agents`
- [ ] Configurar Build Command: `pip install -r ../backend/requirements.txt`
- [ ] Configurar Start Command: `python <agent>_agent.py`
- [ ] Adicionar variável `PORT` (opcional, Render usa automaticamente)
- [ ] Fazer deploy
- [ ] Testar health check
- [ ] Verificar logs

### Após Todos os Agents:
- [ ] Atualizar variáveis de ambiente do backend com URLs dos agents
- [ ] Testar fluxo completo via backend
- [ ] Testar descoberta no ASI:One

---

## 💰 Custo Estimado

**Free Tier do Render:**
- ✅ 750 horas gratuitas/mês
- ✅ 4 serviços = 4 × 750h = 3,000h disponíveis
- ⚠️ Instâncias "spins down" após 15 min de inatividade
- ⚠️ Primeira requisição após spin-down leva ~50s

**Para Hackathon:**
- ✅ Gratuito
- ✅ Suficiente para demo
- ⚠️ Pode ter delay no primeiro request

---

## 🚀 Próximos Passos

1. Fazer as alterações nos 4 agents (adicionar `os.getenv("PORT")`)
2. Fazer commit e push
3. Criar os 4 serviços no Render
4. Testar cada um
5. Atualizar backend com URLs dos agents
6. Testar fluxo completo

**Quer que eu faça as alterações nos agents agora?**


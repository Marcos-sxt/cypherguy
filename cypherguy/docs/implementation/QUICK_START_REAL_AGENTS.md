# ⚡ QUICK START: Agents com Comunicação Real

**Tempo:** 5 minutos  
**Resultado:** Sistema completo funcionando

---

## 🚀 PASSO-A-PASSO

### 1. Abrir 4 Terminais

```
┌─────────────────┬─────────────────┐
│   Terminal 1    │   Terminal 2    │
│  IntakeAgent    │  PolicyAgent    │
├─────────────────┼─────────────────┤
│   Terminal 3    │   Terminal 4    │
│  ComputeAgent   │  ExecutorAgent  │
└─────────────────┴─────────────────┘
```

### 2. Iniciar Agents (um por terminal)

**Terminal 1:**
```bash
cd "/home/user/Documents/SOLANA CYPHERPUNK"
source venv/bin/activate
cd cypherguy
python agents/intake_agent.py
```

**Terminal 2:**
```bash
cd "/home/user/Documents/SOLANA CYPHERPUNK"
source venv/bin/activate
cd cypherguy
python agents/policy_agent.py
```

**Terminal 3:**
```bash
cd "/home/user/Documents/SOLANA CYPHERPUNK"
source venv/bin/activate
cd cypherguy
python agents/compute_agent.py
```

**Terminal 4:**
```bash
cd "/home/user/Documents/SOLANA CYPHERPUNK"
source venv/bin/activate
cd cypherguy
python agents/executor_agent.py
```

### 3. Aguardar Inicialização

Cada terminal vai mostrar:
```
🦸 Starting Agent...
🌐 HTTP server will run on port 8101
INFO: Agent iniciado!
INFO: HTTP server started
```

**Aguarde ~10 segundos** para todos iniciarem.

### 4. Testar Health (Terminal 5)

```bash
curl http://localhost:8101/health  # Intake ✅
curl http://localhost:8102/health  # Policy ✅
curl http://localhost:8103/health  # Compute ✅
curl http://localhost:8104/health  # Executor ✅
```

### 5. Iniciar Backend (Terminal 6)

```bash
cd "/home/user/Documents/SOLANA CYPHERPUNK/cypherguy/backend"
python main.py
```

### 6. Testar End-to-End (Terminal 7)

```bash
curl -X POST "http://localhost:8000/credit" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "CB1A2B3C4D",
    "amount": 5000,
    "token": "USDC",
    "collateral": "SOL"
  }'
```

### 7. Ver Logs em Tempo Real

**Você verá nos 4 terminais dos agents:**

**Terminal 1 (Intake):**
```
🔵 HTTP: Credit request from CB1A2B3C4D: $5000.0
📤 Sending to PolicyAgent...
✅ Policy response received
```

**Terminal 2 (Policy):**
```
🛡️ HTTP: Checking credit policy for CB1A2B3C4D: $5000.0
✅ Policy APPROVED: Amount within limits
📤 Sending to ComputeAgent...
```

**Terminal 3 (Compute):**
```
🧮 HTTP: Computing credit for CB1A2B3C4D: $5000.0
✅ Computation complete: score=750, rate=5.5%
📤 Sending to ExecutorAgent...
```

**Terminal 4 (Executor):**
```
⛓️ HTTP: Executing credit transaction for CB1A2B3C4D: $5000.0
✅ TX executed: abc123...
```

**🎉 ISSO É COMUNICAÇÃO REAL!**

---

## 📱 Testar com Mobile

```bash
# Terminal 8
cd "/home/user/Documents/SOLANA CYPHERPUNK/cypherguy/mobile"
npm run web
```

Acesse http://localhost:19006 e:
1. Conecte com Tangem (modo mock)
2. Tap em "Private DeFi Credit"
3. **Veja os 4 terminais processando em tempo real!** 🔥

---

## 🎬 DEMO PARA HACKATHON

### Setup Visual

```
Monitor/Projetor:
┌──────────────────────────────────────┐
│  [Mobile App] ← Visível             │
├──────────────┬──────────────────────┤
│ Terminal 1:  │ Terminal 2:          │
│ IntakeAgent  │ PolicyAgent          │
├──────────────┼──────────────────────┤
│ Terminal 3:  │ Terminal 4:          │
│ ComputeAgent │ ExecutorAgent        │
└──────────────┴──────────────────────┘
```

### Script de Apresentação

```
1. "Vejam os 4 agents ASI Alliance rodando"

2. "Vou fazer uma requisição pelo mobile app"

3. [Tap no mobile]

4. "Observem os logs em TEMPO REAL!"
   [Apontar para cada terminal conforme aparecem mensagens]

5. "Isso não é mock! É comunicação REAL via HTTP!"

6. "IntakeAgent → PolicyAgent → ComputeAgent → ExecutorAgent"

7. "Cada agent processa sua parte e passa para o próximo"

8. "Esse é o poder do ASI Alliance Multi-Agent System!"
```

**Tempo:** ~2 minutos  
**Impacto:** 🚀 **MÁXIMO!**

---

## 🐛 Se Algo Der Errado

### Agents não iniciam
```bash
# Verificar conflitos de porta
pkill -f "agent.py"
# Tentar novamente
```

### Backend não conecta aos agents
```bash
# Verificar se 4 agents estão rodando
ps aux | grep agent.py | grep -v grep
# Deveria listar 4 processos
```

### Mobile não conecta ao backend
```bash
# Verificar backend
curl http://localhost:8000/
```

---

## ✅ CHECKLIST ANTES DA DEMO

- [ ] 4 agents rodando (terminais 1-4)
- [ ] Health check OK em todos
- [ ] Backend rodando (terminal 6)
- [ ] Mobile rodando (terminal 8)
- [ ] Teste end-to-end funcionando
- [ ] Logs visíveis em todos terminais
- [ ] Screen recording como backup

---

## 🎯 RESULTADO ESPERADO

Quando tudo funciona, você verá:
- ✅ 4 agents logando em tempo real
- ✅ Mensagens passando de um para outro
- ✅ Response final chegando no mobile
- ✅ **DEMO IMPRESSIONANTE!** 🔥

---

**Bora ganhar esse hackathon! 🏆**


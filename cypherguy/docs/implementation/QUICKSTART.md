# 🚀 CypherGuy ASI Agents - QUICKSTART

**Para começar AGORA em 5 minutos!**

---

## ⚡ Setup Rápido

```bash
# 1. Navegar para o projeto
cd /home/user/Documents/SOLANA\ CYPHERPUNK/cypherguy

# 2. Criar estrutura
mkdir -p agents/protocols backend/services tests scripts

# 3. Criar __init__.py
touch agents/__init__.py
touch agents/protocols/__init__.py
touch backend/services/__init__.py

# 4. Instalar dependências
pip install uagents>=0.9.3

# 5. Verificar instalação
python -c "import uagents; print(f'✅ uAgents {uagents.__version__} instalado!')"
```

---

## 📝 Criar Agents (Copiar código do plano)

### **Agent 1: intake_agent.py**
```bash
# Copiar código do plano de implementação para:
# agents/intake_agent.py
```

### **Agent 2: policy_agent.py**
```bash
# Copiar código do plano de implementação para:
# agents/policy_agent.py
```

### **Agent 3: compute_agent.py**
```bash
# Copiar código do plano de implementação para:
# agents/compute_agent.py
```

### **Agent 4: executor_agent.py**
```bash
# Copiar código do plano de implementação para:
# agents/executor_agent.py
```

---

## 🏃 Rodar Agents

### **Opção 1: Terminal Separado (Desenvolvimento)**

```bash
# Terminal 1
cd cypherguy
python agents/intake_agent.py

# Terminal 2
python agents/policy_agent.py

# Terminal 3
python agents/compute_agent.py

# Terminal 4
python agents/executor_agent.py
```

### **Opção 2: Script Único (Produção)**

```bash
# Criar script
cat > scripts/start_agents.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting CypherGuy Agents..."
python agents/intake_agent.py &
sleep 2
python agents/policy_agent.py &
sleep 2
python agents/compute_agent.py &
sleep 2
python agents/executor_agent.py &
echo "✅ All agents running!"
EOF

# Dar permissão
chmod +x scripts/start_agents.sh

# Executar
./scripts/start_agents.sh
```

---

## ✅ Verificar que Está Funcionando

### **Checklist Rápido:**

```bash
# 1. Verificar processos rodando
ps aux | grep agent

# 2. Verificar portas abertas
lsof -i :8001  # AgentIntake
lsof -i :8002  # AgentPolicy
lsof -i :8003  # AgentCompute
lsof -i :8004  # AgentExecutor

# 3. Verificar logs
tail -f ~/.uagents/intake_agent/agent.log
```

### **Teste Manual:**

```python
# test_agents.py
import asyncio
from uagents import Agent, Model

class TestMessage(Model):
    content: str

async def test_intake():
    print("🧪 Testing AgentIntake...")
    # TODO: Implementar teste
    print("✅ AgentIntake OK!")

if __name__ == "__main__":
    asyncio.run(test_intake())
```

---

## 🔧 Troubleshooting Rápido

### **Erro: Port already in use**
```bash
# Matar processo na porta
lsof -ti:8001 | xargs kill -9
```

### **Erro: ModuleNotFoundError**
```bash
# Adicionar ao PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### **Erro: Agent não responde**
```bash
# Verificar logs
tail -f ~/.uagents/*/agent.log
```

---

## 📊 Status Dashboard

```bash
# Ver status de todos agents
watch -n 2 'ps aux | grep "agent.*.py" | grep -v grep'
```

---

## 🎯 Próximo Passo

Após agents rodando:
1. ✅ Testar comunicação entre agents
2. ✅ Integrar com backend FastAPI
3. ✅ Conectar frontend
4. ✅ Testar 4 use cases

---

## 📞 Se algo der errado

1. **Parar todos agents:** `pkill -f "agents/.*_agent.py"`
2. **Limpar cache:** `rm -rf ~/.uagents/*`
3. **Reinstalar:** `pip install --upgrade --force-reinstall uagents`
4. **Recomeçar:** Seguir setup rápido novamente

---

**LET'S GO! 🚀**


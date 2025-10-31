# 🎬 CypherGuy - Demo Video Script

**Duração:** 3-5 minutos  
**Foco:** UX + Decisões Técnicas + Integração Solana

---

## 📋 Estrutura do Roteiro

### 🎯 **INTRO (0:00 - 0:30)**
**Tela:** Logo + Dashboard

**Narração:**
> "Hey judges! This is CypherGuy - your Personal DeFi Assistant.  
> Built for the ASI Alliance Hackathon, CypherGuy makes complex DeFi operations as simple as chatting.  
> Let me show you what we built and why..."

**Ação:**
- Mostrar logo na tela
- Entrar no dashboard
- Highlight: Interface limpa, 4 Quick Actions

---

### 💬 **CORE UX - Natural Language Chat (0:30 - 1:30)**
**Tela:** Chat Interface

**Narração:**
> "The core innovation here is natural language interaction.  
> Instead of filling forms, you just chat with CypherGuy - like talking to a friend who knows DeFi inside and out."

**Ação:**
1. Abrir Chat
2. Digitar: "I want to borrow 1000 USDC"
3. CypherGuy responde explicando o processo
4. Mostrar conversa fluida (3-4 mensagens)
5. **Key Point:** "Notice how CypherGuy remembers context and guides you through the process naturally"

**Decisão Técnica:**
> "We use NLP to extract intent and parameters from natural language, making DeFi accessible to everyone - no technical knowledge needed."

---

### ⚡ **QUICK ACTIONS - Fast Access (1:30 - 2:00)**
**Tela:** Dashboard → Quick Actions

**Narração:**
> "For common operations, we have Quick Actions.  
> One click and you're in a conversation with a pre-filled context."

**Ação:**
1. Clicar em "Get Loan"
2. Chat abre automaticamente com mensagem pré-enviada
3. Mostrar resposta imediata

**Decisão Técnica:**
> "We use React Router state to pass context, creating a seamless flow from dashboard to action."

---

### 🤖 **MULTI-AGENT ARCHITECTURE (2:00 - 3:00)**
**Tela:** Arquitetura diagram (ou código) ou logs

**Narração:**
> "Under the hood, CypherGuy uses 4 autonomous AI agents working together:  
> - IntakeAgent handles natural language and routing  
> - PolicyAgent validates using MeTTa knowledge graphs  
> - ComputeAgent calculates credit scores privately with MPC  
> - ExecutorAgent executes transactions on Solana"

**Mostrar (opcional):**
- Diagrama simples ou
- Logs do agent system funcionando ou
- Código dos agents

**Decisão Técnica:**
> "We chose uAgents framework because it provides the ASI:One Chat Protocol out of the box, making our agents discoverable.  
> Each agent is autonomous but works together - this modularity makes the system scalable and maintainable."

---

### ⛓️ **SOLANA INTEGRATION (3:00 - 3:45)**
**Tela:** ExecutorAgent code ou Solana explorer

**Narração:**
> "All transactions execute on Solana blockchain - real, live transactions.  
> Our ExecutorAgent builds, signs, and sends transactions directly."

**Mostrar:**
- Transaction building code (brief)
- Solana Explorer link (opcional)
- Real transaction execution

**Decisão Técnica:**
> "We integrate with Solana Devnet for demo purposes.  
> The ExecutorAgent uses the official Solana Python SDK to create real transactions.  
> This isn't mock data - these are actual blockchain transactions that could run on mainnet."

---

### 🔒 **PRIVACY & MPC (3:45 - 4:15)**
**Tela:** ComputeAgent ou MPC diagram

**Narração:**
> "Privacy is built-in. Credit scoring uses Multi-Party Computation - your full portfolio stays private.  
> We simulate Arcium's MPC protocol, which would enable private computation without exposing your data."

**Decisão Técnica:**
> "Traditional DeFi loans require revealing your entire portfolio.  
> We use MPC to calculate credit scores privately - you get a loan without exposing your holdings.  
> This is a game-changer for DeFi privacy."

---

### 🎯 **ASI ALLIANCE INTEGRATION (4:15 - 4:45)**
**Tela:** Agentverse ou ASI:One

**Narração:**
> "CypherGuy agents are registered on Agentverse and discoverable via ASI:One Chat Protocol.  
> This means users can interact with CypherGuy from any ASI:One compatible app."

**Mostrar (se possível):**
- Agent manifest
- ASI:One compatibility
- Mailbox connection

**Decisão Técnica:**
> "We leverage ASI Alliance's infrastructure - Agentverse for discovery and ASI:One Protocol for chat.  
> This means CypherGuy works in the ASI ecosystem, not just our own app."

---

### 🏁 **WRAP-UP (4:45 - 5:00)**
**Tela:** Dashboard completo

**Narração:**
> "So that's CypherGuy - making DeFi accessible through natural language, powered by autonomous agents, and integrated with Solana.  
> Thanks for watching!"

**Ação:**
- Fade out com logo
- GitHub link
- Demo URL

---

## 🎥 **SHOTS TO CAPTURE**

### Must Have:
1. ✅ Dashboard com Quick Actions
2. ✅ Chat natural language (2-3 exemplos)
3. ✅ Quick Action → Chat flow
4. ✅ Conversa longa (credit flow completo)
5. ✅ Code snippets (agents, Solana)

### Nice to Have:
1. Agent logs funcionando
2. Solana Explorer transaction
3. Agentverse registration
4. Architecture diagram

---

## 💡 **KEY MESSAGES TO EMPHASIZE**

1. **"Natural Language makes DeFi accessible"** - UX first
2. **"Multi-Agent Architecture is scalable"** - Technical decision
3. **"Real Solana transactions"** - Not mocked
4. **"Privacy through MPC"** - Innovation
5. **"ASI Alliance compatible"** - Ecosystem integration

---

## ⏱️ **TIMING BREAKDOWN**

| Seção | Tempo | Prioridade |
|-------|-------|------------|
| Intro | 0:30 | High |
| Core UX (Chat) | 1:00 | **Critical** |
| Quick Actions | 0:30 | High |
| Multi-Agent | 1:00 | **Critical** |
| Solana | 0:45 | **Critical** |
| Privacy/MPC | 0:30 | Medium |
| ASI Integration | 0:30 | High |
| Wrap-up | 0:15 | High |
| **TOTAL** | **5:00** | |

---

## 🎬 **PRODUCTION TIPS**

1. **Screen Recording:** Use OBS ou simples screen recorder
2. **Audio:** Claro, sem ruído de fundo
3. **Pace:** Não corra - deixe o UX brilhar
4. **Zoom:** Highlight áreas importantes (chat, code)
5. **Transitions:** Suaves entre seções
6. **Text Overlays:** Use para destacar decisões técnicas

---

## 📝 **SCRIPT NOTES**

- **Tom:** Profissional mas entusiasmado
- **Linguagem:** Técnica mas acessível
- **Foco:** Por que construímos assim, não apenas o que faz
- **Real-time:** Mostrar funcionando, não apenas explicar

---

## 🎯 **SUBMISSION CHECKLIST**

- [ ] Vídeo mostra core functionality
- [ ] Decisões técnicas explicadas
- [ ] Solana integration demonstrada
- [ ] UX brilha (natural language)
- [ ] Duração: 3-5 minutos
- [ ] Áudio claro
- [ ] Boa qualidade de vídeo
- [ ] Upload para YouTube/Vimeo
- [ ] Link pronto para submission

---

**Boa sorte com o vídeo! 🚀**


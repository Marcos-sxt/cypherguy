# 🚀 Guia de Deploy - CypherGuy

Configurações para deploy no **Vercel (Frontend)** e **Render (Backend)**.

---

## 📱 Frontend (Vercel)

### Configurações Necessárias

**Root Directory:** `frontend`

**Build Settings:**
- **Framework Preset:** `Vite`
- **Build Command:** `npm run build`
- **Output Directory:** `dist`
- **Install Command:** `npm install` (ou deixe em branco para usar o default)

**Variáveis de Ambiente no Vercel:**
```
VITE_API_URL=https://cypherguy-backend.onrender.com
```
*(Substitua pela URL do seu backend no Render)*

### Arquivos Criados

- ✅ `frontend/vercel.json` - Configuração do Vercel

### Verificações

- ✅ `package.json` tem script `build: vite build`
- ✅ `vite.config.ts` está configurado corretamente
- ⚠️ **FALTA:** Service/API client no frontend para chamar o backend
- ⚠️ **FALTA:** Variável `VITE_API_URL` sendo usada no código

---

## ⚙️ Backend (Render)

### Configurações Necessárias

**Root Directory:** `backend`

**Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Build Command:** `pip install -r requirements.txt` (deixe em branco se o requirements.txt estiver no backend)

**Runtime:** `Python 3`

### Variáveis de Ambiente no Render

```
CORS_ORIGINS=https://cypherguy.vercel.app,https://cypherguy.vercel.app/*
AGENT_INTAKE_URL=http://localhost:8101
AGENT_POLICY_URL=http://localhost:8102
AGENT_COMPUTE_URL=http://localhost:8103
AGENT_EXECUTOR_URL=http://localhost:8104
HTTP_TIMEOUT_SECS=30
```

**Nota:** Os agents (8101-8104) precisam estar rodando separadamente. O backend funciona sem eles, mas os endpoints que dependem dos agents não funcionarão.

### Verificações

- ✅ `requirements.txt` está em `backend/requirements.txt` (copiado da raiz)
- ✅ `backend/main.py` usa uvicorn
- ✅ `backend/settings.py` lê variáveis de ambiente
- ✅ CORS está configurado com `CORS_ORIGINS`
- ✅ Port usa `$PORT` (variável do Render)

---

## 🔧 O Que Falta Configurar

### 1. **Frontend - API Client** ⚠️

O frontend ainda não tem um service para chamar o backend. Precisa criar:

```typescript
// frontend/src/services/api.ts
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = {
  async health() {
    const res = await fetch(`${API_URL}/health`);
    return res.json();
  },
  // ... outros endpoints
};
```

### 2. **Backend - URL do Frontend** ⚠️

Após fazer deploy do frontend no Vercel, atualize `CORS_ORIGINS` no Render com a URL real:
```
CORS_ORIGINS=https://cypherguy-frontend.vercel.app
```

### 3. **Agents** ⚠️

Os 4 agents precisam estar rodando (portas 8101-8104) para os endpoints funcionarem completamente. Eles podem ser:
- Deployados separadamente no Render (4 serviços)
- Ou rodados localmente durante desenvolvimento

---

## ✅ Checklist de Deploy

### Frontend (Vercel)
- [ ] Repositório conectado
- [ ] Root Directory: `frontend`
- [ ] Build Command: `npm run build`
- [ ] Output Directory: `dist`
- [ ] Variável `VITE_API_URL` configurada
- [ ] [ ] Deploy testado
- [ ] URL do frontend copiada para backend CORS

### Backend (Render)
- [ ] Repositório conectado
- [ ] Root Directory: `backend`
- [ ] Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] Build Command configurado (se necessário)
- [ ] Runtime: Python 3
- [ ] Variáveis de ambiente configuradas
- [ ] `CORS_ORIGINS` atualizado com URL do frontend
- [ ] Deploy testado
- [ ] Health check funcionando

---

## 🧪 Testes Após Deploy

### Frontend
```bash
curl https://cypherguy.vercel.app
# Deve retornar HTML da aplicação
```

### Backend
```bash
curl https://cypherguy-backend.onrender.com/health
# Deve retornar: {"status": "healthy", "service": "cypherguy-backend"}
```

---

**Status Atual:**
- ✅ Frontend: Configurado para Vercel
- ✅ Backend: Configurado para Render
- ⚠️ Frontend precisa de API client
- ⚠️ CORS precisa ser atualizado após deploy


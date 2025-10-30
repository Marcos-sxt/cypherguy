# 🚀 Jupiter Ultra Swap - Plano de Implementação

**Data:** 2025-10-28

---

## 🎯 ESTRATÉGIA: Via Tool (Recomendado!)

### Por que Tool?

```python
✅ Consistência com arquitetura existente
   - SolanaRPCTool ✅
   - JupiterPriceTool ✅
   - JupiterUltraSwapTool ← NOVO!

✅ Separação de responsabilidades
   - ComputeAgent orquestra
   - Tools fazem o trabalho pesado

✅ Reutilizável
   - Qualquer agent pode usar
   - Fácil de testar isoladamente

✅ Error handling centralizado
   - Fallback automático
   - Logs consistentes
```

---

## 🏗️ ARQUITETURA PROPOSTA

```
┌─────────────────────────────────────────────────────────┐
│  ComputeAgent                                           │
│  ────────────                                           │
│                                                         │
│  ToolRegistry:                                          │
│    • SolanaRPCTool        (balance, TXs)               │
│    • JupiterPriceTool     (prices)                     │
│    • JupiterUltraSwapTool (swaps) ← NOVO!              │
│                                                         │
│  Use Case: Dark Pool Trading                           │
│    1. Get price via JupiterPriceTool                   │
│    2. Create order via JupiterUltraSwapTool.order()    │
│    3. Execute order via JupiterUltraSwapTool.execute() │
│    4. Return TX to ExecutorAgent                       │
└─────────────────────────────────────────────────────────┘
```

---

## 📝 CÓDIGO DA TOOL

### Estrutura da Tool

```python
# tools/defi_tools.py

class JupiterUltraSwapTool(Tool):
    """
    Tool para executar swaps via Jupiter Ultra API
    RPC-less, Jupiter cuida de tudo!
    """
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            name="jupiter_ultra_swap",
            description="Execute token swaps via Jupiter Ultra API (RPC-less)"
        )
        self.base_url = "https://api.jup.ag/ultra"
        self.api_key = api_key  # Optional, for higher rate limits
        
    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Execute Jupiter Ultra Swap actions
        
        Actions:
          - "order"   : Get best quote and order ID
          - "execute" : Execute the swap
          - "status"  : Check order status
        """
        if action == "order":
            return await self._create_order(**kwargs)
        elif action == "execute":
            return await self._execute_order(**kwargs)
        elif action == "status":
            return await self._check_status(**kwargs)
        else:
            return {"success": False, "error": f"Unknown action: {action}"}
    
    async def _create_order(
        self,
        input_mint: str,
        output_mint: str,
        amount: int,
        slippage_bps: int = 50,
        user_public_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        POST /ultra/order
        Get best quote and create order
        """
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "inputMint": input_mint,
                    "outputMint": output_mint,
                    "amount": amount,
                    "slippageBps": slippage_bps
                }
                
                if user_public_key:
                    payload["userPublicKey"] = user_public_key
                
                headers = {"Content-Type": "application/json"}
                if self.api_key:
                    headers["Authorization"] = f"Bearer {self.api_key}"
                
                async with session.post(
                    f"{self.base_url}/order",
                    json=payload,
                    headers=headers,
                    timeout=10
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"❌ Ultra order failed: {error_text}")
                        return {
                            "success": False,
                            "error": f"Status {response.status}",
                            "details": error_text
                        }
                    
                    data = await response.json()
                    
                    logger.info(f"✅ Ultra order created: {data.get('orderId', 'N/A')}")
                    logger.info(f"💱 Quote: {amount} → {data.get('outAmount', 0)}")
                    
                    return {
                        "success": True,
                        "order_id": data.get("orderId"),
                        "in_amount": amount,
                        "out_amount": data.get("outAmount"),
                        "price_impact": data.get("priceImpact"),
                        "route": data.get("route"),
                        "expires_at": data.get("expiresAt")
                    }
        
        except Exception as e:
            logger.error(f"❌ Error creating Ultra order: {e}")
            return {"success": False, "error": str(e)}
    
    async def _execute_order(
        self,
        order_id: str,
        user_public_key: str,
        signed_transaction: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        POST /ultra/execute
        Execute the swap order
        
        If signed_transaction is provided, Jupiter will broadcast it.
        Otherwise, Jupiter returns unsigned TX for you to sign.
        """
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "orderId": order_id,
                    "userPublicKey": user_public_key
                }
                
                if signed_transaction:
                    payload["signedTransaction"] = signed_transaction
                
                headers = {"Content-Type": "application/json"}
                if self.api_key:
                    headers["Authorization"] = f"Bearer {self.api_key}"
                
                async with session.post(
                    f"{self.base_url}/execute",
                    json=payload,
                    headers=headers,
                    timeout=30  # Longer timeout for execution
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"❌ Ultra execute failed: {error_text}")
                        return {
                            "success": False,
                            "error": f"Status {response.status}",
                            "details": error_text
                        }
                    
                    data = await response.json()
                    
                    logger.info(f"✅ Ultra swap executed!")
                    logger.info(f"🔗 TX: {data.get('signature', 'pending')}")
                    
                    return {
                        "success": True,
                        "signature": data.get("signature"),
                        "status": data.get("status"),
                        "in_amount": data.get("inAmount"),
                        "out_amount": data.get("outAmount"),
                        "fee": data.get("fee")
                    }
        
        except Exception as e:
            logger.error(f"❌ Error executing Ultra order: {e}")
            return {"success": False, "error": str(e)}
    
    async def _check_status(self, order_id: str) -> Dict[str, Any]:
        """
        GET /ultra/status/{orderId}
        Check order status
        """
        try:
            async with aiohttp.ClientSession() as session:
                headers = {}
                if self.api_key:
                    headers["Authorization"] = f"Bearer {self.api_key}"
                
                async with session.get(
                    f"{self.base_url}/status/{order_id}",
                    headers=headers,
                    timeout=5
                ) as response:
                    if response.status != 200:
                        return {"success": False, "error": f"Status {response.status}"}
                    
                    data = await response.json()
                    return {"success": True, **data}
        
        except Exception as e:
            logger.error(f"❌ Error checking Ultra status: {e}")
            return {"success": False, "error": str(e)}
```

---

## 🔧 INTEGRAÇÃO NO COMPUTEAGENT

```python
# agents/compute_agent.py

# Import new tool
from tools.defi_tools import JupiterPriceTool, JupiterUltraSwapTool

# Register tool
try:
    tools.register(JupiterUltraSwapTool())
    logger.info("✅ Jupiter Ultra Swap Tool registered")
except Exception as e:
    logger.warning(f"⚠️ Failed to register Jupiter Ultra Swap Tool: {e}")

# Use in Dark Pool Trading
async def compute_dark_pool_trade_with_tools(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute dark pool trade using Jupiter Ultra Swap
    """
    input_token = data.get("input_token", "SOL")
    output_token = data.get("output_token", "USDC")
    amount = data.get("amount", 0)
    wallet = data.get("wallet_address")
    
    logger.info(f"💱 Dark Pool Trade: {amount} {input_token} → {output_token}")
    
    # Step 1: Get current price
    price_result = await tools.execute(
        "jupiter_price",
        token=input_token
    )
    
    if not price_result.get("success"):
        return {"success": False, "error": "Failed to get price"}
    
    current_price = price_result.get("price_usd")
    logger.info(f"💵 Current {input_token} price: ${current_price}")
    
    # Step 2: Create swap order via Ultra
    order_result = await tools.execute(
        "jupiter_ultra_swap",
        action="order",
        input_mint=get_token_mint(input_token),
        output_mint=get_token_mint(output_token),
        amount=amount,
        slippage_bps=50,
        user_public_key=wallet
    )
    
    if not order_result.get("success"):
        return {"success": False, "error": "Failed to create order"}
    
    order_id = order_result.get("order_id")
    out_amount = order_result.get("out_amount")
    
    logger.info(f"✅ Order created: {order_id}")
    logger.info(f"💱 Will receive: {out_amount} {output_token}")
    
    # Step 3: Execute order (in real scenario, need signed TX)
    # For now, return order details to ExecutorAgent
    return {
        "success": True,
        "order_id": order_id,
        "input_amount": amount,
        "output_amount": out_amount,
        "current_price": current_price,
        "ready_to_execute": True,
        "message": f"Order ready: {amount} {input_token} → {out_amount} {output_token}"
    }
```

---

## 🎯 VANTAGENS DA ULTRA API

### O Que Jupiter Cuida (Automaticamente!)

```
✅ RPC Management
   - Não precisa do seu próprio RPC node
   - Jupiter cuida de balances, broadcasting, tracking

✅ Transaction Fees
   - Priority fees automáticas
   - Jito integration (MEV protection)
   - Dynamic fee optimization

✅ Slippage Optimization
   - Calcula melhor slippage automaticamente
   - Balance entre sucesso e proteção

✅ Transaction Broadcasting
   - Proprietary transaction engine
   - Superior speed & reliability
   - Retry logic built-in

✅ Result Parsing
   - Transaction polling automático
   - Error handling
   - Status tracking
```

### Comparação: Ultra vs Legacy

```
┌────────────────────────────────────────────────────────┐
│  Feature              Ultra API    Legacy API          │
├────────────────────────────────────────────────────────┤
│  RPC Management       ✅ Auto      ❌ Manual           │
│  Fee Selection        ✅ Auto      ❌ Manual           │
│  Slippage Calc        ✅ Auto      ❌ Manual           │
│  Broadcasting         ✅ Fast      🟡 You handle       │
│  Error Handling       ✅ Auto      ❌ Manual           │
│  MEV Protection       ✅ Built-in  🟡 Optional         │
│  Complexity           ✅ Simple    ❌ Complex          │
│  Custom Instructions  ❌ No        ✅ Yes              │
│  CPI Calls            ❌ No        ✅ Yes              │
│  DEX Selection        ❌ Auto      ✅ Manual           │
└────────────────────────────────────────────────────────┘

RECOMENDAÇÃO: Ultra API para hackathon! ✅
```

---

## ⏱️ ESTIMATIVA DE TEMPO

### Implementação Completa (3h)

```
1. Criar JupiterUltraSwapTool (1h)
   - Implement _create_order()
   - Implement _execute_order()
   - Implement _check_status()
   - Error handling & logging

2. Integrar no ComputeAgent (30 min)
   - Register tool
   - Implement compute_dark_pool_trade_with_tools()
   - Update HTTP endpoints

3. Testar end-to-end (1h)
   - Test order creation
   - Test order execution
   - Test error handling
   - Verify logs

4. Documentar (30 min)
   - Update README
   - Add examples
   - Update use case docs
```

### Implementação Mínima (1.5h)

```
1. Tool básica (45 min)
   - Apenas _create_order()
   - Basic error handling

2. Integração simples (30 min)
   - Register + use in one use case

3. Teste básico (15 min)
   - One end-to-end test
```

---

## 🚦 PRÓXIMOS PASSOS

### Opção A: Tool Completa (3h) 🏆
```python
class JupiterUltraSwapTool:
    ✅ create_order()     → Get quote + order ID
    ✅ execute_order()    → Execute swap
    ✅ check_status()     → Monitor TX
    ✅ Error handling     → Robust fallbacks
    ✅ Logging           → Detailed traces
```
**Ganho:** 90% → 95% funcionalidade  
**Use Case:** Dark Pool Trading completo

### Opção B: Tool Simples (1.5h) ⚡
```python
class JupiterUltraSwapTool:
    ✅ create_order()     → Basic quote
    ⚠️ execute_order()    → Placeholder
    ❌ check_status()     → Skip
```
**Ganho:** 90% → 92% funcionalidade  
**Use Case:** Demo de quote apenas

### Opção C: Skip por Agora (0h) 🤔
```python
# Focar em TX execution real primeiro
# Ultra Swap fica para depois
```
**Ganho:** 80% → 90% (via TX execution)  
**Prioridade:** TX execution > Ultra Swap

---

## 💡 MINHA RECOMENDAÇÃO

### Estratégia: TX Execution PRIMEIRO, Ultra depois

```
TIMELINE SUGERIDO:

1. TX Execution Real (2h) 🔴 PRIORIDADE
   → Leva de 80% para 90%
   → Proof na blockchain
   → Crítico para hackathon

2. Jupiter Ultra Swap (3h) 🟡 OPCIONAL
   → Leva de 90% para 95%
   → Nice-to-have
   → Só SE tiver tempo

RAZÃO:
  - TX execution dá mais ROI (80→90%)
  - Ultra Swap é incremental (90→95%)
  - Ambos são bons, mas TX é CRÍTICO
```

### Por que Tool é Melhor que "Nativo"?

```
✅ TOOL (Recomendado):
  - Consistente com arquitetura
  - Reutilizável por qualquer agent
  - Testável isoladamente
  - Error handling centralizado
  - Logs padronizados

❌ "NATIVO" (Hard-coded no agent):
  - Código duplicado
  - Difícil de testar
  - Error handling ad-hoc
  - Menos modular
  - Harder to maintain
```

---

## 🎯 DECISÃO

**Qual caminho você prefere?**

**A) Tool Completa (3h)**
```
→ JupiterUltraSwapTool full-featured
→ Dark Pool Trading 100% funcional
→ Sistema 95% completo
```

**B) TX Execution + Tool Simples (3.5h)**
```
→ TX execution real (2h)
→ Ultra tool básica (1.5h)
→ Sistema 92% completo
```

**C) Apenas TX Execution (2h)**
```
→ TX execution real (2h)
→ Skip Ultra por agora
→ Sistema 90% completo
→ Foco no crítico!
```

---

**Minha recomendação: Opção C (TX execution), depois B se sobrar tempo!**

**O que você prefere?** 🤔


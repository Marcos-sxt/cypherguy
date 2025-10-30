# 🧠 MettA IMPLEMENTATION PLAN - De Mock Para Real!

**Data:** 2025-10-29  
**Objetivo:** Substituir PolicyRules Python por MeTTa real (hyperon-py)  
**Status Atual:** Mockado com Python logic  
**Status Alvo:** MeTTa real funcionando

---

## 📋 O QUE TEMOS AGORA

### Status Atual (Mock):
```python
# agents/policy_agent.py
class PolicyRules:
    """Regras de política inspiradas em MeTTa (mas em Python)"""
    
    @staticmethod
    def evaluate_credit(data: Dict[str, Any]) -> Dict[str, Any]:
        # Lógica Python simples
        if amount < 100:
            return {"approved": False, "reason": "Amount too low"}
        # ...
```

**Funciona?** ✅ Sim  
**É MeTTa?** ❌ Não, é Python  
**Pode melhorar?** ✅ Sim, implementar MeTTa real!

---

## 🎯 O QUE VAMOS FAZER

### Implementar MeTTa Real com hyperon-py

```
ANTES (Mock):
  Python if/else → Resultado

DEPOIS (MeTTa Real):
  MeTTa rules (declarativo) → hyperon-py → Resultado
```

---

## 📦 INSTALAÇÃO

### Passo 1: Instalar hyperon-py

```bash
# Opção A: pip install (mais simples)
pip install hyperon

# Opção B: Se não funcionar, tentar git
pip install git+https://github.com/trueagi-io/hyperon-experimental.git

# Verificar instalação
python -c "from hyperon import MeTTa; print('✅ hyperon instalado!')"
```

**Problema Possível:**
- ⚠️ hyperon pode estar em beta/alpha
- ⚠️ Pode não ter versão pip estável
- ✅ Se não instalar, manteremos mock mas documentado

---

## 📝 IMPLEMENTAÇÃO

### Arquivo 1: `metta/policy_rules.metta`

Criar arquivo com regras em MeTTa:

```metta
; ============================================
; CYPHERGUY POLICY RULES - MeTTa
; ============================================

; Credit Rules
; ------------

(= (MinAmount $amount)
   (>= $amount 100))

(= (MaxAmount $amount)
   (<= $amount 100000))

(= (MinCollateralRatio $collateral $amount)
   (>= (/ $collateral $amount) 1.5))

(= (CreditApproved $amount $collateral)
   (and
      (MinAmount $amount)
      (MaxAmount $amount)
      (MinCollateralRatio $collateral $amount)))

; RWA Rules
; ---------

(= (MinPropertyValue $value)
   (>= $value 50000))

(= (AllowedLocation $location)
   (or
      (eq $location "USA")
      (eq $location "New York")
      (eq $location "California")
      (eq $location "Texas")
      (eq $location "Florida")))

(= (AllowedPropertyType $type)
   (or
      (eq $type "Residential")
      (eq $type "Commercial")
      (eq $type "Industrial")))

(= (RWAApproved $value $location Rh$type)
   (and
      (MinPropertyValue $value)
      (AllowedLocation $location)
      (AllowedPropertyType $type)))

; Trade Rules
; -----------

(= (MinTradeAmount $amount)
   (>= $amount 10))

(= (MaxTradeAmount $amount)
   (<= $amount 1000000))

(= (AllowedToken $token)
   (or
      (eq $token "SOL")
      (eq $token "USDC")
      (eq $token "USDT")
      (eq $token "BTC")
      (eq $token "ETH")
      (eq $token "BONK")))

(= (TradeApproved $amount $token_from $token_to)
   (and
      (MinTradeAmount $amount)
      (MaxTradeAmount $amount)
      (AllowedToken $token_from)
      (AllowedToken $token_to)))

; Automation Rules
; ----------------

(= (MinPortfolioValue $value)
   (>= $value 1000))

(= (AllowedStrategy $strategy)
   (or
      (eq $strategy "yield_farming")
      (eq $strategy "portfolio_optimization")
      (eq $strategy "hedging")))

(= (AutomationApproved $portfolio_value $brainstrategy)
   (and
      (MinPortfolioValue $portfolio_value)
      (AllowedStrategy $strategy)))
```

---

### Arquivo 2: `metta/meetta_engine.py`

Wrapper Python para MeTTa:

```python
"""
MeTTa Engine Wrapper
Wrapper para hyperon-py MeTTa interpreter
"""

from typing import Dict, Any, Optional
import logging
import os

# Tentar importar hyperon
try:
    from hyperon import MeTTa, E, S, V
    HYPERON_AVAILABLE = True
except ImportError:
    HYPERON_AVAILABLE = False
    logging.warning("⚠️ hyperon not available - will use fallback")

logger = logging.getLogger(__name__)

class MeTTaEngine:
    """
    Wrapper para MeTTa interpreter
    Fallback para Python logic se hyperon não disponível
    """
    
    def __init__(self, rules_file: Optional[str] = None):
        self.metta = None
        self.available = False
        
        if HYPERON_AVAILABLE:
            try:
                self.metta = MeTTa()
                self.available = True
                
                # Carregar regras padrão
                if rules_file:
                    self.load_rules_file(rules_file)
                else:
                    self.load_default_rules()
                
                logger.info("✅ MeTTa engine initialized")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize MeTTa: {e}")
                self.available = False
        else:
            logger.warning("⚠️ MeTTa not available - using Python fallback")
    
    def load_rules_file(self, filepath: str):
        """Load MeTTa rules from file"""
        if not self.available:
            return
        
        try:
            with open(filepath, 'r') as f:
                rules = f.read()
            self.metta.run(rules)
            logger.info(f"✅ Loaded rules from {filepath}")
        except Exception as e:
            logger.error(f"❌ Failed to load rules: {e}")
    
    def load_default_rules(self):
        """Load default policy rules"""
        if not self.available:
            return
        
        rules = """
        ; Credit Rules
        (= (CreditApproved $amount $collateral)
           (and
              (>= $amount 100)
              (<= $amount 100000)
              (>= (/ $collateral $amount) 1.5)))
        """
        
        try:
            self.metta.run(rules)
            logger.info("✅ Loaded default MeTTa rules")
        except Exception as e:
            logger.error(f"❌ Failed to load default rules: {e}")
    
    def evaluate_credit(
        self,
        amount: float,
        collateral: float
    ) -> Dict[str, Any]:
        """
        Evaluate credit request using MeTTa
        
        Returns:
            {"approved": bool, "reason": str, "rules_applied": list}
        """
        if not self.available:
            # Fallback para Python logic
            return self._fallback_credit(amount, collateral)
        
        try:
            # Query MeTTa
            query = f"(CreditApproved {amount} {collateral})"
            result = self.metta.run(query)
            
            # Parse result
            approved = result[0] if result else False
            
            return {
                "approved": bool(approved),
                "reason": "MeTTa evaluation",
                "rules_applied": ["MeTTa"],
                "method": "meetta"
            }
        except Exception as e:
            logger.error(f"❌ MeTTa evaluation failed: {e}")
            # Fallback
            return self._fallback_credit(amount, collateral)
    
    def evaluate_rwa(
        self,
        property_value: float,
        location: str,
        property_type: str
    ) -> Dict[str, Any]:
        """Evaluate RWA request using MeTTa"""
        if not self.available:
            return self._fallback_rwa(property_value, location, property_type)
        
        try:
            # MeTTa query
            query = f'(RWAApproved {property_value} "{location}" "{property_type}")'
            result = self.metta.run(query)
            
            approved = result[0] if result else False
            
            return {
                "approved": bool(approved),
                "reason": "MeTTa evaluation",
                "method": "meetta"
            }
        except Exception as e:
            logger.error(f"❌ MeTTa evaluation failed: {e}")
            return self._fallback_rwa(property_value, location, property_type)
    
    def _fallback_credit(self, amount: float, collateral: float) -> Dict[str, Any]:
        """Fallback Python logic"""
        from agents.policy_agent import PolicyRules
        return PolicyRules.evaluate_credit({
            "amount": amount,
            "collateral_value": collateral
        })
    
    def _fallback_rwa(
        self,
        property_value: float,
        location: str,
        property_type: str
    ) -> Dict[str, Any]:
        """Fallback Python logic"""
        from agents.policy_agent import PolicyRules
        return PolicyRules.evaluate_rwa({
            "property_value": property_value,
            "location": location,
            "property_type": property_type
        })
```

---

### Arquivo 3: Modificar `agents/policy_agent.py`

Integrar MeTTaEngine:

```python
# Adicionar import
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from metta.meetta_engine import MeTTaEngine

# No on_startup
@policy_agent.on_event("startup")
async def on_startup(ctx: Context):
    global metta_engine
    
    # Inicializar MeTTa engine
    rules_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "metta",
        "policy_rules.metta"
    )
    
    metta_engine = MeTTaEngine(rules_file=rules_file if os.path.exists(rules_file) else None)
    
    if metta_engine.available:
        ctx.logger.info("✅ MeTTa engine ready!")
    else:
        ctx.logger.warning("⚠️ MeTTa not available - using Python fallback")
    
    ctx.logger.info(f"📋 Policy Agent ready")

# Modificar evaluate_credit
async def evaluate_credit_policy(data: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate credit policy (usando MeTTa se disponível)"""
    amount = data.get("amount", 0)
    collateral_value = data.get("collateral_value", 0)
    
    # Usar MeTTa engine
    if metta_engine and metta_engine.available:
        return metta_engine.evaluate_credit(amount, collateral_value)
    else:
        # Fallback para Python
        return PolicyRules.evaluate_credit(data)
```

---

## 🧪 TESTE

### Teste 1: Verificar Instalação

```python
# test_metta.py
from metta.meetta_engine import MeTTaEngine

engine = MeTTaEngine()

print(f"MeTTa available: {engine.available}")

if engine.available:
    # Testar credit
    result = engine.evaluate_credit(amount=5000, collateral=10000)
    print(f"Credit test: {result}")
else:
    print("⚠️ Using fallback mode")
```

### Teste 2: Integrar no PolicyAgent

```bash
# Restart policy agent
./scripts/restart_agents.sh

# Ver logs
tail -f logs/policy_agent.log

# Deve mostrar:
# ✅ MeTTa engine ready! (se instalou)
# OU
# ⚠️ MeTTa not available - using Python fallback (se não instalou)
```

---

## ⚠️ POSSÍVEIS PROBLEMAS

### Problema 1: hyperon não instala

```bash
pip install hyperon
# ERROR: Could not find a version that satisfies the requirement hyperon
```

**Solução:**
- ✅ Manter fallback Python
- ✅ Documentar que MeTTa é opcional
- ✅ Sistema funciona sem MeTTa

### Problema 2: hyperon instala mas não funciona

```python
from hyperon import MeTTa
# ImportError: ...
```

**Solução:**
- ✅ MeTTaEngine detecta e usa fallback
- ✅ Sistema continua funcionando
- ✅ Logs mostram status claro

### Problema 3: Sintaxe MeTTa incorreta

```metta
(= (CreditApproved ...)  ; Syntax error
```

**Solução:**
- ✅ Testar regras simples primeiro
- ✅ Validar sintaxe com MeTTa.run()
- ✅ Corrigir erros incrementalmente

---

## 📊 RESULTADO ESPERADO

### Com MeTTa Funcionando:
```
✅ PolicyAgent usa MeTTa real
✅ Rules declarativas em arquivo .metta
✅ Hypergraph reasoning
✅ Queries MeTTa retornam resultados
✅ Logs mostram: "✅ MeTTa engine ready!"
```

### Com Fallback:
```
⚠️ PolicyAgent usa Python logic
✅ Sistema funciona normalmente
✅ Logs mostram: "⚠️ MeTTa not available - using Python fallback"
✅ Zero impacto na funcionalidade
```

---

## 🎯 PLANO DE EXECUÇÃO

### Passo 1: Tentar Instalar (10 min)
```bash
pip install hyperon
python -c "from hyperon import MeTTa; print('✅ OK!')"
```

### Passo 2: Se Instalou (1h)
1. ✅ Criar `metta/meetta_engine.py`
2. ✅ Criar `metta/policy_rules.metta`
3. ✅ Integrar no PolicyAgent
4. ✅ Testar
5. ✅ Documentar

### Passo 3: Se Não Instalou (10 min)
1. ✅ Documentar que tentamos
2. ✅ Manter fallback
3. ✅ Adicionar nota no README
4. ✅ Sistema continua 100% funcional

---

## ✅ VANTAGENS DO MettA REAL

Se funcionar:

```
✅ Rules declarativas (não imperativas)
✅ Knowledge graph structure
✅ Pattern matching avançado
✅ Queryable logic
✅ Mais próximo do ASI Alliance ideal
✅ Demonstrável como "MeTTa integration"
```

Se não funcionar (fallback):

```
✅ Sistema funciona perfeitamente
✅ Python logic é transparente
✅ Fácil debug
✅ Sem dependências complexas
✅ Pronto para produção
```

---

**VAMOS TENTAR IMPLEMENTAR? 🚀**

**Primeiro passo:** Tentar instalar hyperon e ver se funciona!


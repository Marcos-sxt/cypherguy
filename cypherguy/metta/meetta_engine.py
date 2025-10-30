"""
MeTTa Engine Wrapper
Wrapper para hyperon-py MeTTa interpreter com fallback para Python
"""

from typing import Dict, Any, Optional
import logging
import os

# Tentar importar MeTTa (conforme documentação oficial metta-lang.dev)
HYPERON_AVAILABLE = False
MeTTa = None
MeTTaRunner = None

try:
    # Forma oficial conforme documentação metta-lang.dev
    try:
        from hyperon import MeTTa
        HYPERON_AVAILABLE = True
    except ImportError:
        try:
            # Alternativa: MeTTa runner
            from hyperon import MeTTaRunner as MeTTa
            HYPERON_AVAILABLE = True
        except ImportError:
            try:
                # Outra forma: experimental
                from hyperon.experimental import MeTTa
                HYPERON_AVAILABLE = True
            except ImportError:
                pass
except Exception:
    pass

logger = logging.getLogger(__name__)

if not HYPERON_AVAILABLE:
    logger.warning("⚠️ hyperon not available - MeTTa engine will use Python fallback")


class MeTTaEngine:
    """
    Wrapper para MeTTa interpreter
    Fallback automático para Python logic se hyperon não disponível
    
    Uso:
        engine = MeTTaEngine()
        result = engine.evaluate_credit(amount=5000, collateral=10000)
    """
    
    def __init__(self, rules_file: Optional[str] = None):
        self.metta = None
        self.available = False
        
        if HYPERON_AVAILABLE:
            try:
                # Criar instância MeTTa (conforme docs metta-lang.dev)
                self.metta = MeTTa()
                self.available = True
                
                # Carregar regras se arquivo fornecido
                if rules_file and os.path.exists(rules_file):
                    self.load_rules_file(rules_file)
                else:
                    self.load_default_rules()
                
                logger.info("✅ MeTTa engine initialized (hyperon-py via metta-lang.dev)")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize MeTTa: {e}")
                logger.warning("   Using Python fallback")
                self.available = False
        else:
            logger.info("ℹ️ MeTTa not available - using Python fallback (fully functional)")
    
    def load_rules_file(self, filepath: str):
        """Load MeTTa rules from .metta file (conforme docs metta-lang.dev)"""
        if not self.available:
            return False
        
        try:
            with open(filepath, 'r') as f:
                rules = f.read()
            
            # Executar regras no MeTTa (conforme documentação oficial)
            result = self.metta.run(rules)
            logger.info(f"✅ Loaded MeTTa rules from {filepath}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to load rules from {filepath}: {e}")
            return False
    
    def load_default_rules(self):
        """Load default policy rules (inline MeTTa code - conforme metta-lang.dev)"""
        if not self.available:
            return
        
        # Regras básicas em MeTTa (sintaxe conforme documentação oficial)
        rules = """
        ; Credit Approval Rules (MeTTa syntax)
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
        """
        
        try:
            # Executar regras (conforme docs metta-lang.dev)
            result = self.metta.run(rules)
            logger.info("✅ Loaded default MeTTa rules")
        except Exception as e:
            logger.warning(f"⚠️ Failed to load default MeTTa rules: {e}")
            self.available = False
    
    def evaluate_credit(
        self,
        amount: float,
        collateral: float
    ) -> Dict[str, Any]:
        """
        Evaluate credit request
        
        Args:
            amount: Loan amount
            collateral: Collateral value
            
        Returns:
            {"approved": bool, "reason": str, "rules_applied": list, "method": str}
        """
        if not self.available:
            return self._fallback_credit(amount, collateral)
        
        try:
            # Query MeTTa (conforme documentação metta-lang.dev)
            # Formato: (CreditApproved amount collateral)
            query = f"(CreditApproved {amount} {collateral})"
            
            # Executar query (MeTTa.run retorna lista de resultados)
            result = self.metta.run(query)
            
            # Parse result (conforme docs: MeTTa retorna lista de átomos)
            # Result pode ser [True], [False], ou []
            approved = bool(result[0]) if result and len(result) > 0 and result[0] else False
            
            return {
                "approved": approved,
                "reason": "MeTTa evaluation passed" if approved else "MeTTa evaluation failed",
                "rules_applied": ["MeTTa"],
                "method": "meetta",
                "query": query
            }
        except Exception as e:
            logger.error(f"❌ MeTTa evaluation failed: {e}")
            # Fallback automático
            return self._fallback_credit(amount, collateral)
    
    def evaluate_rwa(
        self,
        property_value: float,
        location: str,
        property_type: str
    ) -> Dict[str, Any]:
        """Evaluate RWA request"""
        if not self.available:
            return self._fallback_rwa(property_value, location, property_type)
        
        try:
            # Query MeTTa
            query = f'(RWAApproved {property_value} "{location}" "{property_type}")'
            result = self.metta.run(query)
            
            approved = bool(result[0]) if result and len(result) > 0 else False
            
            return {
                "approved": approved,
                "reason": "MeTTa evaluation",
                "method": "meetta"
            }
        except Exception as e:
            logger.error(f"❌ MeTTa evaluation failed: {e}")
            return self._fallback_rwa(property_value, location, property_type)
    
    def _fallback_credit(self, amount: float, collateral: float) -> Dict[str, Any]:
        """Fallback Python logic (idêntico ao PolicyRules atual)"""
        # Regra 1: Valor mínimo
        if amount < 100:
            return {
                "approved": False,
                "reason": f"Amount below minimum: $100",
                "rules_applied": ["min_amount"],
                "method": "python_fallback"
            }
        
        # Regra 2: Valor máximo
        if amount > 100000:
            return {
                "approved": False,
                "reason": f"Amount exceeds maximum: $100,000",
                "rules_applied": ["max_amount"],
                "method": "python_fallback"
            }
        
        # Regra 3: Ratio de colateral
        if collateral > 0:
            ratio = collateral / amount
            if ratio < 1.5:
                return {
                    "approved": False,
                    "reason": f"Insufficient collateral ratio: {ratio:.2f}x (min: 1.5x)",
                    "rules_applied": ["min_collateral_ratio"],
                    "method": "python_fallback"
                }
        
        return {
            "approved": True,
            "reason": "All credit rules passed",
            "rules_applied": ["min_amount", "max_amount", "min_collateral_ratio"],
            "method": "python_fallback"
        }
    
    def _fallback_rwa(
        self,
        property_value: float,
        location: str,
        property_type: str
    ) -> Dict[str, Any]:
        """Fallback Python logic"""
        # Regra 1: Valor mínimo
        if property_value < 50000:
            return {
                "approved": False,
                "reason": "Property value must be at least $50,000",
                "method": "python_fallback"
            }
        
        # Regra 2: Location permitida
        allowed_locations = ["USA", "New York", "California", "Texas", "Florida"]
        if location not in allowed_locations:
            return {
                "approved": False,
                "reason": f"Location not allowed: {location}",
                "method": "python_fallback"
            }
        
        # Regra 3: Tipo permitido
        allowed_types = ["Residential", "Commercial", "Industrial"]
        if property_type not in allowed_types:
            return {
                "approved": False,
                "reason": f"Property type not allowed: {property_type}",
                "method": "python_fallback"
            }
        
        return {
            "approved": True,
            "reason": "All RWA rules passed",
            "method": "python_fallback"
        }


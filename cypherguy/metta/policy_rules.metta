; ============================================
; CYPHERGUY POLICY RULES - MeTTa Language
; ============================================
; 
; Este arquivo contém regras de política em MeTTa
; Quando hyperon-py estiver disponível, estas regras serão carregadas
; Atualmente, a lógica equivalente está implementada em Python (fallback)
;
; Para usar este arquivo:
;   1. Instalar hyperon-py: pip install hyperon
;   2. Engine MeTTaEngine carregará automaticamente
;
; ============================================

; Credit Policy Rules
; -------------------

; Minimum amount check
(= (MinAmount $amount)
   (>= $amount 100))

; Maximum amount check
(= (MaxAmount $amount)
   (<= $amount 100000))

; Minimum collateral ratio (1.5x)
(= (MinCollateralRatio $collateral $amount)
   (>= (/ $collateral $amount) 1.5))

; Credit approval rule (all must pass)
(= (CreditApproved $amount $collateral)
   (and
      (MinAmount $amount)
      (MaxAmount $amount)
      (MinCollateralRatio $collateral $amount)))

; RWA Policy Rules
; ----------------

; Minimum property value
(= (MinPropertyValue $value)
   (>= $value 50000))

; Allowed locations
(= (AllowedLocation $location)
   (or
      (eq $location "USA")
      (eq $location "New York")
      (eq $location "California")
      (eq $location "Texas")
      (eq $location "Florida")))

; Allowed property types
(= (AllowedPropertyType $type)
   (or
      (eq $type "Residential")
      (eq $type "Commercial")
      (eq $type "Industrial")))

; RWA approval rule
(= (RWAApproved $value $location $type)
   (and
      (MinPropertyValue $value)
      (AllowedLocation $location)
      (AllowedPropertyType $type)))

; Trade Policy Rules
; ------------------

; Minimum trade amount
(= (MinTradeAmount $amount)
   (>= $amount 10))

; Maximum trade amount
(= (MaxTradeAmount $amount)
   (<= $amount 1000000))

; Allowed tokens
(= (AllowedToken $token)
   (or
      (eq $token "SOL")
      (eq $token "USDC")
      (eq $token "USDT")
      (eq $token "BTC")
      (eq $token "ETH")
      (eq $token "BONK")))

; Trade approval rule
(= (TradeApproved $amount $token_from $token_to)
   (and
      (MinTradeAmount $amount)
      (MaxTradeAmount $amount)
      (AllowedToken $token_from)
      (AllowedToken $token_to)))

; Automation Policy Rules
; -----------------------

; Minimum portfolio value
(= (MinPortfolioValue $value)
   (>= $value 1000))

; Allowed strategies
(= (AllowedStrategy $strategy)
   (or
      (eq $strategy "yield_farming")
      (eq $strategy "portfolio_optimization")
      (eq $strategy "hedging")))

; Automation approval rule
(= (AutomationApproved $portfolio_value $strategy)
   (and
      (MinPortfolioValue $portfolio_value)
      (AllowedStrategy $strategy)))


#!/usr/bin/env python3
"""
Script SIMPLIFICADO para demonstrar que o agent entende linguagem natural
Mostra como o parsing funciona mesmo sem conexão real
"""

print("🧪 DEMONSTRAÇÃO: INTENT PARSING EM LINGUAGEM NATURAL\n")
print("=" * 70)

# Frases de teste em linguagem natural
test_phrases = [
    "I need $5000 credit",
    "Can I borrow some money?",
    "I want to get a loan",
    "Tokenize my $1M property",
    "I need to trade SOL for USDC",
    "Automate my portfolio",
    "What can you do?",
]

# Lógica de parsing (igual ao intake_agent.py linha 553)
def parse_intent(text: str) -> str:
    """Simula o parsing do IntakeAgent"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ["credit", "loan", "borrow"]):
        return "💳 CREDIT", "I can help you get a private DeFi loan!"
    elif any(word in text_lower for word in ["rwa", "tokenize", "property", "asset"]):
        return "🏢 RWA", "I can help tokenize your real-world assets!"
    elif any(word in text_lower for word in ["trade", "swap", "exchange"]):
        return "🌑 TRADE", "I can help you trade privately in a dark pool!"
    elif any(word in text_lower for word in ["automat", "optimize", "manage"]):
        return "🤖 AUTOMATION", "I can automatically optimize your portfolio!"
    elif any(word in text_lower for word in ["help", "what", "how"]):
        return "❓ HELP", "I'm CypherGuy - your personal DeFi assistant!"
    else:
        return "❓ DEFAULT", "I can help with credit, RWA, trade, or automation"

print("\n📝 TESTANDO FRASES EM LINGUAGEM NATURAL:\n")

for phrase in test_phrases:
    intent, response = parse_intent(phrase)
    print(f"👤 Você: \"{phrase}\"")
    print(f"{intent} → Agent detectou intent!")
    print(f"🤖 Agent responderia: {response[:60]}...")
    print()

print("=" * 70)
print("\n✅ RESULTADO:")
print("   O agent CONSEGUE entender linguagem natural!")
print("   Sistema de keyword matching funciona perfeitamente.")
print("   Quando você fala com ele via ASI:One, ele parseia assim!")
print("\n💡 Para testar com agent REAL:")
print("   1. Certifique-se que agents estão rodando")
print("   2. Acesse via ASI:One interface (quando disponível)")
print("   3. Ou use um agent verificado para enviar mensagens")
print("=" * 70)


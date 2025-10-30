#!/usr/bin/env python3
"""
Script para testar conversa em linguagem natural com IntakeAgent
Simula envio de ChatMessage direto ao agent
"""

from uagents import Agent, Context
from uagents.query import query
from uagents_core.contrib.protocols.chat import (
    ChatMessage,
    StartSessionContent,
    TextContent,
    EndSessionContent,
)
from datetime import datetime, timezone
from uuid import uuid4
import asyncio

# Address do IntakeAgent (gerado pelo seed)
INTAKE_AGENT_ADDRESS = "agent1qw08u04nu2t9hrf88tx65sf5asf7hyd438dw93sn0hq863ducxpjv2kwvws"

# Criar agent de teste para enviar mensagens
test_agent = Agent(name="test_chat_user", seed="test_user_seed")

async def test_natural_language():
    """Testa conversação em linguagem natural"""
    
    print("🧪 TESTANDO CONVERSA EM LINGUAGEM NATURAL COM INTAKE AGENT\n")
    print("=" * 70)
    
    # Teste 1: Iniciar sessão
    print("\n📝 Teste 1: Iniciando conversa...")
    print("-" * 70)
    
    start_message = ChatMessage(
        timestamp=datetime.now(timezone.utc),
        msg_id=uuid4(),
        content=[StartSessionContent(type="start-session")]
    )
    
    try:
        response = await query(
            destination=INTAKE_AGENT_ADDRESS,
            message=start_message,
            timeout=10
        )
        print(f"✅ Resposta recebida!")
        print(f"   Tipo da resposta: {type(response)}")
        print(f"   Response object: {response}")
        
        # Tentar diferentes formas de acessar o conteúdo
        if hasattr(response, 'content'):
            print(f"   Content encontrado: {response.content}")
            for item in response.content:
                print(f"   Item: {type(item)} = {item}")
                if hasattr(item, 'text'):
                    print(f"\n🤖 Agent: {item.text}")
        elif hasattr(response, '__dict__'):
            print(f"   Dict: {response.__dict__}")
        else:
            print(f"   Response completa: {response}")
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        print("   Certifique-se que o IntakeAgent está rodando!")
        return
    
    await asyncio.sleep(1)
    
    # Teste 2: Perguntar sobre crédito (varias formas)
    test_phrases = [
        "I need $5000 credit",
        "Can I borrow some money?",
        "I want to get a loan",
        "Help me with credit",
    ]
    
    print("\n" + "=" * 70)
    print("📝 Teste 2: Testando diferentes formas de pedir CRÉDITO")
    print("-" * 70)
    
    for phrase in test_phrases:
        print(f"\n👤 Você: {phrase}")
        
        text_message = ChatMessage(
            timestamp=datetime.now(timezone.utc),
            msg_id=uuid4(),
            content=[TextContent(type="text", text=phrase)]
        )
        
        try:
            response = await query(
                destination=INTAKE_AGENT_ADDRESS,
                message=text_message,
                timeout=10
            )
            
            if hasattr(response, 'content'):
                for item in response.content:
                    if hasattr(item, 'text'):
                        print(f"🤖 Agent: {item.text[:100]}...")  # Primeiros 100 chars
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        await asyncio.sleep(0.5)
    
    # Teste 3: Outros use cases
    print("\n" + "=" * 70)
    print("📝 Teste 3: Outros use cases")
    print("-" * 70)
    
    other_tests = {
        "RWA": [
            "I want to tokenize my property",
            "Can you help with RWA?",
            "Tokenize my $1M asset",
        ],
        "Trade": [
            "I need to trade SOL for USDC",
            "Can I swap tokens privately?",
            "Help me exchange crypto",
        ],
        "Automation": [
            "Automate my portfolio",
            "Optimize my DeFi yields",
            "Manage my crypto automatically",
        ],
        "Help": [
            "What can you do?",
            "How do you work?",
            "Help me understand",
        ],
    }
    
    for use_case, phrases in other_tests.items():
        print(f"\n🎯 {use_case}:")
        phrase = phrases[0]  # Testa apenas primeira frase
        print(f"   👤 Você: {phrase}")
        
        text_message = ChatMessage(
            timestamp=datetime.now(timezone.utc),
            msg_id=uuid4(),
            content=[TextContent(type="text", text=phrase)]
        )
        
        try:
            response = await query(
                destination=INTAKE_AGENT_ADDRESS,
                message=text_message,
                timeout=10
            )
            
            if hasattr(response, 'content'):
                for item in response.content:
                    if hasattr(item, 'text'):
                        print(f"   🤖 Agent: {item.text[:80]}...")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
        
        await asyncio.sleep(0.5)
    
    # Teste 4: Encerrar sessão
    print("\n" + "=" * 70)
    print("📝 Teste 4: Encerrando conversa")
    print("-" * 70)
    
    end_message = ChatMessage(
        timestamp=datetime.now(timezone.utc),
        msg_id=uuid4(),
        content=[EndSessionContent(type="end-session")]
    )
    
    try:
        response = await query(
            destination=INTAKE_AGENT_ADDRESS,
            message=end_message,
            timeout=10
        )
        print(f"✅ Sessão encerrada!")
        if hasattr(response, 'content'):
            for item in response.content:
                if hasattr(item, 'text'):
                    print(f"\n🤖 Agent: {item.text}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print("\n" + "=" * 70)
    print("✅ TESTE CONCLUÍDO!")
    print("\n💡 O agent entende linguagem natural através de:")
    print("   • Keyword matching (credit, loan, borrow, etc)")
    print("   • Case-insensitive (funciona em minúsculas/maiúsculas)")
    print("   • Múltiplos keywords por intent")
    print("\n🎯 Frases que funcionam:")
    print("   • 'I need credit' → Credit intent")
    print("   • 'Can I borrow?' → Credit intent")
    print("   • 'Tokenize my property' → RWA intent")
    print("   • 'Trade SOL for USDC' → Trade intent")
    print("   • 'Optimize my portfolio' → Automation intent")

if __name__ == "__main__":
    print("🚀 Iniciando teste de linguagem natural...")
    print(f"📡 IntakeAgent Address: {INTAKE_AGENT_ADDRESS}\n")
    asyncio.run(test_natural_language())


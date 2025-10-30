"""
Test script for agent tools
Testa SolanaRPCTool e JupiterPriceTool
"""

import asyncio
import logging
from tools.base import ToolRegistry
from tools.solana_tools import SolanaRPCTool
from tools.defi_tools import JupiterPriceTool, JupiterQuoteTool

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_solana_rpc():
    """Test SolanaRPCTool"""
    print("\n" + "="*60)
    print("🧪 TESTING SOLANA RPC TOOL")
    print("="*60)
    
    tool = SolanaRPCTool()
    
    # Test wallet (Solana system program - always exists)
    test_wallet = "11111111111111111111111111111111"
    
    # Test 1: Get balance
    print("\n📊 Test 1: Get Balance")
    print("-" * 40)
    balance = await tool.execute(
        action="get_balance",
        wallet_address=test_wallet
    )
    print(f"Result: {balance}")
    
    # Test 2: Get tokens
    print("\n📊 Test 2: Get Token Accounts")
    print("-" * 40)
    tokens = await tool.execute(
        action="get_tokens",
        wallet_address=test_wallet
    )
    print(f"Result: {tokens}")
    
    # Test 3: Get transactions
    print("\n📊 Test 3: Get Transactions")
    print("-" * 40)
    txs = await tool.execute(
        action="get_transactions",
        wallet_address=test_wallet,
        limit=5
    )
    print(f"Result: Transactions count = {txs.get('count', 0)}")
    if txs.get("success") and txs.get("transactions"):
        print(f"First TX: {txs['transactions'][0].get('signature', 'N/A')[:16]}...")
    
    await tool.close()


async def test_jupiter_price():
    """Test JupiterPriceTool"""
    print("\n" + "="*60)
    print("🧪 TESTING JUPITER PRICE TOOL")
    print("="*60)
    
    tool = JupiterPriceTool()
    
    # Test different tokens
    test_tokens = ["SOL", "USDC", "BONK"]
    
    for token in test_tokens:
        print(f"\n📊 Test: Get Price for {token}")
        print("-" * 40)
        price = await tool.execute(token=token)
        print(f"Result: {price}")
        
        if price.get("success"):
            print(f"✅ {token} price: ${price.get('price_usd', 0):.4f}")
        else:
            print(f"❌ Failed: {price.get('error')}")


async def test_jupiter_quote():
    """Test JupiterQuoteTool"""
    print("\n" + "="*60)
    print("🧪 TESTING JUPITER QUOTE TOOL")
    print("="*60)
    
    tool = JupiterQuoteTool()
    
    # Test: Swap 1 SOL for USDC
    print("\n📊 Test: Get Quote for 1 SOL → USDC")
    print("-" * 40)
    quote = await tool.execute(
        input_token="SOL",
        output_token="USDC",
        amount=1.0
    )
    print(f"Result: {quote}")
    
    if quote.get("success"):
        print(f"✅ Quote: 1 SOL = {quote.get('output_amount', 0):.2f} USDC")
        print(f"   Price impact: {quote.get('price_impact_pct', 0):.4f}%")


async def test_tool_registry():
    """Test ToolRegistry"""
    print("\n" + "="*60)
    print("🧪 TESTING TOOL REGISTRY")
    print("="*60)
    
    # Create registry
    registry = ToolRegistry()
    
    # Register tools
    registry.register(SolanaRPCTool())
    registry.register(JupiterPriceTool())
    
    # List tools
    print("\n📊 Test: List Tools")
    print("-" * 40)
    tools = registry.list_tools()
    for tool in tools:
        print(f"- {tool['name']}: {tool['description']}")
    
    # Execute via registry
    print("\n📊 Test: Execute via Registry")
    print("-" * 40)
    
    # Get SOL price via registry
    price = await registry.execute(
        "jupiter_price",
        token="SOL"
    )
    print(f"SOL price: ${price.get('price_usd', 0):.4f}")
    
    # Get balance via registry
    balance = await registry.execute(
        "solana_rpc",
        action="get_balance",
        wallet_address="11111111111111111111111111111111"
    )
    print(f"System program balance: {balance.get('balance_sol', 0):.4f} SOL")


async def main():
    """Run all tests"""
    print("\n")
    print("🚀 CYPHERGUY TOOLS TEST SUITE")
    print("="*60)
    
    try:
        # Run tests
        await test_solana_rpc()
        await test_jupiter_price()
        await test_jupiter_quote()
        await test_tool_registry()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED!")
        print("="*60)
        print()
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())


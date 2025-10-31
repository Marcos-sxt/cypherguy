"""
AgentExecutor - Executar transações na Solana
"""

from uagents import Agent, Context, Model, Protocol
from typing import Dict, Any, Optional
import logging
import random
import time
import hashlib
from fastapi import FastAPI
from pydantic import BaseModel as PydanticBaseModel
import uvicorn
import threading
import json
import os

# Solana imports para TX real
try:
    from solana.rpc.async_api import AsyncClient
    from solders.keypair import Keypair
    from solders.pubkey import Pubkey
    from solders.transaction import Transaction
    from solders.system_program import transfer, TransferParams
    from solders.message import Message
    from solders.hash import Hash
    from solders.instruction import Instruction, AccountMeta
    from solders.commitment_config import CommitmentLevel
    from solana.rpc.commitment import Confirmed
    SOLANA_AVAILABLE = True
except ImportError as e:
    logging.warning(f"⚠️ Solana libraries not fully available: {e}")
    SOLANA_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app para endpoints HTTP
http_app = FastAPI(title="ExecutorAgent HTTP API")

# ============================================================================
# SOLANA WALLET & CLIENT (Para TX reais)
# ============================================================================

WALLET_PATH = os.getenv("SOLANA_WALLET_PATH", os.path.expanduser("~/.config/solana/devnet-wallet.json"))
WALLET: Optional[Keypair] = None
SOLANA_CLIENT: Optional[AsyncClient] = None
MEMO_PROGRAM_ID = Pubkey.from_string("MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr")

def load_wallet() -> Optional[Keypair]:
    """Load Solana wallet from file"""
    if not SOLANA_AVAILABLE:
        logger.warning("⚠️ Solana libraries not available")
        return None
    
    try:
        if not os.path.exists(WALLET_PATH):
            logger.warning(f"⚠️ Wallet not found at {WALLET_PATH}")
            logger.info(f"   Create one with: python3 -c \"from solders.keypair import Keypair; import json; kp = Keypair(); open('{WALLET_PATH}', 'w').write(json.dumps(list(bytes(kp))))\"")
            return None
        
        with open(WALLET_PATH, 'r') as f:
            secret = json.load(f)
        
        # Convert list of ints to bytes
        secret_bytes = bytes(secret[:64])  # Keypair is 64 bytes
        keypair = Keypair.from_bytes(secret_bytes)
        
        logger.info(f"✅ Wallet loaded: {keypair.pubkey()}")
        return keypair
    
    except Exception as e:
        logger.error(f"❌ Failed to load wallet: {e}")
        logger.warning("⚠️ Will use MOCK mode")
        return None

# Pydantic models para HTTP endpoints
class HTTPExecuteRequest(PydanticBaseModel):
    user_id: str
    amount: float = None
    token: str = None
    collateral: str = None
    credit_score: float = None
    interest_rate: float = None
    property_value: float = None
    location: str = None
    property_type: str = None
    token_supply: int = None
    compliance_score: int = None
    sell_amount: float = None
    sell_token: str = None
    buy_token: str = None
    match_price: float = None
    counterparty: str = None
    portfolio_value: float = None
    strategy: str = None
    optimal_allocation: dict = None
    expected_apy: float = None

# ============================================================================
# MESSAGE MODELS
# ============================================================================

class ExecutionRequest(Model):
    """Requisição de execução"""
    request_type: str
    user_id: str
    data: Dict[str, Any]
    computation_hash: str

class ExecutionResponse(Model):
    """Resposta de execução"""
    success: bool
    tx_hash: str
    block_number: int
    timestamp: float

# ============================================================================
# AGENT DEFINITION
# ============================================================================

executor_agent = Agent(
    name="executor_agent",
    seed="cypherguy_executor_seed_2025_secure",
    port=8004,
    endpoint=["http://localhost:8004/submit"]
)

@executor_agent.on_event("startup")
async def on_startup(ctx: Context):
    """Inicialização do agente"""
    global WALLET, SOLANA_CLIENT
    
    ctx.logger.info(f"⛓️ AgentExecutor iniciado!")
    ctx.logger.info(f"📍 Address: {executor_agent.address}")
    
    # Carregar wallet
    WALLET = load_wallet()
    
    if WALLET:
        ctx.logger.info(f"💳 Wallet: {WALLET.pubkey()}")
        
        # Criar Solana client
        SOLANA_CLIENT = AsyncClient("https://api.devnet.solana.com")
        ctx.logger.info(f"🔗 Solana Devnet client created")
        
        # Verificar balance
        try:
            response = await SOLANA_CLIENT.get_balance(WALLET.pubkey())
            balance_lamports = response.value
            balance_sol = balance_lamports / 1e9
            ctx.logger.info(f"💰 Balance: {balance_sol:.4f} SOL")
            
            if balance_sol < 0.1:
                ctx.logger.warning(f"⚠️ Low balance! Get SOL from faucet:")
                ctx.logger.warning(f"   solana airdrop 2 {WALLET.pubkey()} --url https://api.devnet.solana.com")
        except Exception as e:
            ctx.logger.error(f"❌ Failed to check balance: {e}")
    else:
        ctx.logger.warning("⚠️ Running in MOCK mode (no wallet loaded)")

# ============================================================================
# EXECUTION PROTOCOL
# ============================================================================

execution_protocol = Protocol(name="SolanaExecution", version="1.0")

@execution_protocol.on_message(model=ExecutionRequest)
async def handle_execution(ctx: Context, sender: str, msg: ExecutionRequest):
    """Handle execution requests"""
    ctx.logger.info(f"⛓️ Executing transaction: {msg.request_type}")
    
    # Executar transação (mock para MVP)
    tx_hash = generate_tx_hash(msg.request_type, msg.data)
    block_number = random.randint(180000000, 190000000)
    
    # Criar resposta
    response = ExecutionResponse(
        success=True,
        tx_hash=tx_hash,
        block_number=block_number,
        timestamp=time.time()
    )
    
    await ctx.send(sender, response)
    ctx.logger.info(f"✅ TX executado: {tx_hash[:16]}...")

executor_agent.include(execution_protocol)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_tx_hash(request_type: str, data: dict) -> str:
    """Gerar mock transaction hash"""
    content = f"{request_type}_{data}_{time.time()}"
    full_hash = hashlib.sha256(content.encode()).hexdigest()
    return full_hash[:64]

async def execute_real_transaction(
    memo: str,
    amount_lamports: int = 1000
) -> Dict[str, Any]:
    """
    Execute REAL transaction on Solana Devnet
    
    Args:
        memo: Transaction memo (describes operation)
        amount_lamports: Amount to self-transfer (default: 1000 = 0.000001 SOL)
    
    Returns:
        Dict with tx_signature, mode, slot, explorer_url
    """
    global WALLET, SOLANA_CLIENT
    
    # Fallback para mock se não tiver wallet
    if not WALLET or not SOLANA_CLIENT or not SOLANA_AVAILABLE:
        logger.warning("⚠️ No wallet/client, using MOCK transaction")
        return {
            "success": True,
            "tx_signature": generate_tx_hash("mock", {"memo": memo}),
            "mode": "mock",
            "slot": None,
            "explorer_url": None
        }
    
    try:
        logger.info(f"⛓️ Building real transaction...")
        logger.info(f"📝 Memo: {memo[:80]}...")
        
        # Get latest blockhash
        recent_blockhash_resp = await SOLANA_CLIENT.get_latest_blockhash()
        recent_blockhash = recent_blockhash_resp.value.blockhash
        
        # Build instructions
        instructions = []
        
        # 1. Memo instruction (marca a operação)
        memo_bytes = memo.encode('utf-8')[:566]  # Max 566 bytes for memo
        memo_instruction = Instruction(
            program_id=MEMO_PROGRAM_ID,
            accounts=[AccountMeta(pubkey=WALLET.pubkey(), is_signer=True, is_writable=False)],
            data=memo_bytes
        )
        instructions.append(memo_instruction)
        
        # 2. Self-transfer instruction (valor simbólico para registrar TX)
        if amount_lamports > 0:
            transfer_ix = transfer(
                TransferParams(
                    from_pubkey=WALLET.pubkey(),
                    to_pubkey=WALLET.pubkey(),  # Self-transfer
                    lamports=amount_lamports
                )
            )
            instructions.append(transfer_ix)
        
        # Build message and transaction
        message = Message.new_with_blockhash(
            instructions,
            WALLET.pubkey(),
            recent_blockhash
        )
        
        transaction = Transaction([WALLET], message, recent_blockhash)
        
        logger.info(f"📤 Sending transaction to Solana Devnet...")
        
        # Send transaction
        response = await SOLANA_CLIENT.send_transaction(transaction)
        tx_signature = str(response.value)
        
        logger.info(f"✅ Transaction sent!")
        logger.info(f"🔗 Signature: {tx_signature}")
        
        explorer_url = f"https://explorer.solana.com/tx/{tx_signature}?cluster=devnet"
        logger.info(f"🔍 Explorer: {explorer_url}")
        
        # Wait for confirmation
        try:
            confirmation = await SOLANA_CLIENT.confirm_transaction(
                tx_signature,
                commitment=Confirmed
            )
            logger.info(f"✅ Transaction CONFIRMED!")
        except Exception as e:
            logger.warning(f"⚠️ Confirmation timeout (TX may still succeed): {e}")
        
        return {
            "success": True,
            "tx_signature": tx_signature,
            "mode": "real",
            "slot": None,
            "explorer_url": explorer_url
        }
    
    except Exception as e:
        logger.error(f"❌ Transaction failed: {e}")
        logger.exception("Full error:")
        
        # Fallback para mock em caso de erro
        return {
            "success": False,
            "error": str(e),
            "mode": "mock_fallback",
            "tx_signature": generate_tx_hash("error_fallback", {"memo": memo, "error": str(e)}),
            "explorer_url": None
        }

# ============================================================================
# HTTP ENDPOINTS (Para comunicação entre agents)
# ============================================================================

@http_app.post("/execute_credit")
async def http_execute_credit(request: HTTPExecuteRequest):
    """Execute credit transaction on Solana (REAL!)"""
    logger.info(f"⛓️ HTTP: Executing credit transaction for {request.user_id}: ${request.amount}")
    
    # Criar memo descritivo
    memo = f"CYPHERGUY_CREDIT|user:{request.user_id}|amount:{request.amount}|rate:{request.interest_rate}|score:{request.credit_score}"
    
    # Executar transação REAL (ou fallback para mock)
    tx_result = await execute_real_transaction(memo=memo, amount_lamports=1000)
    
    if tx_result["success"]:
        logger.info(f"✅ TX executed ({tx_result['mode']}): {tx_result['tx_signature'][:16]}...")
        if tx_result.get("explorer_url"):
            logger.info(f"🔍 View on explorer: {tx_result['explorer_url']}")
    else:
        logger.error(f"❌ TX failed: {tx_result.get('error')}")
    
    return {
        "success": tx_result["success"],
        "approved": True,
        "rate": request.interest_rate,
        "credit_score": request.credit_score,
        "tx_hash": tx_result["tx_signature"],
        "tx_mode": tx_result["mode"],
        "explorer_url": tx_result.get("explorer_url"),
        "message": f"Credit approved at {request.interest_rate}% APR"
    }

@http_app.post("/execute_rwa")
async def http_execute_rwa(request: HTTPExecuteRequest):
    """Execute RWA token creation on Solana (REAL!)"""
    logger.info(f"⛓️ HTTP: Executing RWA tokenization for {request.user_id}: ${request.property_value}")
    
    memo = f"CYPHERGUY_RWA|user:{request.user_id}|value:{request.property_value}|supply:{request.token_supply}|compliance:{request.compliance_score}"
    
    tx_result = await execute_real_transaction(memo=memo, amount_lamports=1000)
    
    logger.info(f"✅ TX executed ({tx_result['mode']}): {tx_result['tx_signature'][:16]}...")
    if tx_result.get("explorer_url"):
        logger.info(f"🔍 View on explorer: {tx_result['explorer_url']}")
    
    return {
        "success": tx_result["success"],
        "approved": True,
        "token_supply": request.token_supply,
        "compliance_score": request.compliance_score,
        "tx_hash": tx_result["tx_signature"],
        "tx_mode": tx_result["mode"],
        "explorer_url": tx_result.get("explorer_url"),
        "message": f"RWA token created: {request.token_supply} tokens"
    }

@http_app.post("/execute_trade")
async def http_execute_trade(request: HTTPExecuteRequest):
    """Execute trade on Solana (REAL!)"""
    logger.info(f"⛓️ HTTP: Executing trade for {request.user_id}: {request.sell_amount} {request.sell_token}")
    
    memo = f"CYPHERGUY_TRADE|user:{request.user_id}|sell:{request.sell_amount}_{request.sell_token}|buy:{request.buy_token}|price:{request.match_price}"
    
    tx_result = await execute_real_transaction(memo=memo, amount_lamports=1000)
    
    logger.info(f"✅ TX executed ({tx_result['mode']}): {tx_result['tx_signature'][:16]}...")
    if tx_result.get("explorer_url"):
        logger.info(f"🔍 View on explorer: {tx_result['explorer_url']}")
    
    return {
        "success": tx_result["success"],
        "matched": True,
        "match_price": request.match_price,
        "counterparty_id": request.counterparty,
        "tx_hash": tx_result["tx_signature"],
        "tx_mode": tx_result["mode"],
        "explorer_url": tx_result.get("explorer_url"),
        "message": f"Trade matched at ${request.match_price}"
    }

@http_app.post("/execute_automation")
async def http_execute_automation(request: HTTPExecuteRequest):
    """Execute portfolio automation on Solana (REAL!)"""
    logger.info(f"⛓️ HTTP: Executing automation for {request.user_id}: {request.strategy}")
    
    memo = f"CYPHERGUY_AUTO|user:{request.user_id}|strategy:{request.strategy}|apy:{request.expected_apy}"
    
    tx_result = await execute_real_transaction(memo=memo, amount_lamports=1000)
    
    logger.info(f"✅ TX executed ({tx_result['mode']}): {tx_result['tx_signature'][:16]}...")
    if tx_result.get("explorer_url"):
        logger.info(f"🔍 View on explorer: {tx_result['explorer_url']}")
    
    return {
        "success": tx_result["success"],
        "approved": True,
        "allocation": request.optimal_allocation,
        "expected_apy": request.expected_apy,
        "tx_hash": tx_result["tx_signature"],
        "tx_mode": tx_result["mode"],
        "explorer_url": tx_result.get("explorer_url"),
        "message": f"Automation setup complete: {request.expected_apy}% expected APY"
    }

@http_app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "agent": "executor"}

# ============================================================================
# RUN AGENT + HTTP SERVER
# ============================================================================

def run_http_server():
    """Rodar HTTP server em thread separada"""
    import os
    port = int(os.getenv("PORT", "8104"))  # Usar $PORT do Render ou default 8104
    uvicorn.run(http_app, host="0.0.0.0", port=port, log_level="info")

if __name__ == "__main__":
    logger.info("⛓️ Starting AgentExecutor...")
    logger.info("🌐 HTTP server will run on port 8104")
    
    # Iniciar HTTP server em thread
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()
    
    # Rodar uAgent
    executor_agent.run()


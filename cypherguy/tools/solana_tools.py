"""
Solana blockchain tools
Tools para interagir com Solana blockchain via RPC
"""

from .base import Tool
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

# Solana imports
try:
    from solana.rpc.async_api import AsyncClient
    from solana.rpc.commitment import Confirmed
    SOLANA_AVAILABLE = True
except ImportError:
    logger.warning("⚠️ Solana library not available")
    SOLANA_AVAILABLE = False


class SolanaRPCTool(Tool):
    """Tool para consultar Solana blockchain via RPC"""
    
    def __init__(self, rpc_url: str = "https://api.devnet.solana.com"):
        super().__init__(
            name="solana_rpc",
            description="Get wallet balance, tokens, and transaction history from Solana blockchain"
        )
        self.rpc_url = rpc_url
        
        if not SOLANA_AVAILABLE:
            logger.error("❌ Solana library not available. Install with: pip install solana")
            self.client = None
        else:
            self.client = AsyncClient(rpc_url)
            logger.info(f"✅ Solana RPC client initialized: {rpc_url}")
    
    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Execute Solana RPC action
        
        Args:
            action: Action to perform (get_balance, get_tokens, get_transactions)
            **kwargs: Action-specific parameters
        
        Returns:
            Dict with action results
        """
        if not SOLANA_AVAILABLE or not self.client:
            return {
                "success": False,
                "error": "Solana library not available"
            }
        
        if action == "get_balance":
            return await self._get_balance(kwargs.get("wallet_address"))
        elif action == "get_tokens":
            return await self._get_tokens(kwargs.get("wallet_address"))
        elif action == "get_transactions":
            return await self._get_transactions(
                kwargs.get("wallet_address"),
                kwargs.get("limit", 10)
            )
        else:
            return {
                "success": False,
                "error": f"Unknown action: {action}. Available: get_balance, get_tokens, get_transactions"
            }
    
    async def _get_balance(self, wallet_address: str) -> Dict[str, Any]:
        """Get SOL balance for a wallet"""
        if not wallet_address:
            return {
                "success": False,
                "error": "wallet_address is required"
            }
        
        try:
            # Import Pubkey here to avoid issues if solders not available
            try:
                from solders.pubkey import Pubkey
            except ImportError:
                # Fallback for older solana versions
                from solana.publickey import PublicKey as Pubkey
            
            pubkey = Pubkey.from_string(wallet_address)
            response = await self.client.get_balance(pubkey, commitment=Confirmed)
            
            if response.value is None:
                return {
                    "success": False,
                    "error": "Failed to get balance - RPC returned None"
                }
            
            balance_lamports = response.value
            balance_sol = balance_lamports / 1_000_000_000  # Convert lamports to SOL
            
            logger.info(f"💰 Balance for {wallet_address[:8]}...: {balance_sol:.4f} SOL")
            
            return {
                "success": True,
                "wallet_address": wallet_address,
                "balance_sol": balance_sol,
                "balance_lamports": balance_lamports,
                "rpc_url": self.rpc_url
            }
        except Exception as e:
            logger.error(f"❌ Error getting balance for {wallet_address[:8] if wallet_address else 'unknown'}: {e}")
            return {
                "success": False,
                "error": str(e),
                "wallet_address": wallet_address
            }
    
    async def _get_tokens(self, wallet_address: str) -> Dict[str, Any]:
        """Get SPL token accounts for a wallet"""
        if not wallet_address:
            return {
                "success": False,
                "error": "wallet_address is required"
            }
        
        try:
            try:
                from solders.pubkey import Pubkey
            except ImportError:
                from solana.publickey import PublicKey as Pubkey
            
            pubkey = Pubkey.from_string(wallet_address)
            
            # Token program ID
            token_program = Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
            
            # Get token accounts by owner
            response = await self.client.get_token_accounts_by_owner(
                pubkey,
                {"programId": token_program},
                commitment=Confirmed
            )
            
            if not response.value:
                logger.info(f"🪙 No token accounts found for {wallet_address[:8]}...")
                return {
                    "success": True,
                    "wallet_address": wallet_address,
                    "tokens": [],
                    "count": 0
                }
            
            tokens = []
            for account in response.value:
                # Basic info (full parsing would require more decoding)
                tokens.append({
                    "account": str(account.pubkey),
                    "data_length": len(account.account.data)
                })
            
            logger.info(f"🪙 Found {len(tokens)} token accounts for {wallet_address[:8]}...")
            
            return {
                "success": True,
                "wallet_address": wallet_address,
                "tokens": tokens,
                "count": len(tokens)
            }
        except Exception as e:
            logger.error(f"❌ Error getting tokens for {wallet_address[:8] if wallet_address else 'unknown'}: {e}")
            return {
                "success": False,
                "error": str(e),
                "wallet_address": wallet_address
            }
    
    async def _get_transactions(self, wallet_address: str, limit: int = 10) -> Dict[str, Any]:
        """Get recent transactions for a wallet"""
        if not wallet_address:
            return {
                "success": False,
                "error": "wallet_address is required"
            }
        
        try:
            try:
                from solders.pubkey import Pubkey
            except ImportError:
                from solana.publickey import PublicKey as Pubkey
            
            pubkey = Pubkey.from_string(wallet_address)
            
            response = await self.client.get_signatures_for_address(
                pubkey,
                limit=limit,
                commitment=Confirmed
            )
            
            if not response.value:
                logger.info(f"📜 No transactions found for {wallet_address[:8]}...")
                return {
                    "success": True,
                    "wallet_address": wallet_address,
                    "transactions": [],
                    "count": 0
                }
            
            transactions = []
            for sig_info in response.value:
                tx_data = {
                    "signature": str(sig_info.signature),
                    "slot": sig_info.slot,
                    "status": "success" if sig_info.err is None else "error"
                }
                
                # Add block_time if available
                if hasattr(sig_info, 'block_time') and sig_info.block_time:
                    tx_data["block_time"] = sig_info.block_time
                
                transactions.append(tx_data)
            
            logger.info(f"📜 Found {len(transactions)} transactions for {wallet_address[:8]}...")
            
            return {
                "success": True,
                "wallet_address": wallet_address,
                "transactions": transactions,
                "count": len(transactions)
            }
        except Exception as e:
            logger.error(f"❌ Error getting transactions for {wallet_address[:8] if wallet_address else 'unknown'}: {e}")
            return {
                "success": False,
                "error": str(e),
                "wallet_address": wallet_address
            }
    
    async def close(self):
        """Close the RPC client connection"""
        if self.client:
            await self.client.close()
            logger.info("🔌 Solana RPC client closed")


"""
DeFi protocol tools
Tools para interagir com protocolos DeFi (Jupiter, etc)
"""

from .base import Tool
import aiohttp
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class JupiterPriceTool(Tool):
    """Tool para buscar preços de tokens via Jupiter API"""
    
    # Token mints conhecidos (Solana mainnet)
    KNOWN_TOKENS = {
        "SOL": "So11111111111111111111111111111111111111112",
        "USDC": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        "USDT": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
        "BONK": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
        "JUP": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
    }
    
    # Fallback prices (for offline/demo mode)
    FALLBACK_PRICES = {
        "SOL": 145.50,
        "USDC": 1.00,
        "USDT": 1.00,
        "BONK": 0.000015,
        "JUP": 0.85,
    }
    
    def __init__(self, fallback_mode: bool = False):
        super().__init__(
            name="jupiter_price",
            description="Get real-time token prices from Jupiter aggregator"
        )
        # Jupiter Lite API - endpoint correto!
        self.quote_url = "https://lite-api.jup.ag/swap/v1/quote"
        self.fallback_mode = fallback_mode
        if fallback_mode:
            logger.info("⚠️ Jupiter Price Tool in FALLBACK mode (using mock prices)")
        else:
            logger.info("✅ Jupiter Lite API initialized (lite-api.jup.ag)")
    
    async def execute(self, token: str, **kwargs) -> Dict[str, Any]:
        """
        Get token price from Jupiter
        
        Args:
            token: Token symbol (SOL, USDC, etc) or mint address
            **kwargs: Additional parameters
        
        Returns:
            Dict with price data
        """
        token_upper = token.upper()
        token_mint = self.KNOWN_TOKENS.get(token_upper, token)
        
        # Use fallback mode if enabled or requested
        use_fallback = self.fallback_mode or kwargs.get("fallback", False)
        
        if use_fallback:
            # Use fallback prices
            price = self.FALLBACK_PRICES.get(token_upper, 0)
            logger.info(f"💵 Price for {token} (FALLBACK): ${price:.4f}")
            
            return {
                "success": True,
                "token": token,
                "token_mint": token_mint,
                "price_usd": price,
                "source": "fallback",
                "timestamp": None
            }
        
        # Try to fetch real price via Jupiter Lite API
        try:
            logger.info(f"💵 Fetching price for {token} via Jupiter Lite API...")
            
            # Use USDC as output to get price (1 token -> USDC)
            usdc_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
            # 1 token in smallest units (assume 9 decimals like SOL)
            amount = 1_000_000_000
            
            async with aiohttp.ClientSession() as session:
                params = {
                    "inputMint": token_mint,
                    "outputMint": usdc_mint,
                    "amount": amount,
                    "slippageBps": 50
                }
                
                async with session.get(
                    self.quote_url,
                    params=params,
                    timeout=10
                ) as response:
                    if response.status != 200:
                        logger.warning(f"⚠️ Jupiter API returned status {response.status}, using fallback")
                        price = self.FALLBACK_PRICES.get(token_upper, 0)
                        return {
                            "success": True,
                            "token": token,
                            "token_mint": token_mint,
                            "price_usd": price,
                            "source": "fallback",
                            "note": f"API returned status {response.status}"
                        }
                    
                    data = await response.json()
                    
                    # Calculate price from quote
                    # outAmount is in USDC lamports (6 decimals)
                    out_amount = int(data.get("outAmount", 0))
                    price = out_amount / 1_000_000  # Convert USDC lamports to dollars
                    
                    logger.info(f"💵 Price for {token}: ${price:.4f} (REAL from Jupiter)")
                    
                    return {
                        "success": True,
                        "token": token,
                        "token_mint": token_mint,
                        "price_usd": price,
                        "source": "jupiter_lite_api",
                        "timestamp": None
                    }
        
        except Exception as e:
            logger.warning(f"⚠️ Error fetching price for {token}, using fallback: {e}")
            price = self.FALLBACK_PRICES.get(token_upper, 0)
            return {
                "success": True,
                "token": token,
                "token_mint": token_mint,
                "price_usd": price,
                "source": "fallback",
                "note": f"Error: {str(e)}"
            }


class JupiterQuoteTool(Tool):
    """Tool para buscar quotes de swap via Jupiter"""
    
    def __init__(self):
        super().__init__(
            name="jupiter_quote",
            description="Get swap quotes from Jupiter aggregator"
        )
        self.base_url = "https://quote-api.jup.ag/v6"
        logger.info("✅ Jupiter Quote API initialized")
    
    async def execute(
        self,
        input_token: str,
        output_token: str,
        amount: float,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get swap quote from Jupiter
        
        Args:
            input_token: Input token mint or symbol
            output_token: Output token mint or symbol
            amount: Amount to swap (in token units)
            **kwargs: Additional parameters (slippage_bps, etc)
        
        Returns:
            Dict with quote data
        """
        try:
            # Convert symbols to mints if needed
            input_mint = JupiterPriceTool.KNOWN_TOKENS.get(input_token.upper(), input_token)
            output_mint = JupiterPriceTool.KNOWN_TOKENS.get(output_token.upper(), output_token)
            
            # Convert amount to smallest unit (assuming 9 decimals like SOL)
            decimals = kwargs.get("decimals", 9)
            amount_smallest = int(amount * (10 ** decimals))
            
            slippage_bps = kwargs.get("slippage_bps", 50)  # 0.5% default
            
            logger.info(f"💱 Getting quote: {amount} {input_token} → {output_token}")
            
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/quote"
                params = {
                    "inputMint": input_mint,
                    "outputMint": output_mint,
                    "amount": amount_smallest,
                    "slippageBps": slippage_bps
                }
                
                async with session.get(url, params=params, timeout=10) as response:
                    if response.status != 200:
                        logger.error(f"❌ Jupiter API returned status {response.status}")
                        return {
                            "success": False,
                            "error": f"API returned status {response.status}",
                            "input_token": input_token,
                            "output_token": output_token
                        }
                    
                    data = await response.json()
                    
                    # Parse output amount
                    out_amount_smallest = int(data.get("outAmount", 0))
                    out_amount = out_amount_smallest / (10 ** decimals)
                    
                    # Parse price impact
                    price_impact = float(data.get("priceImpactPct", 0))
                    
                    logger.info(f"💱 Quote: {amount} {input_token} → {out_amount:.4f} {output_token} (impact: {price_impact}%)")
                    
                    return {
                        "success": True,
                        "input_token": input_token,
                        "output_token": output_token,
                        "input_amount": amount,
                        "output_amount": out_amount,
                        "price_impact_pct": price_impact,
                        "route": data.get("routePlan", []),
                        "source": "jupiter"
                    }
        
        except aiohttp.ClientError as e:
            logger.error(f"❌ HTTP error getting quote: {e}")
            return {
                "success": False,
                "error": f"HTTP error: {str(e)}",
                "input_token": input_token,
                "output_token": output_token
            }
        except Exception as e:
            logger.error(f"❌ Error getting quote: {e}")
            return {
                "success": False,
                "error": str(e),
                "input_token": input_token,
                "output_token": output_token
            }


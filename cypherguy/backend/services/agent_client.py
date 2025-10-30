"""
Cliente para comunicar com os agents uAgents - VERSÃO REAL COM HTTP
"""

import aiohttp
import asyncio
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class AgentClient:
    """Cliente para comunicação com agents via HTTP"""
    
    def __init__(self):
        # HTTP endpoints dos agents
        self.intake_endpoint = "http://localhost:8101"
        self.policy_endpoint = "http://localhost:8102"
        self.compute_endpoint = "http://localhost:8103"
        self.executor_endpoint = "http://localhost:8104"
        
        logger.info("🔗 AgentClient initialized")
        logger.info(f"   Intake:  {self.intake_endpoint}")
        logger.info(f"   Policy:  {self.policy_endpoint}")
        logger.info(f"   Compute: {self.compute_endpoint}")
        logger.info(f"   Executor: {self.executor_endpoint}")
    
    async def _check_agent_health(self, agent_name: str, endpoint: str) -> bool:
        """Verificar se um agent está online"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{endpoint}/health", timeout=aiohttp.ClientTimeout(total=2)) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.debug(f"✅ {agent_name} is healthy")
                        return True
                    else:
                        logger.warning(f"⚠️ {agent_name} returned status {response.status}")
                        return False
        except Exception as e:
            logger.error(f"❌ {agent_name} is unreachable: {e}")
            return False
    
    async def check_all_agents_health(self) -> Dict[str, bool]:
        """Verificar saúde de todos os agents"""
        results = {
            "intake": await self._check_agent_health("IntakeAgent", self.intake_endpoint),
            "policy": await self._check_agent_health("PolicyAgent", self.policy_endpoint),
            "compute": await self._check_agent_health("ComputeAgent", self.compute_endpoint),
            "executor": await self._check_agent_health("ExecutorAgent", self.executor_endpoint),
        }
        return results
    
    async def process_credit_request(
        self, 
        user_id: str, 
        amount: float, 
        token: str, 
        collateral: str
    ) -> Dict[str, Any]:
        """
        Processar requisição de crédito através da cadeia de agents
        
        Flow: Backend → Intake → Policy → Compute → Executor → Response
        """
        
        logger.info("=" * 80)
        logger.info(f"🚀 STARTING CREDIT REQUEST")
        logger.info(f"   User: {user_id}")
        logger.info(f"   Amount: ${amount}")
        logger.info(f"   Token: {token}")
        logger.info(f"   Collateral: {collateral}")
        logger.info("=" * 80)
        
        try:
            # Call Intake Agent (que vai chamar os outros)
            logger.info("📤 [1/4] Sending to IntakeAgent...")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.intake_endpoint}/process_credit",
                    json={
                        "user_id": user_id,
                        "amount": amount,
                        "token": token,
                        "collateral": collateral
                    },
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        logger.info("=" * 80)
                        logger.info(f"✅ CREDIT REQUEST COMPLETED")
                        logger.info(f"   Approved: {result.get('approved', False)}")
                        logger.info(f"   Rate: {result.get('rate', 'N/A')}%")
                        logger.info(f"   TX Hash: {result.get('tx_hash', 'N/A')[:16]}...")
                        logger.info(f"   Message: {result.get('message', 'N/A')}")
                        logger.info("=" * 80)
                        
                        return result
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ Intake agent returned {response.status}: {error_text}")
                        return {
                            "success": False,
                            "approved": False,
                            "message": f"Intake agent error: {response.status}"
                        }
        
        except asyncio.TimeoutError:
            logger.error("❌ Request timed out (30s)")
            return {
                "success": False,
                "approved": False,
                "message": "Request timed out - agents may be offline"
            }
        except Exception as e:
            logger.error(f"❌ Error processing credit request: {e}")
            return {
                "success": False,
                "approved": False,
                "message": f"Error: {str(e)}"
            }
    
    async def process_rwa_request(
        self,
        user_id: str,
        property_value: float,
        location: str,
        property_type: str
    ) -> Dict[str, Any]:
        """Processar requisição de RWA através da cadeia de agents"""
        
        logger.info("=" * 80)
        logger.info(f"🚀 STARTING RWA REQUEST")
        logger.info(f"   User: {user_id}")
        logger.info(f"   Property Value: ${property_value}")
        logger.info(f"   Location: {location}")
        logger.info(f"   Type: {property_type}")
        logger.info("=" * 80)
        
        try:
            logger.info("📤 [1/4] Sending to IntakeAgent...")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.intake_endpoint}/process_rwa",
                    json={
                        "user_id": user_id,
                        "property_value": property_value,
                        "location": location,
                        "property_type": property_type
                    },
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        logger.info("=" * 80)
                        logger.info(f"✅ RWA REQUEST COMPLETED")
                        logger.info(f"   Approved: {result.get('approved', False)}")
                        logger.info(f"   Token Supply: {result.get('token_supply', 'N/A')}")
                        logger.info(f"   TX Hash: {result.get('tx_hash', 'N/A')[:16]}...")
                        logger.info(f"   Message: {result.get('message', 'N/A')}")
                        logger.info("=" * 80)
                        
                        return result
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ Intake agent returned {response.status}: {error_text}")
                        return {
                            "success": False,
                            "approved": False,
                            "message": f"Intake agent error: {response.status}"
                        }
        
        except Exception as e:
            logger.error(f"❌ Error processing RWA request: {e}")
            return {
                "success": False,
                "approved": False,
                "message": f"Error: {str(e)}"
            }
    
    async def process_trade_request(
        self,
        user_id: str,
        sell_amount: float,
        sell_token: str,
        buy_token: str
    ) -> Dict[str, Any]:
        """Processar requisição de trade através da cadeia de agents"""
        
        logger.info("=" * 80)
        logger.info(f"🚀 STARTING TRADE REQUEST")
        logger.info(f"   User: {user_id}")
        logger.info(f"   Selling: {sell_amount} {sell_token}")
        logger.info(f"   Buying: {buy_token}")
        logger.info("=" * 80)
        
        try:
            logger.info("📤 [1/4] Sending to IntakeAgent...")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.intake_endpoint}/process_trade",
                    json={
                        "user_id": user_id,
                        "sell_amount": sell_amount,
                        "sell_token": sell_token,
                        "buy_token": buy_token
                    },
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        logger.info("=" * 80)
                        logger.info(f"✅ TRADE REQUEST COMPLETED")
                        logger.info(f"   Matched: {result.get('matched', False)}")
                        logger.info(f"   Price: ${result.get('match_price', 'N/A')}")
                        logger.info(f"   TX Hash: {result.get('tx_hash', 'N/A')[:16]}...")
                        logger.info(f"   Message: {result.get('message', 'N/A')}")
                        logger.info("=" * 80)
                        
                        return result
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ Intake agent returned {response.status}: {error_text}")
                        return {
                            "success": False,
                            "matched": False,
                            "message": f"Intake agent error: {response.status}"
                        }
        
        except Exception as e:
            logger.error(f"❌ Error processing trade request: {e}")
            return {
                "success": False,
                "matched": False,
                "message": f"Error: {str(e)}"
            }
    
    async def process_automation_request(
        self,
        user_id: str,
        portfolio_value: float,
        strategy: str
    ) -> Dict[str, Any]:
        """Processar requisição de automação através da cadeia de agents"""
        
        logger.info("=" * 80)
        logger.info(f"🚀 STARTING AUTOMATION REQUEST")
        logger.info(f"   User: {user_id}")
        logger.info(f"   Portfolio: ${portfolio_value}")
        logger.info(f"   Strategy: {strategy}")
        logger.info("=" * 80)
        
        try:
            logger.info("📤 [1/4] Sending to IntakeAgent...")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.intake_endpoint}/process_automation",
                    json={
                        "user_id": user_id,
                        "portfolio_value": portfolio_value,
                        "strategy": strategy
                    },
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        logger.info("=" * 80)
                        logger.info(f"✅ AUTOMATION REQUEST COMPLETED")
                        logger.info(f"   Approved: {result.get('approved', False)}")
                        logger.info(f"   Expected APY: {result.get('expected_apy', 'N/A')}%")
                        logger.info(f"   TX Hash: {result.get('tx_hash', 'N/A')[:16]}...")
                        logger.info(f"   Message: {result.get('message', 'N/A')}")
                        logger.info("=" * 80)
                        
                        return result
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ Intake agent returned {response.status}: {error_text}")
                        return {
                            "success": False,
                            "approved": False,
                            "message": f"Intake agent error: {response.status}"
                        }
        
        except Exception as e:
            logger.error(f"❌ Error processing automation request: {e}")
            return {
                "success": False,
                "approved": False,
                "message": f"Error: {str(e)}"
            }

# Singleton
agent_client = AgentClient()

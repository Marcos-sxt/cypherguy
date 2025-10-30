#!/usr/bin/env python3
"""
CypherGuy Backend - Main FastAPI Application

This is the main entry point for the CypherGuy backend API.
It provides endpoints for the 4 main use cases:
1. Private DeFi Credit
2. RWA Compliance  
3. Dark Pool Trading
4. DeFi Automations
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import asyncio
import logging

# Import agent client
from services.agent_client import agent_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="CypherGuy API",
    description="Personal DeFi Assistant API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API requests/responses
class CreditRequest(BaseModel):
    amount: float
    token: str = "USDC"
    collateral: str = "SOL"
    user_id: str

class CreditResponse(BaseModel):
    approved: bool
    rate: Optional[float] = None
    message: str
    tx_hash: Optional[str] = None

class RWARequest(BaseModel):
    property_value: float
    location: str
    property_type: str
    user_id: str

class RWAResponse(BaseModel):
    compliant: bool
    token_id: Optional[str] = None
    message: str
    tx_hash: Optional[str] = None

class TradeRequest(BaseModel):
    sell_amount: float
    sell_token: str
    buy_token: str
    user_id: str

class TradeResponse(BaseModel):
    matched: bool
    price: Optional[float] = None
    message: str
    tx_hash: Optional[str] = None

class AutomationRequest(BaseModel):
    portfolio_value: float
    strategy: str
    user_id: str

class AutomationResponse(BaseModel):
    optimized: bool
    new_allocation: Optional[Dict[str, float]] = None
    message: str
    tx_hash: Optional[str] = None

# Note: Backend now uses agent_client from services/agent_client.py
# which communicates with the actual uAgents agents

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "🦸 Welcome to CypherGuy API!",
        "version": "0.1.0",
        "endpoints": {
            "credit": "/credit",
            "rwa": "/rwa",
            "trade": "/trade",
            "automation": "/automation"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "cypherguy-backend"}

@app.post("/credit", response_model=CreditResponse)
async def request_credit(request: CreditRequest):
    """
    Request a private DeFi credit loan
    
    This endpoint processes credit requests through the agent system:
    - AgentIntake authenticates and parses request
    - AgentPolicy checks credit limits
    - AgentCompute calculates credit score and rate (Arcium MPC)
    - AgentExecutor executes the loan on Solana
    """
    try:
        logger.info(f"Processing credit request: {request}")
        
        # Use agent_client to process through agent system
        result = await agent_client.process_credit_request(
            user_id=request.user_id,
            amount=request.amount,
            token=request.token,
            collateral=request.collateral
        )
        
        if not result.get("success"):
            return CreditResponse(
                approved=False,
                message=result.get("message", "Credit request failed")
            )
        
        return CreditResponse(
            approved=result.get("approved", False),
            rate=result.get("rate"),
            message=result.get("message"),
            tx_hash=result.get("tx_hash")
        )
        
    except Exception as e:
        logger.error(f"Error processing credit request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rwa", response_model=RWAResponse)
async def tokenize_rwa(request: RWARequest):
    """
    Tokenize real-world assets with compliance
    
    This endpoint processes RWA tokenization through the agent system:
    - AgentIntake parses property data
    - AgentPolicy checks compliance rules (MeTTa)
    - AgentCompute validates legal requirements
    - AgentExecutor creates SPL token on Solana
    """
    try:
        logger.info(f"Processing RWA tokenization request: {request}")
        
        # Use agent_client to process through agent system
        result = await agent_client.process_rwa_request(
            user_id=request.user_id,
            property_value=request.property_value,
            location=request.location,
            property_type=request.property_type
        )
        
        if not result.get("success"):
            return RWAResponse(
                compliant=False,
                message=result.get("message", "RWA tokenization failed")
            )
        
        return RWAResponse(
            compliant=result.get("approved", False),
            token_id=f"RWA_{request.user_id}_{int(request.property_value)}",
            message=result.get("message"),
            tx_hash=result.get("tx_hash")
        )
        
    except Exception as e:
        logger.error(f"Error processing RWA request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/trade", response_model=TradeResponse)
async def execute_dark_pool_trade(request: TradeRequest):
    """
    Execute a private dark pool trade
    
    This endpoint processes trades through the agent system:
    - AgentIntake encrypts order details
    - AgentPolicy checks trading limits
    - AgentCompute matches orders privately (Arcium MPC)
    - AgentExecutor executes swap on Solana
    """
    try:
        logger.info(f"Processing dark pool trade request: {request}")
        
        # Use agent_client to process through agent system
        result = await agent_client.process_trade_request(
            user_id=request.user_id,
            sell_amount=request.sell_amount,
            sell_token=request.sell_token,
            buy_token=request.buy_token
        )
        
        if not result.get("success"):
            return TradeResponse(
                matched=False,
                message=result.get("message", "Trade failed")
            )
        
        return TradeResponse(
            matched=result.get("matched", False),
            price=result.get("match_price"),
            message=result.get("message"),
            tx_hash=result.get("tx_hash")
        )
        
    except Exception as e:
        logger.error(f"Error processing trade request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/automation", response_model=AutomationResponse)
async def optimize_portfolio(request: AutomationRequest):
    """
    Automatically optimize portfolio allocation
    
    This endpoint processes automation through the agent system:
    - AgentIntake monitors market data
    - AgentPolicy checks rebalance rules
    - AgentCompute optimizes allocation
    - AgentExecutor executes rebalance
    """
    try:
        logger.info(f"Processing automation request: {request}")
        
        # Use agent_client to process through agent system
        result = await agent_client.process_automation_request(
            user_id=request.user_id,
            portfolio_value=request.portfolio_value,
            strategy=request.strategy
        )
        
        if not result.get("success"):
            return AutomationResponse(
                optimized=False,
                message=result.get("message", "Automation failed")
            )
        
        return AutomationResponse(
            optimized=result.get("approved", False),
            new_allocation=result.get("allocation"),
            message=result.get("message"),
            tx_hash=result.get("tx_hash")
        )
        
    except Exception as e:
        logger.error(f"Error processing automation request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info("🦸 Starting CypherGuy Backend...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

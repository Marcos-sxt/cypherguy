#!/usr/bin/env python3
"""
CypherGuy API Test Script

This script tests all the main API endpoints to ensure they're working correctly.
"""

import requests
import json
import time
from typing import Dict, Any

# API base URL
BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint: str, method: str = "GET", data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing {endpoint}: {e}")
        return {"error": str(e)}

def test_root():
    """Test root endpoint"""
    print("🧪 Testing root endpoint...")
    result = test_endpoint("/")
    print(f"✅ Root endpoint: {result}")
    return result

def test_health():
    """Test health check endpoint"""
    print("🧪 Testing health check...")
    result = test_endpoint("/health")
    print(f"✅ Health check: {result}")
    return result

def test_credit():
    """Test credit endpoint"""
    print("🧪 Testing credit endpoint...")
    
    credit_request = {
        "amount": 1000.0,
        "token": "USDC",
        "collateral": "SOL",
        "user_id": "test_user_123"
    }
    
    result = test_endpoint("/credit", "POST", credit_request)
    print(f"✅ Credit request: {result}")
    return result

def test_rwa():
    """Test RWA endpoint"""
    print("🧪 Testing RWA endpoint...")
    
    rwa_request = {
        "property_value": 500000.0,
        "location": "New York",
        "property_type": "Residential",
        "user_id": "test_user_123"
    }
    
    result = test_endpoint("/rwa", "POST", rwa_request)
    print(f"✅ RWA request: {result}")
    return result

def test_trade():
    """Test trade endpoint"""
    print("🧪 Testing trade endpoint...")
    
    trade_request = {
        "sell_amount": 100.0,
        "sell_token": "SOL",
        "buy_token": "USDC",
        "user_id": "test_user_123"
    }
    
    result = test_endpoint("/trade", "POST", trade_request)
    print(f"✅ Trade request: {result}")
    return result

def test_automation():
    """Test automation endpoint"""
    print("🧪 Testing automation endpoint...")
    
    automation_request = {
        "portfolio_value": 10000.0,
        "strategy": "yield_optimizer",
        "user_id": "test_user_123"
    }
    
    result = test_endpoint("/automation", "POST", automation_request)
    print(f"✅ Automation request: {result}")
    return result

def main():
    """Run all tests"""
    print("🦸 Starting CypherGuy API Tests...")
    print("=" * 50)
    
    # Test basic endpoints
    test_root()
    test_health()
    
    print("\n" + "=" * 50)
    print("🧪 Testing Use Cases...")
    
    # Test all use cases
    test_credit()
    test_rwa()
    test_trade()
    test_automation()
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print("\nTo view the API documentation, visit:")
    print(f"📚 {BASE_URL}/docs")
    print(f"📚 {BASE_URL}/redoc")

if __name__ == "__main__":
    main()

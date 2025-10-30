"""
Testes básicos de importação dos agents
"""

import sys
import os

# Adicionar o diretório parent ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_import_intake_agent():
    """Testar que AgentIntake pode ser importado"""
    try:
        from agents import intake_agent
        assert intake_agent.intake_agent is not None
        print("✅ AgentIntake imported successfully")
        return True
    except Exception as e:
        print(f"❌ AgentIntake import failed: {e}")
        return False

def test_import_policy_agent():
    """Testar que AgentPolicy pode ser importado"""
    try:
        from agents import policy_agent
        assert policy_agent.policy_agent is not None
        print("✅ AgentPolicy imported successfully")
        return True
    except Exception as e:
        print(f"❌ AgentPolicy import failed: {e}")
        return False

def test_import_compute_agent():
    """Testar que AgentCompute pode ser importado"""
    try:
        from agents import compute_agent
        assert compute_agent.compute_agent is not None
        print("✅ AgentCompute imported successfully")
        return True
    except Exception as e:
        print(f"❌ AgentCompute import failed: {e}")
        return False

def test_import_executor_agent():
    """Testar que AgentExecutor pode ser importado"""
    try:
        from agents import executor_agent
        assert executor_agent.executor_agent is not None
        print("✅ AgentExecutor imported successfully")
        return True
    except Exception as e:
        print(f"❌ AgentExecutor import failed: {e}")
        return False

def test_policy_rules():
    """Testar PolicyRules"""
    try:
        from agents.policy_agent import PolicyRules
        
        # Testar credit rules
        result = PolicyRules.evaluate_credit({"amount": 5000, "collateral_value": 10000})
        assert result["approved"] == True
        print("✅ PolicyRules credit evaluation works")
        
        # Testar amount muito baixo
        result = PolicyRules.evaluate_credit({"amount": 50, "collateral_value": 100})
        assert result["approved"] == False
        print("✅ PolicyRules rejects low amounts")
        
        return True
    except Exception as e:
        print(f"❌ PolicyRules test failed: {e}")
        return False

def test_compute_functions():
    """Testar compute functions"""
    try:
        from agents.compute_agent import compute_credit_score, compute_rwa_validation
        
        # Testar credit score
        result = compute_credit_score({"amount": 10000})
        assert result["success"] == True
        assert "credit_score" in result["data"]
        print("✅ Compute credit score works")
        
        # Testar RWA validation
        result = compute_rwa_validation({"property_value": 250000})
        assert result["success"] == True
        assert "compliance_score" in result["data"]
        print("✅ Compute RWA validation works")
        
        return True
    except Exception as e:
        print(f"❌ Compute functions test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Running agent tests...")
    print("=" * 50)
    
    tests = [
        test_import_intake_agent,
        test_import_policy_agent,
        test_import_compute_agent,
        test_import_executor_agent,
        test_policy_rules,
        test_compute_functions,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
    
    print("=" * 50)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {len(tests)}")
    
    if failed == 0:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed")
        sys.exit(1)


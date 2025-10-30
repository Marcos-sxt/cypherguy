import os
from typing import List

# Centralized backend settings (env-overridable)

AGENT_INTAKE_URL: str = os.getenv("AGENT_INTAKE_URL", "http://localhost:8101")
AGENT_POLICY_URL: str = os.getenv("AGENT_POLICY_URL", "http://localhost:8102")
AGENT_COMPUTE_URL: str = os.getenv("AGENT_COMPUTE_URL", "http://localhost:8103")
AGENT_EXECUTOR_URL: str = os.getenv("AGENT_EXECUTOR_URL", "http://localhost:8104")

HTTP_TIMEOUT_SECS: float = float(os.getenv("HTTP_TIMEOUT_SECS", "30"))

# CORS
CORS_ORIGINS: List[str] = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()]

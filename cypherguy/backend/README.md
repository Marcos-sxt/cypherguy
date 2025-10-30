# CypherGuy Backend (FastAPI)

Minimal API that orchestrates multi-agent flows (Intake → Policy → Compute → Executor).

## Environment variables

- `AGENT_INTAKE_URL` (default: `http://localhost:8101`)
- `AGENT_POLICY_URL` (default: `http://localhost:8102`)
- `AGENT_COMPUTE_URL` (default: `http://localhost:8103`)
- `AGENT_EXECUTOR_URL` (default: `http://localhost:8104`)
- `HTTP_TIMEOUT_SECS` (default: `30`)
- `CORS_ORIGINS` (default: `*` or comma-separated list)

Example:
```bash
export AGENT_INTAKE_URL="http://localhost:8101"
export AGENT_POLICY_URL="http://localhost:8102"
export AGENT_COMPUTE_URL="http://localhost:8103"
export AGENT_EXECUTOR_URL="http://localhost:8104"
export HTTP_TIMEOUT_SECS="30"
export CORS_ORIGINS="http://localhost:5173"
```

## Run

Agents must be up on ports 8101–8104. Then:
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Health:
```bash
curl -s http://localhost:8000/health
curl -s http://localhost:8000/agents/health
```

Credit test:
```bash
curl -s -X POST http://localhost:8000/credit \
 -H "Content-Type: application/json" \
 -d '{"user_id":"demo","amount":1000,"token":"USDC","collateral":"SOL"}'
```

#!/bin/bash
# Script automatizado para preparar deploy dos agents no Render
# Este script cria um resumo das configurações necessárias para cada agent

set -e

echo "🚀 CypherGuy - Render Agents Deployment Helper"
echo "================================================"
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 Configurações para criar os 4 serviços no Render:${NC}"
echo ""

declare -a agents=(
    "intake:8101:cypherguy-intake-agent"
    "policy:8102:cypherguy-policy-agent"
    "compute:8103:cypherguy-compute-agent"
    "executor:8104:cypherguy-executor-agent"
)

echo "Para cada agent, use estas configurações no Render:"
echo ""

for agent_info in "${agents[@]}"; do
    IFS=':' read -r agent_name port service_name <<< "$agent_info"
    
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}Agent: ${agent_name^}Agent${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "  Name:              $service_name"
    echo "  Environment:       Python 3"
    echo "  Region:            Oregon (US West)"
    echo "  Branch:            main"
  echo "  Root Directory:    agents"
  echo "  Build Command:     pip install -r requirements.txt"
  echo "  Start Command:     python ${agent_name}_agent.py"
  echo "                       (Render já está na pasta agents/, então funciona direto)"
    echo "  Instance Type:     Free"
    echo ""
    echo "  Environment Variables:"
    echo "    PORT=$port (opcional, Render usa automaticamente)"
    if [ "$agent_name" == "intake" ]; then
        echo "    PERPLEXITY_API_KEY=your_key (opcional)"
    fi
    echo ""
    echo "  Health Check URL:"
    echo "    https://${service_name}.onrender.com/health"
    echo ""
done

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}📝 Próximos Passos:${NC}"
echo ""
echo "1. Acesse: https://dashboard.render.com"
echo "2. Clique em 'New +' → 'Web Service'"
echo "3. Conecte seu repositório GitHub"
echo "4. Para CADA agent (4x), repita:"
echo "   - Use as configurações acima"
echo "   - Crie um novo serviço"
echo ""
echo "5. Após deploy de todos os 4 agents, atualize o backend no Render:"
echo "   Environment Variables → Adicionar:"
echo "     AGENT_INTAKE_URL=https://cypherguy-intake-agent.onrender.com"
echo "     AGENT_POLICY_URL=https://cypherguy-policy-agent.onrender.com"
echo "     AGENT_COMPUTE_URL=https://cypherguy-compute-agent.onrender.com"
echo "     AGENT_EXECUTOR_URL=https://cypherguy-executor-agent.onrender.com"
echo ""
echo "6. Teste os health checks:"
for agent_info in "${agents[@]}"; do
    IFS=':' read -r agent_name port service_name <<< "$agent_info"
    echo "   curl https://${service_name}.onrender.com/health"
done
echo ""
echo -e "${YELLOW}⚠️  IMPORTANTE:${NC}"
echo "   - Free tier do Render pode ter delay de ~50s na primeira requisição"
echo "   - Instâncias 'spin down' após 15 min de inatividade"
echo "   - Após deploy, teste via ASI:One app para confirmar descoberta"
echo ""
echo -e "${GREEN}✅ Commit feito! Agora você pode fazer push e criar os serviços no Render.${NC}"
echo ""


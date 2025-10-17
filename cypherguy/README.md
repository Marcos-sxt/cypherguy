# 🦸 CypherGuy - DeFi Assistant

**CypherGuy** is your personal DeFi assistant that hides all the technical complexity behind a friendly interface.

## 🎯 What is CypherGuy?

CypherGuy is an autonomous, encrypted, and verifiable DeFi execution layer for Solana that makes DeFi accessible to everyone.

### Key Features:
- 💳 **Private DeFi Credit** - Get loans without revealing your full portfolio
- 🏢 **RWA Compliance** - Tokenize real assets following regulations
- 🌑 **Dark Pool Trading** - Trade large amounts without moving the market
- 🤖 **DeFi Automations** - Automatically optimize your portfolio

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CypherGuy Stack                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📱 Frontend (React Native)                               │
│  ├─ Simple UI (no technical jargon)                        │
│  ├─ Tangem integration (tap to sign)                      │
│  └─ Real-time status updates                              │
│                                                             │
│  🤖 Backend (Python + FastAPI)                            │
│  ├─ AgentIntake (parse user requests)                     │
│  ├─ AgentPolicy (MeTTa rules engine)                      │
│  ├─ AgentCompute (Arcium MPC)                             │
│  └─ AgentExecutor (Solana integration)                   │
│                                                             │
│  ⛓️ Blockchain (Solana Devnet)                            │
│  ├─ Anchor program (record operations)                     │
│  ├─ SPL tokens (RWA tokenization)                         │
│  └─ DeFi protocols (Solend, Mango, Jupiter)               │
│                                                             │
│  🔐 Security (Tangem Wallet)                             │
│  ├─ NFC authentication                                     │
│  ├─ Transaction signing                                     │
│  └─ Hardware security (EAL6+)                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- Rust 1.70+
- Solana CLI
- Anchor Framework

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd cypherguy
```

2. **Setup Python environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Setup Solana**
```bash
solana config set --url devnet
solana-keygen new
```

4. **Build Anchor program**
```bash
cd anchor-program
anchor build
```

5. **Run the backend**
```bash
cd ../backend
python main.py
```

## 📁 Project Structure

```
cypherguy/
├── backend/                 # Python FastAPI backend
│   ├── agents/             # Agent implementations
│   ├── api/                # API endpoints
│   └── services/           # Business logic
├── frontend/               # React Native mobile app
│   ├── src/                # Source code
│   └── components/         # UI components
├── anchor-program/         # Solana Anchor program
│   ├── programs/           # Smart contract code
│   └── tests/              # Program tests
├── agents/                 # Agent definitions
│   ├── intake/             # AgentIntake
│   ├── policy/             # AgentPolicy
│   ├── compute/            # AgentCompute
│   └── executor/           # AgentExecutor
└── docs/                   # Documentation
```

## 🎪 Use Cases

### 1. Private DeFi Credit
- **User Story:** "I want to borrow USDC but don't want to reveal my full portfolio"
- **Technology:** Arcium MPC for private credit scoring
- **Implementation:** Solana lending protocols with encrypted computation

### 2. RWA Compliance
- **User Story:** "I want to tokenize my real estate but need to follow regulations"
- **Technology:** MeTTa rules engine for compliance
- **Implementation:** SPL token creation with regulatory validation

### 3. Dark Pool Trading
- **User Story:** "I want to trade large amounts without moving the market"
- **Technology:** Arcium MPC for encrypted order matching
- **Implementation:** Jupiter swap integration with privacy

### 4. DeFi Automations
- **User Story:** "I want my crypto to automatically earn the best yields"
- **Technology:** ASI Alliance agents for autonomous execution
- **Implementation:** Automated portfolio optimization

## 🔧 Development

### Running Tests
```bash
# Backend tests
cd backend
python -m pytest

# Anchor program tests
cd anchor-program
anchor test
```

### Building for Production
```bash
# Build Anchor program
cd anchor-program
anchor build

# Build mobile app
cd frontend
npm run build
```

## 📚 Documentation

- [Technical Implementation Guide](docs/technical_stuff/README.md)
- [Agent Architecture](docs/technical_stuff/asi_alliance/asi-alliance-implementation.md)
- [Privacy Layer](docs/technical_stuff/arcium/arcium-implementation.md)
- [Solana Integration](docs/technical_stuff/solana/solana-implementation.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation:** [docs/](docs/)
- **Issues:** [GitHub Issues](https://github.com/your-org/cypherguy/issues)
- **Discord:** [CypherGuy Community](https://discord.gg/cypherguy)

---

**Ready to build the future of DeFi?** 🦸‍♂️

Let's make DeFi accessible to everyone!

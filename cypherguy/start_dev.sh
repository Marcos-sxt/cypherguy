#!/bin/bash

# CypherGuy Development Startup Script

echo "🦸 Starting CypherGuy Development Environment..."
echo "================================================"

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the cypherguy directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Check if Solana CLI is installed
if ! command -v solana &> /dev/null; then
    echo "❌ Error: Solana CLI not found. Please install it first."
    echo "   Run: cargo install solana-cli"
    exit 1
fi

# Check if Anchor is installed
if ! command -v anchor &> /dev/null; then
    echo "❌ Error: Anchor not found. Please install it first."
    echo "   Run: cargo install --git https://github.com/coral-xyz/anchor avm --locked --force"
    exit 1
fi

# Configure Solana for devnet
echo "⛓️ Configuring Solana for devnet..."
solana config set --url devnet

# Check Solana connection
echo "🔍 Checking Solana connection..."
if solana cluster-version &> /dev/null; then
    echo "✅ Solana devnet connection successful"
else
    echo "⚠️ Warning: Could not connect to Solana devnet"
fi

# Build Anchor program
echo "🔨 Building Anchor program..."
cd anchor-program
if anchor build; then
    echo "✅ Anchor program built successfully"
else
    echo "⚠️ Warning: Anchor program build failed (this is expected for MVP)"
fi
cd ..

# Start the backend
echo "🚀 Starting CypherGuy backend..."
echo "================================================"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "📚 ReDoc: http://localhost:8000/redoc"
echo "🧪 Test Script: python test_api.py"
echo "================================================"

# Start the FastAPI server
cd backend
python main.py

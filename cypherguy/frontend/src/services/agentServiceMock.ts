/**
 * Mock Agent Service - 100% mocked responses
 * Use this if IntakeAgent connection fails
 */

export interface ChatResponse {
  response: string;
  user_id: string;
  intent?: string;
}

/**
 * Mock chat responses based on user input
 */
export async function sendChatMessageMock(message: string, userId: string = 'default_user'): Promise<ChatResponse> {
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 500));
  
  const textLower = message.toLowerCase();
  
  // Extract numbers
  const numbers = message.match(/\d+/g);
  const amounts = numbers ? numbers.map(n => parseInt(n)).filter(n => n > 0) : [];
  
  // Check for tokens
  const tokens: string[] = [];
  ['usdc', 'sol', 'eth', 'usdt', 'btc'].forEach(token => {
    if (textLower.includes(token)) {
      tokens.push(token.toUpperCase());
    }
  });
  
  // Intent detection (same logic as IntakeAgent)
  const normalizedText = textLower.replace('do borrow', 'borrow').replace('to borrow', 'borrow');
  
  // Credit intent
  if (normalizedText.includes('credit') || normalizedText.includes('loan') || normalizedText.includes('borrow')) {
    if (amounts.length > 0 && tokens.length > 0) {
      return {
        response: `✅ Perfect! Processing your credit request:\n\n💰 Amount: ${amounts[0]} USDC\n🔒 Collateral: ${tokens[0]}\n\n🔍 Checking credit policy...\n📊 Calculating credit score...\n\n⏳ This may take a moment while I contact PolicyAgent and ComputeAgent!`,
        user_id: userId,
        intent: 'credit',
      };
    } else if (amounts.length > 0) {
      return {
        response: `✅ Amount: ${amounts[0]} USDC\n\nWhat collateral would you like to use?\n(e.g., SOL, ETH, USDC)`,
        user_id: userId,
        intent: 'credit',
      };
    } else {
      return {
        response: `💳 I can help you get a private DeFi loan!\n\nI'll need:\n- Amount (USDC)\n- Collateral type\n\nYour credit score will be calculated privately using MPC. How much would you like to borrow?`,
        user_id: userId,
        intent: 'credit',
      };
    }
  }
  
  // RWA intent
  if (textLower.includes('rwa') || textLower.includes('tokenize') || textLower.includes('property') || textLower.includes('asset')) {
    return {
      response: `🏢 I can help tokenize your real-world assets!\n\nI'll need:\n- Property value\n- Location\n- Property type\n\nI'll check compliance rules automatically. What asset would you like to tokenize?`,
      user_id: userId,
    };
  }
  
  // Trade intent
  if (textLower.includes('trade') || textLower.includes('swap') || textLower.includes('exchange')) {
    return {
      response: `🌑 I can help you trade privately in a dark pool!\n\nI'll need:\n- Amount to sell\n- Tokens (from/to)\n\nYour order will be matched privately without moving the market. What would you like to trade?`,
      user_id: userId,
    };
  }
  
  // Automation intent
  if (textLower.includes('automat') || textLower.includes('optimize') || textLower.includes('manage')) {
    return {
      response: `🤖 I can automatically optimize your portfolio!\n\nI'll need:\n- Portfolio value\n- Strategy (yield farming, balanced, etc)\n\nI'll monitor markets 24/7 and rebalance for best yields. What strategy interests you?`,
      user_id: userId,
    };
  }
  
  // Help intent
  if (textLower.includes('help') || textLower.includes('what') || textLower.includes('how')) {
    return {
      response: `🦸 I'm CypherGuy - your personal DeFi assistant!\n\nI help you with complex DeFi operations using AI agents:\n\n💳 **Private DeFi Credit** - Get loans without revealing your portfolio\n🏢 **RWA Compliance** - Tokenize real-world assets following regulations\n🌑 **Dark Pool Trading** - Trade large amounts privately\n🤖 **DeFi Automation** - Auto-optimize for best yields\n\nJust tell me what you need!`,
      user_id: userId,
    };
  }
  
  // Greeting
  if (textLower.includes('hi') || textLower.includes('hello') || textLower.includes('hey')) {
    return {
      response: `👋 Hi! I'm CypherGuy, your DeFi assistant!\n\nI can help you with:\n💳 Private DeFi Credit\n🏢 RWA Tokenization\n🌑 Dark Pool Trading\n🤖 DeFi Automation\n\nWhat would you like to do?`,
      user_id: userId,
    };
  }
  
  // Default
  return {
    response: `I can help with:\n💳 Credit/Loans\n🏢 RWA Tokenization\n🌑 Private Trading\n🤖 Portfolio Automation\n\nWhich one interests you? Just tell me what you'd like to do!`,
    user_id: userId,
  };
}


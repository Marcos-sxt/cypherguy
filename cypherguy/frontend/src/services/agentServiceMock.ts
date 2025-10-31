/**
 * Mock Agent Service - 100% mocked responses with refined conversations
 * Enhanced with context-aware responses and longer conversation flows
 */

export interface ChatResponse {
  response: string;
  user_id: string;
  intent?: string;
}

interface ConversationContext {
  intent?: string;
  amount?: number;
  collateral?: string;
  step?: string;
  messages: string[];
}

// Simple in-memory context store (per user session)
const conversationContexts = new Map<string, ConversationContext>();

/**
 * Enhanced mock chat responses with context-aware, refined conversations
 */
export async function sendChatMessageMock(
  message: string, 
  userId: string = 'default_user',
  previousMessages?: Array<{ role: string; content: string }>
): Promise<ChatResponse> {
  // Simulate network delay (realistic response time)
  await new Promise(resolve => setTimeout(resolve, 800 + Math.random() * 500));
  
  const textLower = message.toLowerCase();
  
  // Get or create conversation context
  let context = conversationContexts.get(userId) || {
    intent: undefined,
    amount: undefined,
    collateral: undefined,
    step: 'initial',
    messages: []
  };
  
  // Extract numbers and tokens
  const numbers = message.match(/\d+/g);
  const amounts = numbers ? numbers.map(n => parseInt(n)).filter(n => n > 0) : [];
  
  const tokens: string[] = [];
  ['usdc', 'sol', 'eth', 'usdt', 'btc'].forEach(token => {
    if (textLower.includes(token)) {
      tokens.push(token.toUpperCase());
    }
  });
  
  const normalizedText = textLower.replace('do borrow', 'borrow').replace('to borrow', 'borrow');
  
  // Update context based on current message
  context.messages.push(message);
  
  // ===== CREDIT FLOW (Enhanced with longer conversations) =====
  if (normalizedText.includes('credit') || normalizedText.includes('loan') || normalizedText.includes('borrow') || context.intent === 'credit') {
    context.intent = 'credit';
    
    // Step 1: Initial interest in credit
    if (context.step === 'initial' && amounts.length === 0 && tokens.length === 0) {
      context.step = 'credit_amount';
      conversationContexts.set(userId, context);
      return {
        response: `💳 Great! I can help you get a private DeFi loan with some really cool benefits:\n\n✨ **Privacy-First**: Your full portfolio stays private - we only need collateral\n🔒 **Secure**: Uses Multi-Party Computation (MPC) for credit scoring\n⚡ **Fast**: No traditional banks, just smart contracts\n💰 **Flexible**: Borrow in USDC against your crypto assets\n\nTo get started, I'll need:\n1️⃣ The amount you want to borrow (in USDC)\n2️⃣ What you'd like to use as collateral (SOL, ETH, BTC, etc.)\n\n**How much USDC would you like to borrow?**`,
        user_id: userId,
        intent: 'credit',
      };
    }
    
    // Step 2: User provided amount
    if (context.step === 'credit_amount' && amounts.length > 0 && !context.amount) {
      context.amount = amounts[0];
      
      if (tokens.length > 0) {
        // User provided both amount and collateral
        context.collateral = tokens[0];
        context.step = 'processing';
        conversationContexts.set(userId, context);
        return {
          response: `✅ Perfect! I've got your request:\n\n💰 **Amount**: ${amounts[0]} USDC\n🔒 **Collateral**: ${tokens[0]}\n\nNow let me work my magic! 🔮\n\n📋 **Step 1/3**: Checking policy rules...\n   → Validating amount limits (min: $100, max: $100k)\n   → Ensuring collateral ratio compliance\n\n📊 **Step 2/3**: Calculating your credit score privately...\n   → Using MPC to analyze your on-chain history\n   → No personal data exposed - fully privacy-preserving\n\n⛓️ **Step 3/3**: Preparing Solana transaction...\n   → Building smart contract interaction\n   → Setting up escrow for collateral\n\nThis will take just a moment... ⏳`,
          user_id: userId,
          intent: 'credit',
        };
      }
      
      // Only amount provided
      context.step = 'credit_collateral';
      conversationContexts.set(userId, context);
      return {
        response: `✅ Got it! **${amounts[0]} USDC** - that's a great starting point!\n\nNow, what would you like to use as collateral? Some popular options:\n\n🔵 **SOL** - Very liquid, typically 70-80% LTV\n🔵 **ETH** - Strong asset, around 75-85% LTV\n🔵 **BTC** - Highest LTV, up to 90%\n🟡 **USDC/USDT** - Stable, lower risk\n\n**Which asset do you want to lock as collateral?**\n\n*(Just type the token symbol - e.g., SOL, ETH, BTC)*`,
        user_id: userId,
        intent: 'credit',
      };
    }
    
    // Step 3: User provided collateral after amount
    if (context.step === 'credit_collateral' && context.amount && (tokens.length > 0 || textLower.match(/\b(sol|eth|btc|usdc|usdt)\b/))) {
      const collateralToken = tokens[0] || textLower.match(/\b(sol|eth|btc|usdc|usdt)\b/)?.[0].toUpperCase() || 'SOL';
      context.collateral = collateralToken;
      context.step = 'processing';
      conversationContexts.set(userId, context);
      
      return {
        response: `✅ Excellent choice! **${collateralToken}** as collateral works great.\n\n**Your Loan Details:**\n💰 Amount: ${context.amount} USDC\n🔒 Collateral: ${collateralToken}\n\n🔍 **Now processing your request...**\n\nI'm checking:\n1️⃣ Policy compliance (amount within limits, collateral ratio OK)\n2️⃣ Credit score via private MPC computation\n3️⃣ Current market conditions for best rates\n\nThis usually takes 10-30 seconds. I'll get back to you with the terms shortly! ⏳\n\n*While we wait, did you know this loan uses zero-knowledge proofs to keep your portfolio private? Pretty cool, right?*`,
        user_id: userId,
        intent: 'credit',
      };
    }
    
    // Step 4: Processing complete (simulated)
    if (context.step === 'processing' && context.amount && context.collateral) {
      context.step = 'completed';
      const rate = (3.5 + Math.random() * 2).toFixed(2);
      conversationContexts.set(userId, context);
      
      return {
        response: `🎉 **Great news! Your loan request has been processed!**\n\n**Approved Terms:**\n✅ **Amount**: ${context.amount} USDC\n✅ **Collateral**: ${context.collateral}\n✅ **Interest Rate**: ${rate}% APR\n✅ **Loan-to-Value**: 75%\n✅ **Collateral Required**: ${(context.amount / 0.75).toFixed(2)} ${context.collateral} equivalent\n\n📝 **Next Steps:**\n1. Review and approve the loan terms\n2. Lock your ${context.collateral} collateral in the smart contract\n3. Receive ${context.amount} USDC in your wallet\n\nWould you like to proceed with this loan? Just say "yes" or "approve" to continue! 🚀`,
        user_id: userId,
        intent: 'credit',
      };
    }
  }
  
  // ===== RWA FLOW (Enhanced) =====
  if (textLower.includes('rwa') || textLower.includes('tokenize') || textLower.includes('property') || textLower.includes('asset') || context.intent === 'rwa') {
    if (context.intent !== 'rwa') {
      context.intent = 'rwa';
      context.step = 'rwa_initial';
      conversationContexts.set(userId, context);
      return {
        response: `🏢 **Real-World Asset Tokenization** - This is exciting!\n\nI can help you tokenize physical assets like:\n🏠 Real Estate\n🏭 Commercial Properties\n🚗 High-value vehicles\n💎 Art or collectibles\n\n**The Process:**\n1️⃣ We verify the asset and its value\n2️⃣ Create an SPL token on Solana representing ownership\n3️⃣ Set up compliance rules (MeTTa-based policies)\n4️⃣ Your asset becomes tradeable as a token!\n\n**What type of asset are you looking to tokenize?**\n\n*(e.g., "a property", "my house", "commercial building")*`,
        user_id: userId,
        intent: 'rwa',
      };
    }
    
    if (context.step === 'rwa_initial' && amounts.length > 0) {
      context.amount = amounts[0];
      context.step = 'rwa_location';
      conversationContexts.set(userId, context);
      return {
        response: `💰 **Value: $${amounts[0].toLocaleString()}** - That's a substantial asset!\n\nNow I need a few more details:\n\n📍 **Location**: Where is this property located?\n   *(City, State/Country - for compliance checks)*\n\n🏗️ **Type**: What kind of property is it?\n   *(Residential, Commercial, Land, etc.)*\n\n**Let's start with the location** - where is your property?`,
        user_id: userId,
        intent: 'rwa',
      };
    }
  }
  
  // ===== TRADE FLOW (Enhanced) =====
  if (textLower.includes('trade') || textLower.includes('swap') || textLower.includes('exchange') || context.intent === 'trade') {
    if (context.intent !== 'trade') {
      context.intent = 'trade';
      context.step = 'trade_initial';
      conversationContexts.set(userId, context);
      return {
        response: `🌑 **Private Dark Pool Trading** - Trade large amounts without moving markets!\n\n**Why Dark Pools?**\n🔒 **Privacy**: Your orders aren't visible until matched\n📊 **No Slippage**: Large orders don't affect price\n⚡ **Fast Execution**: Direct peer-to-peer matching\n💰 **Better Prices**: No front-running or MEV bots\n\n**How it works:**\n1. You submit your order (encrypted)\n2. Our system matches it privately\n3. Execute the swap on Solana\n4. Receive your tokens - done!\n\n**What would you like to trade?**\n\n*Example: "I want to sell 1000 SOL for USDC"*`,
        user_id: userId,
        intent: 'trade',
      };
    }
  }
  
  // ===== AUTOMATION FLOW (Enhanced) =====
  if (textLower.includes('automat') || textLower.includes('optimize') || textLower.includes('manage') || context.intent === 'automation') {
    if (context.intent !== 'automation') {
      context.intent = 'automation';
      context.step = 'auto_initial';
      conversationContexts.set(userId, context);
      return {
        response: `🤖 **Automated Portfolio Optimization** - Set it and forget it!\n\nI'll continuously monitor your portfolio and:\n📈 **Rebalance** for optimal yield\n🎯 **Adjust allocations** based on market conditions\n⚡ **Execute trades** automatically when opportunities arise\n📊 **Track performance** and adjust strategy\n\n**Available Strategies:**\n💰 **Yield Farming** - Maximize returns from DeFi protocols\n⚖️ **Balanced** - Moderate risk, steady growth\n🚀 **Aggressive** - Higher risk, higher potential returns\n🛡️ **Conservative** - Capital preservation focus\n\n**What's your current portfolio value?** *(roughly)*`,
        user_id: userId,
        intent: 'automation',
      };
    }
  }
  
  // ===== GREETINGS & HELP =====
  if (textLower.includes('help') || textLower.includes('what') || textLower.includes('how') || textLower.includes('capabilities')) {
    return {
      response: `🦸 **I'm CypherGuy - Your Personal DeFi Assistant!**\n\nI use AI agents to help you with complex DeFi operations:\n\n💳 **Private DeFi Credit**\n   → Borrow USDC privately using crypto as collateral\n   → Credit scoring with MPC (no data leaks)\n   → Fast, secure, blockchain-native\n\n🏢 **RWA Tokenization**\n   → Turn real-world assets into Solana tokens\n   → Full compliance automation\n   → Fractional ownership enabled\n\n🌑 **Dark Pool Trading**\n   → Trade large amounts privately\n   → No slippage, no front-running\n   → Better prices for big orders\n\n🤖 **Portfolio Automation**\n   → Auto-rebalance for optimal yields\n   → 24/7 market monitoring\n   → Strategy-based trading\n\n**What would you like to explore?** Just tell me what interests you! 🚀`,
      user_id: userId,
    };
  }
  
  if (textLower.includes('hi') || textLower.includes('hello') || textLower.includes('hey')) {
    return {
      response: `👋 Hey there! I'm **CypherGuy**, your AI-powered DeFi assistant.\n\nI'm here to help you navigate the complex world of decentralized finance with ease. Whether you're looking to:\n\n💳 Get a loan\n🏢 Tokenize assets\n🌑 Trade privately\n🤖 Optimize your portfolio\n\n...I've got you covered!\n\n**What can I help you with today?** 😊`,
      user_id: userId,
    };
  }
  
  // ===== DEFAULT RESPONSE (Enhanced) =====
  const suggestions = [
    '💳 "I want to borrow 1000 USDC"',
    '🏢 "I want to tokenize my property"',
    '🌑 "I want to trade privately"',
    '🤖 "I want to optimize my portfolio"',
  ];
  
  return {
    response: `I'm here to help with all things DeFi! 🚀\n\n**Here are some things I can do:**\n\n${suggestions.join('\n')}\n\n**Or ask me anything** - I can help explain how these features work, answer questions about DeFi, or guide you through any process.\n\nWhat would you like to do?`,
    user_id: userId,
  };
}

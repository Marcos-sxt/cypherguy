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
  sellToken?: string;
  buyToken?: string;
  portfolioValue?: number;
  strategy?: string;
  location?: string;
  propertyType?: string;
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
  
  const textLower = message.toLowerCase().trim();
  
  // Get or create conversation context
  let context = conversationContexts.get(userId) || {
    intent: undefined,
    amount: undefined,
    collateral: undefined,
    step: 'initial',
    messages: []
  };
  
  // Extract numbers and tokens (better parsing)
  const numbers = message.match(/\d+/g);
  const amounts = numbers ? numbers.map(n => parseInt(n)).filter(n => n > 0) : [];
  
  // Better token detection (including in phrases like "100 USDC")
  const tokens: string[] = [];
  const tokenPatterns = [
    /\b(usdc|sol|eth|usdt|btc)\b/i,
    /(usdc|sol|eth|usdt|btc)/i
  ];
  
  tokenPatterns.forEach(pattern => {
    const matches = message.match(pattern);
    if (matches) {
      matches.forEach(m => {
        const token = m.toUpperCase();
        if (!tokens.includes(token)) tokens.push(token);
      });
    }
  });
  
  // Normalize text for intent detection
  const normalizedText = textLower
    .replace('do borrow', 'borrow')
    .replace('to borrow', 'borrow')
    .replace('wants to', 'want')
    .replace('want to', 'want');
  
  // Update context based on current message
  context.messages.push(message);
  
  // ===== CREDIT FLOW (Fixed and Enhanced) =====
  const isCreditIntent = normalizedText.includes('credit') || 
                         normalizedText.includes('loan') || 
                         normalizedText.includes('borrow') ||
                         context.intent === 'credit';
  
  if (isCreditIntent) {
    context.intent = 'credit';
    
    // Step 1: Initial interest in credit (no amount/collateral yet)
    if ((context.step === 'initial' || !context.step) && !context.amount) {
      // Check if user provided amount in initial message
      if (amounts.length > 0) {
        context.amount = amounts[0];
        if (tokens.length > 0) {
          // Both provided at once
          context.collateral = tokens[0];
          context.step = 'processing';
          conversationContexts.set(userId, context);
          return {
            response: `✅ Perfect! I've got your request:\n\n💰 Amount: ${amounts[0]} USDC\n🔒 Collateral: ${tokens[0]}\n\nNow let me work my magic! 🔮\n\n📋 Step 1/3: Checking policy rules...\n   → Validating amount limits (min: $100, max: $100k)\n   → Ensuring collateral ratio compliance\n\n📊 Step 2/3: Calculating your credit score privately...\n   → Using MPC to analyze your on-chain history\n   → No personal data exposed - fully privacy-preserving\n\n⛓️ Step 3/3: Preparing Solana transaction...\n   → Building smart contract interaction\n   → Setting up escrow for collateral\n\nThis will take just a moment... ⏳`,
            user_id: userId,
            intent: 'credit',
          };
        } else {
          // Only amount provided
          context.step = 'credit_collateral';
          conversationContexts.set(userId, context);
          return {
            response: `✅ Got it! ${amounts[0]} USDC - that's a great starting point!\n\nNow, what would you like to use as collateral? Some popular options:\n\n🔵 SOL - Very liquid, typically 70-80% LTV\n🔵 ETH - Strong asset, around 75-85% LTV\n🔵 BTC - Highest LTV, up to 90%\n🟡 USDC/USDT - Stable, lower risk\n\nWhich asset do you want to lock as collateral?\n\n(Just type the token symbol - e.g., SOL, ETH, BTC)`,
            user_id: userId,
            intent: 'credit',
          };
        }
      }
      
      // No amount yet, ask for it
      context.step = 'credit_amount';
      conversationContexts.set(userId, context);
      return {
        response: `💳 Great! I can help you get a private DeFi loan with some really cool benefits:\n\n✨ Privacy-First: Your full portfolio stays private - we only need collateral\n🔒 Secure: Uses Multi-Party Computation (MPC) for credit scoring\n⚡ Fast: No traditional banks, just smart contracts\n💰 Flexible: Borrow in USDC against your crypto assets\n\nTo get started, I'll need:\n1️⃣ The amount you want to borrow (in USDC)\n2️⃣ What you'd like to use as collateral (SOL, ETH, BTC, etc.)\n\nHow much USDC would you like to borrow?`,
        user_id: userId,
        intent: 'credit',
      };
    }
    
    // Step 2: We're in credit flow, user provided amount
    if (context.step === 'credit_amount' && amounts.length > 0 && !context.amount) {
      context.amount = amounts[0];
      
      if (tokens.length > 0) {
        // User provided both
        context.collateral = tokens[0];
        context.step = 'processing';
        conversationContexts.set(userId, context);
        return {
          response: `✅ Perfect! I've got your request:\n\n💰 Amount: ${amounts[0]} USDC\n🔒 Collateral: ${tokens[0]}\n\nNow let me work my magic! 🔮\n\n📋 Step 1/3: Checking policy rules...\n   → Validating amount limits (min: $100, max: $100k)\n   → Ensuring collateral ratio compliance\n\n📊 Step 2/3: Calculating your credit score privately...\n   → Using MPC to analyze your on-chain history\n   → No personal data exposed - fully privacy-preserving\n\n⛓️ Step 3/3: Preparing Solana transaction...\n   → Building smart contract interaction\n   → Setting up escrow for collateral\n\nThis will take just a moment... ⏳`,
          user_id: userId,
          intent: 'credit',
        };
      }
      
      // Only amount
      context.step = 'credit_collateral';
      conversationContexts.set(userId, context);
      return {
        response: `✅ Got it! ${amounts[0]} USDC - that's a great starting point!\n\nNow, what would you like to use as collateral? Some popular options:\n\n🔵 SOL - Very liquid, typically 70-80% LTV\n🔵 ETH - Strong asset, around 75-85% LTV\n🔵 BTC - Highest LTV, up to 90%\n🟡 USDC/USDT - Stable, lower risk\n\nWhich asset do you want to lock as collateral?\n\n(Just type the token symbol - e.g., SOL, ETH, BTC)`,
        user_id: userId,
        intent: 'credit',
      };
    }
    
    // Step 3: Waiting for collateral, user provided it
    if (context.step === 'credit_collateral' && context.amount && !context.collateral) {
      // Check if user provided token
      if (tokens.length > 0 || textLower.match(/\b(sol|eth|btc|usdc|usdt)\b/)) {
        const collateralToken = tokens[0] || textLower.match(/\b(sol|eth|btc|usdc|usdt)\b/)?.[0].toUpperCase() || 'SOL';
        context.collateral = collateralToken;
        context.step = 'processing';
        conversationContexts.set(userId, context);
        
        return {
          response: `✅ Excellent choice! ${collateralToken} as collateral works great.\n\nYour Loan Details:\n💰 Amount: ${context.amount} USDC\n🔒 Collateral: ${collateralToken}\n\n🔍 Now processing your request...\n\nI'm checking:\n1️⃣ Policy compliance (amount within limits, collateral ratio OK)\n2️⃣ Credit score via private MPC computation\n3️⃣ Current market conditions for best rates\n\nThis usually takes 10-30 seconds. I'll get back to you with the terms shortly! ⏳\n\nWhile we wait, did you know this loan uses zero-knowledge proofs to keep your portfolio private? Pretty cool, right?`,
          user_id: userId,
          intent: 'credit',
        };
      }
      
      // Still in collateral step, remind
      conversationContexts.set(userId, context);
      return {
        response: `I need to know what you want to use as collateral. Some options:\n\n🔵 SOL - Very liquid, typically 70-80% LTV\n🔵 ETH - Strong asset, around 75-85% LTV\n🔵 BTC - Highest LTV, up to 90%\n\nWhich one would you like? (Just type: SOL, ETH, or BTC)`,
        user_id: userId,
        intent: 'credit',
      };
    }
    
    // Step 4: Processing or amount provided, wait or confirm
    if (context.step === 'processing' && context.amount && context.collateral) {
      // Show results after processing
      context.step = 'completed';
      const rate = (3.5 + Math.random() * 2).toFixed(2);
      conversationContexts.set(userId, context);
      
      return {
        response: `🎉 Great news! Your loan request has been processed!\n\nApproved Terms:\n✅ Amount: ${context.amount} USDC\n✅ Collateral: ${context.collateral}\n✅ Interest Rate: ${rate}% APR\n✅ Loan-to-Value: 75%\n✅ Collateral Required: ${(context.amount / 0.75).toFixed(2)} ${context.collateral} equivalent\n\n📝 Next Steps:\n1. Review and approve the loan terms\n2. Lock your ${context.collateral} collateral in the smart contract\n3. Receive ${context.amount} USDC in your wallet\n\nWould you like to proceed with this loan? Just say "yes" or "approve" to continue! 🚀`,
        user_id: userId,
        intent: 'credit',
      };
    }
  }
  
  // ===== RWA FLOW (Fixed) =====
  const isRWAIntent = textLower.includes('rwa') || 
                      textLower.includes('tokenize') || 
                      textLower.includes('property') || 
                      textLower.includes('asset') ||
                      context.intent === 'rwa';
  
  if (isRWAIntent) {
    context.intent = 'rwa';
    
    // Step 1: Initial or reset
    if (!context.step || context.step === 'initial' || context.step === 'rwa_initial') {
      // Check if user already said property type
      const propertyTypes = ['house', 'property', 'building', 'commercial', 'residential', 'land', 'apartment', 'condo'];
      if (propertyTypes.some(type => textLower.includes(type))) {
        context.propertyType = textLower.includes('commercial') ? 'Commercial' : 
                               textLower.includes('residential') ? 'Residential' : 
                               textLower.includes('land') ? 'Land' : 'Residential';
        context.step = 'rwa_value';
        conversationContexts.set(userId, context);
        return {
          response: `✅ ${context.propertyType} property - got it!\n\nNow I need to know the estimated value of your property. This helps us:\n- Set the token supply\n- Determine compliance requirements\n- Calculate token price\n\nWhat's the estimated value of your property?\n\n(Just give me a number in USD, e.g., "500000" or "1.5 million")`,
          user_id: userId,
          intent: 'rwa',
        };
      }
      
      context.step = 'rwa_type';
      conversationContexts.set(userId, context);
      return {
        response: `🏢 Real-World Asset Tokenization - This is exciting!\n\nI can help you tokenize physical assets like:\n🏠 Real Estate\n🏭 Commercial Properties\n🚗 High-value vehicles\n💎 Art or collectibles\n\nThe Process:\n1️⃣ We verify the asset and its value\n2️⃣ Create an SPL token on Solana representing ownership\n3️⃣ Set up compliance rules (MeTTa-based policies)\n4️⃣ Your asset becomes tradeable as a token!\n\nWhat type of asset are you looking to tokenize?\n\n(e.g., "a property", "my house", "commercial building")`,
        user_id: userId,
        intent: 'rwa',
      };
    }
    
    // Step 2: Get property type
    if (context.step === 'rwa_type' && !context.propertyType) {
      const propertyTypes = ['house', 'property', 'building', 'commercial', 'residential', 'land', 'apartment', 'condo'];
      if (propertyTypes.some(type => textLower.includes(type))) {
        context.propertyType = textLower.includes('commercial') ? 'Commercial' : 
                               textLower.includes('residential') ? 'Residential' : 
                               textLower.includes('land') ? 'Land' : 'Residential';
        context.step = 'rwa_value';
        conversationContexts.set(userId, context);
        return {
          response: `✅ ${context.propertyType} property - got it!\n\nNow I need to know the estimated value of your property. This helps us:\n- Set the token supply\n- Determine compliance requirements\n- Calculate token price\n\nWhat's the estimated value of your property?\n\n(Just give me a number in USD, e.g., "500000" or "1.5 million")`,
          user_id: userId,
          intent: 'rwa',
        };
      }
      
      // Still waiting for property type
      conversationContexts.set(userId, context);
      return {
        response: `What type of property are you looking to tokenize?\n\nOptions:\n🏠 Residential property\n🏭 Commercial building\n🌳 Land\n🏢 Apartment/Condo\n\nJust tell me what type of property you have!`,
        user_id: userId,
        intent: 'rwa',
      };
    }
    
    // Step 3: Get property value
    if (context.step === 'rwa_value' && amounts.length > 0 && !context.amount) {
      context.amount = amounts[0];
      context.step = 'rwa_location';
      conversationContexts.set(userId, context);
      return {
        response: `💰 Value: $${amounts[0].toLocaleString()} - That's a substantial asset!\n\nGreat! Now I need the location for compliance checks. Different jurisdictions have different regulations, so this is important.\n\nWhere is this property located?\n\n(Format: City, State/Country - e.g., "New York, USA" or "São Paulo, Brazil")`,
        user_id: userId,
        intent: 'rwa',
      };
    }
    
    // Step 4: Get location
    if (context.step === 'rwa_location' && !context.location && textLower.length > 3 && !amounts.length) {
      context.location = message;
      context.step = 'rwa_processing';
      conversationContexts.set(userId, context);
      return {
        response: `✅ Location: ${message} - noted!\n\nPerfect! I have everything I need:\n\n📋 Asset Details:\n🏠 Type: ${context.propertyType || 'Property'}\n💰 Value: $${context.amount?.toLocaleString() || 'N/A'}\n📍 Location: ${message}\n\n🔍 Now processing your tokenization request...\n\nI'm checking:\n1️⃣ Compliance rules for ${message}\n2️⃣ Regulatory requirements\n3️⃣ Property verification process\n4️⃣ Token economics setup\n\nThis usually takes 1-2 minutes. I'll come back with the tokenization plan shortly! ⏳`,
        user_id: userId,
        intent: 'rwa',
      };
    }
    
    // Step 5: Processing complete
    if (context.step === 'rwa_processing' && context.amount && context.location) {
      context.step = 'rwa_completed';
      const tokenId = `RWA_${userId.slice(0, 6)}_${Date.now().toString().slice(-6)}`;
      conversationContexts.set(userId, context);
      
      return {
        response: `🎉 Your property is ready to be tokenized!\n\nTokenization Plan:\n✅ Token ID: ${tokenId}\n✅ Asset Type: ${context.propertyType || 'Property'}\n✅ Total Value: $${context.amount?.toLocaleString()}\n✅ Token Supply: 1,000,000 tokens\n✅ Token Price: $${((context.amount || 0) / 1000000).toFixed(4)} per token\n✅ Blockchain: Solana (SPL token)\n✅ Compliance: Verified for ${context.location}\n\n📝 Next Steps:\n1. Review and sign the tokenization agreement\n2. Verify property ownership documents\n3. Deploy smart contract on Solana\n4. Your property becomes tradeable!\n\nWould you like to proceed with tokenization? Say "yes" to continue! 🚀`,
        user_id: userId,
        intent: 'rwa',
      };
    }
    
    // Fallback: if in RWA flow but step unclear, continue flow
    if (context.intent === 'rwa') {
      conversationContexts.set(userId, context);
      // Try to continue based on what's missing
      if (!context.propertyType) {
        return {
          response: `What type of property are you looking to tokenize?\n\n(e.g., "a property", "my house", "commercial building")`,
          user_id: userId,
          intent: 'rwa',
        };
      } else if (!context.amount) {
        return {
          response: `What's the estimated value of your property?\n\n(Just give me a number in USD)`,
          user_id: userId,
          intent: 'rwa',
        };
      } else if (!context.location) {
        return {
          response: `Where is this property located?\n\n(Format: City, State/Country)`,
          user_id: userId,
          intent: 'rwa',
        };
      }
    }
  }
  
  // ===== TRADE FLOW (Fixed) =====
  const isTradeIntent = textLower.includes('trade') || 
                        textLower.includes('swap') || 
                        textLower.includes('exchange') ||
                        context.intent === 'trade';
  
  if (isTradeIntent) {
    context.intent = 'trade';
    
    // Step 1: Initial
    if (!context.step || context.step === 'initial' || context.step === 'trade_initial') {
      context.step = 'trade_details';
      conversationContexts.set(userId, context);
      return {
        response: `🌑 Private Dark Pool Trading - Trade large amounts without moving markets!\n\nWhy Dark Pools?\n🔒 Privacy: Your orders aren't visible until matched\n📊 No Slippage: Large orders don't affect price\n⚡ Fast Execution: Direct peer-to-peer matching\n💰 Better Prices: No front-running or MEV bots\n\nHow it works:\n1. You submit your order (encrypted)\n2. Our system matches it privately\n3. Execute the swap on Solana\n4. Receive your tokens - done!\n\nWhat would you like to trade?\n\nExample: "I want to sell 1000 SOL for USDC" or just tell me what you want to sell and buy!`,
        user_id: userId,
        intent: 'trade',
      };
    }
    
    // Step 2: Parse trade details
    if (context.step === 'trade_details') {
      // Try to extract: amount, sell token, buy token
      if (amounts.length > 0 && !context.amount) {
        context.amount = amounts[0];
      }
      
      // Look for "sell" or "for" patterns
      const sellMatch = textLower.match(/(?:sell|swap|trade)\s+(\d+)?\s*(\w+)/i);
      const forMatch = textLower.match(/for\s+(\w+)/i);
      
      if (sellMatch) {
        const amountFromText = sellMatch[1] ? parseInt(sellMatch[1]) : (amounts[0] || undefined);
        if (amountFromText && !context.amount) context.amount = amountFromText;
        if (!context.sellToken) context.sellToken = sellMatch[2]?.toUpperCase() || tokens[0] || 'SOL';
      } else if (amounts.length > 0 && tokens.length > 0 && !context.sellToken) {
        context.sellToken = tokens[0];
      }
      
      if (forMatch) {
        context.buyToken = forMatch[1]?.toUpperCase() || 'USDC';
      } else if (tokens.length > 1 && !context.buyToken) {
        context.buyToken = tokens[1];
      } else if (tokens.length === 1 && context.sellToken && !context.buyToken) {
        context.buyToken = 'USDC';
      }
      
      // Check if we have enough info
      if (context.amount && context.sellToken && context.buyToken) {
        context.step = 'trade_processing';
        conversationContexts.set(userId, context);
        return {
          response: `✅ Perfect! I've got your trade order:\n\n💰 Amount: ${context.amount} ${context.sellToken}\n🔄 Trading for: ${context.buyToken}\n\n🔍 Now finding the best match in our dark pool...\n\nI'm looking for:\n1️⃣ Counterparties with matching orders\n2️⃣ Best price available\n3️⃣ Private order book\n\nThis usually takes 5-15 seconds. Large orders get priority matching! ⏳`,
          user_id: userId,
          intent: 'trade',
        };
      } else {
        // Missing info
        let missing = [];
        if (!context.amount) missing.push('amount');
        if (!context.sellToken) missing.push('token to sell');
        if (!context.buyToken) missing.push('token to buy');
        
        conversationContexts.set(userId, context);
        return {
          response: `I need a bit more info:\n\n${missing.includes('amount') ? '💵 How much do you want to trade?\n' : ''}${missing.includes('token to sell') ? '🔄 What token do you want to sell? (e.g., SOL, ETH, BTC)\n' : ''}${missing.includes('token to buy') ? '💰 What token do you want to receive? (e.g., USDC, USDT)\n' : ''}\n\nOr just say something like: "I want to sell 1000 SOL for USDC"`,
          user_id: userId,
          intent: 'trade',
        };
      }
    }
    
    // Step 3: Processing complete
    if (context.step === 'trade_processing' && context.amount && context.sellToken && context.buyToken) {
      const priceRatio = context.sellToken === 'SOL' ? 150 : context.sellToken === 'ETH' ? 3000 : 65000;
      const receiveAmount = (context.amount * priceRatio).toFixed(2);
      context.step = 'trade_completed';
      conversationContexts.set(userId, context);
      
      return {
        response: `🎉 Match found! Your order is ready:\n\n✅ Sell: ${context.amount} ${context.sellToken}\n✅ Buy: ~${receiveAmount} ${context.buyToken}\n✅ Price: 1 ${context.sellToken} = ${(priceRatio).toLocaleString()} ${context.buyToken}\n✅ Slippage: <0.1% (excellent!)\n✅ Execution: Private dark pool\n\n📝 Next Steps:\n1. Review the trade details above\n2. Confirm the order\n3. Execute on Solana blockchain\n4. Receive ${context.buyToken} in your wallet\n\nReady to execute? Say "yes" or "confirm" to proceed! 🚀`,
        user_id: userId,
        intent: 'trade',
      };
    }
  }
  
  // ===== AUTOMATION FLOW (Fixed) =====
  const isAutomationIntent = textLower.includes('automat') || 
                             textLower.includes('optimize') || 
                             textLower.includes('manage') ||
                             context.intent === 'automation';
  
  if (isAutomationIntent) {
    context.intent = 'automation';
    
    // Step 1: Initial
    if (!context.step || context.step === 'initial' || context.step === 'auto_initial') {
      context.step = 'auto_portfolio';
      conversationContexts.set(userId, context);
      return {
        response: `🤖 Automated Portfolio Optimization - Set it and forget it!\n\nI'll continuously monitor your portfolio and:\n📈 Rebalance for optimal yield\n🎯 Adjust allocations based on market conditions\n⚡ Execute trades automatically when opportunities arise\n📊 Track performance and adjust strategy\n\nAvailable Strategies:\n💰 Yield Farming - Maximize returns from DeFi protocols\n⚖️ Balanced - Moderate risk, steady growth\n🚀 Aggressive - Higher risk, higher potential returns\n🛡️ Conservative - Capital preservation focus\n\nWhat's your current portfolio value?\n\n(Just give me a rough number in USD)`,
        user_id: userId,
        intent: 'automation',
      };
    }
    
    // Step 2: Get portfolio value
    if (context.step === 'auto_portfolio' && amounts.length > 0 && !context.portfolioValue) {
      context.portfolioValue = amounts[0];
      context.step = 'auto_strategy';
      conversationContexts.set(userId, context);
      return {
        response: `✅ Portfolio Value: $${amounts[0].toLocaleString()} - Nice!\n\nNow, which strategy fits your risk appetite?\n\n💰 Yield Farming\n   → Best for: Maximizing returns\n   → Risk: Medium-High\n   → Expected APY: 15-25%\n   → Rebalances: Daily\n\n⚖️ Balanced\n   → Best for: Steady growth\n   → Risk: Medium\n   → Expected APY: 8-15%\n   → Rebalances: Weekly\n\n🚀 Aggressive\n   → Best for: High growth potential\n   → Risk: High\n   → Expected APY: 20-40%\n   → Rebalances: Hourly\n\n🛡️ Conservative\n   → Best for: Capital preservation\n   → Risk: Low\n   → Expected APY: 5-10%\n   → Rebalances: Weekly\n\nWhich strategy would you like? (Just say the name)`,
        user_id: userId,
        intent: 'automation',
      };
    }
    
    // Step 3: Get strategy
    if (context.step === 'auto_strategy' && !context.strategy) {
      const strategies = ['yield', 'balanced', 'aggressive', 'conservative'];
      const foundStrategy = strategies.find(s => textLower.includes(s));
      
      if (foundStrategy) {
        context.strategy = foundStrategy.charAt(0).toUpperCase() + foundStrategy.slice(1);
        context.step = 'auto_processing';
        conversationContexts.set(userId, context);
        return {
          response: `✅ ${context.strategy} Strategy - Excellent choice!\n\nPerfect! I'm setting up your automated portfolio optimization:\n\n📊 Portfolio Details:\n💰 Value: $${context.portfolioValue?.toLocaleString()}\n🎯 Strategy: ${context.strategy}\n\n🔍 Now calculating optimal allocation...\n\nI'm analyzing:\n1️⃣ Current market conditions\n2️⃣ Best yield opportunities\n3️⃣ Risk diversification\n4️⃣ Optimal token allocations\n\nThis will take about 30 seconds. I'll show you the proposed allocation shortly! ⏳`,
          user_id: userId,
          intent: 'automation',
        };
      }
      
      // Still waiting for strategy
      conversationContexts.set(userId, context);
      return {
        response: `Which strategy would you like?\n\n💰 Yield Farming\n⚖️ Balanced\n🚀 Aggressive\n🛡️ Conservative\n\nJust say the name of the strategy!`,
        user_id: userId,
        intent: 'automation',
      };
    }
    
    // Step 4: Processing complete
    if (context.step === 'auto_processing' && context.portfolioValue && context.strategy) {
      context.step = 'auto_completed';
      conversationContexts.set(userId, context);
      
      const allocations = {
        'Yield': { SOL: 30, ETH: 25, USDC: 20, BTC: 15, Others: 10 },
        'Balanced': { SOL: 25, ETH: 20, USDC: 30, BTC: 15, Others: 10 },
        'Aggressive': { SOL: 40, ETH: 30, BTC: 20, Others: 10 },
        'Conservative': { SOL: 15, ETH: 10, USDC: 50, BTC: 15, Others: 10 },
      };
      
      const allocation = allocations[context.strategy as keyof typeof allocations] || allocations['Balanced'];
      
      return {
        response: `🎉 Your optimized portfolio is ready!\n\nProposed Allocation (${context.strategy} Strategy):\n\n${Object.entries(allocation).map(([token, pct]) => `📊 ${token}: ${pct}%`).join('\n')}\n\nExpected Performance:\n✅ Estimated APY: ${context.strategy === 'Aggressive' ? '20-35%' : context.strategy === 'Conservative' ? '5-10%' : context.strategy === 'Yield' ? '15-25%' : '8-15%'}\n✅ Rebalance Frequency: ${context.strategy === 'Aggressive' ? 'Hourly' : 'Weekly'}\n✅ Auto-trading: Enabled\n✅ Risk Management: Active\n\n📝 Next Steps:\n1. Review the allocation above\n2. Approve the strategy\n3. I'll start monitoring and rebalancing automatically\n\nReady to start? Say "yes" to activate automation! 🚀`,
        user_id: userId,
        intent: 'automation',
      };
    }
    
    // Fallback: continue automation flow
    if (context.intent === 'automation') {
      conversationContexts.set(userId, context);
      if (!context.portfolioValue) {
        return {
          response: `What's your current portfolio value?\n\n(Just give me a rough number in USD)`,
          user_id: userId,
          intent: 'automation',
        };
      } else if (!context.strategy) {
        return {
          response: `Which strategy would you like? (Yield Farming, Balanced, Aggressive, or Conservative)`,
          user_id: userId,
          intent: 'automation',
        };
      }
    }
  }
  
  // ===== GREETINGS & HELP =====
  if (textLower.includes('help') || textLower.includes('what') || textLower.includes('how') || textLower.includes('capabilities')) {
    // Reset context on help
    context.intent = undefined;
    context.step = 'initial';
    conversationContexts.set(userId, context);
    return {
      response: `🦸 I'm CypherGuy - Your Personal DeFi Assistant!\n\nI use AI agents to help you with complex DeFi operations:\n\n💳 Private DeFi Credit\n   → Borrow USDC privately using crypto as collateral\n   → Credit scoring with MPC (no data leaks)\n   → Fast, secure, blockchain-native\n\n🏢 RWA Tokenization\n   → Turn real-world assets into Solana tokens\n   → Full compliance automation\n   → Fractional ownership enabled\n\n🌑 Dark Pool Trading\n   → Trade large amounts privately\n   → No slippage, no front-running\n   → Better prices for big orders\n\n🤖 Portfolio Automation\n   → Auto-rebalance for optimal yields\n   → 24/7 market monitoring\n   → Strategy-based trading\n\nWhat would you like to explore? Just tell me what interests you! 🚀`,
      user_id: userId,
    };
  }
  
  if (textLower.includes('hi') || textLower.includes('hello') || textLower.includes('hey')) {
    return {
      response: `👋 Hey there! I'm CypherGuy, your AI-powered DeFi assistant.\n\nI'm here to help you navigate the complex world of decentralized finance with ease. Whether you're looking to:\n\n💳 Get a loan\n🏢 Tokenize assets\n🌑 Trade privately\n🤖 Optimize your portfolio\n\n...I've got you covered!\n\nWhat can I help you with today? 😊`,
      user_id: userId,
    };
  }
  
  // ===== DEFAULT RESPONSE (Enhanced) =====
  // Save context before returning default
  conversationContexts.set(userId, context);
  
  const suggestions = [
    '💳 "I want to borrow 1000 USDC"',
    '🏢 "I want to tokenize my property"',
    '🌑 "I want to trade privately"',
    '🤖 "I want to optimize my portfolio"',
  ];
  
  return {
    response: `I'm here to help with all things DeFi! 🚀\n\nHere are some things I can do:\n\n${suggestions.join('\n')}\n\nOr ask me anything - I can help explain how these features work, answer questions about DeFi, or guide you through any process.\n\nWhat would you like to do?`,
    user_id: userId,
  };
}

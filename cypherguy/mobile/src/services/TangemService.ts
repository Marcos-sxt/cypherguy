/**
 * Tangem Wallet Service
 * Real implementation with Tangem SDK
 * 
 * SDK: tangem-sdk-react-native (XRPL Labs)
 * Docs: https://github.com/XRPL-Labs/tangem-sdk-react-native
 */

import RNTangemSdk from 'tangem-sdk-react-native';

export interface TangemCard {
  cardId: string;
  publicKey: string;
  walletPublicKey: string;
  blockchain: string;
  status: 'active' | 'locked';
  firmwareVersion?: string;
  manufacturer?: string;
  issuer?: string;
}

export interface SignResult {
  signature: string;
  publicKey: string;
  cardId: string;
}

export interface TangemConfig {
  attestationMode?: 'offline' | 'full' | 'nomral'; // Note: typo in SDK ('nomral' not 'normal')
  defaultDerivationPaths?: string;
  useMock?: boolean; // Set to true for testing without physical card
}

export class TangemService {
  private currentCard: TangemCard | null = null;
  private sessionStarted: boolean = false;
  private useMock: boolean;

  constructor(config?: TangemConfig) {
    this.useMock = config?.useMock ?? false;

    if (!this.useMock) {
      // Initialize Tangem SDK with config
      const sdkConfig = {
        attestationMode: config?.attestationMode || 'offline',
        defaultDerivationPaths: config?.defaultDerivationPaths || "m/44'/501'/0'/0/0", // Solana path
      };

      try {
        RNTangemSdk.startSession(sdkConfig);
        this.sessionStarted = true;
        console.log('🔐 Tangem SDK session started with config:', sdkConfig);
      } catch (error) {
        console.error('❌ Failed to start Tangem SDK session:', error);
        console.warn('⚠️  Falling back to mock mode');
        this.useMock = true;
      }
    } else {
      console.log('🎭 Tangem Service initialized in MOCK mode');
    }
  }

  /**
   * Scan Tangem card via NFC
   */
  async scanCard(): Promise<TangemCard> {
    if (this.useMock) {
      return this.scanCardMock();
    }

    try {
      console.log('🔍 Scanning Tangem card via NFC...');
      
      const cardInfo = await RNTangemSdk.scanCard();

      console.log('📱 Card scanned successfully:', cardInfo);

      const card: TangemCard = {
        cardId: cardInfo.cardId || cardInfo.cardPublicKey,
        publicKey: cardInfo.cardPublicKey,
        walletPublicKey: cardInfo.wallets?.[0]?.publicKey || cardInfo.cardPublicKey,
        blockchain: 'solana',
        status: cardInfo.isAccessCodeSet ? 'locked' : 'active',
        firmwareVersion: String(cardInfo.firmwareVersion || ''),
        manufacturer: String(cardInfo.manufacturer || ''),
        issuer: String(cardInfo.issuer || ''),
      };

      this.currentCard = card;
      console.log('✅ Card info processed:', {
        cardId: card.cardId,
        blockchain: card.blockchain,
        status: card.status,
      });

      return card;
    } catch (error: any) {
      console.error('❌ Failed to scan card:', error);
      
      // Check for specific errors
      if (error.code === 'USER_CANCELLED') {
        throw new Error('Card scan was cancelled by user');
      } else if (error.code === 'NFC_DISABLED') {
        throw new Error('NFC is disabled. Please enable NFC in device settings');
      } else if (error.code === 'NFC_NOT_SUPPORTED') {
        throw new Error('This device does not support NFC');
      }

      throw new Error(`Failed to scan Tangem card: ${error.message || error}`);
    }
  }

  /**
   * Sign transaction with Tangem card
   */
  async signTransaction(
    transactionData: string,
    cardId?: string
  ): Promise<SignResult> {
    if (this.useMock) {
      return this.signTransactionMock(transactionData, cardId);
    }

    try {
      console.log('✍️ Signing transaction with Tangem card...');

      if (!this.currentCard && !cardId) {
        throw new Error('No card scanned. Please scan card first.');
      }

      const targetCardId = cardId || this.currentCard!.cardId;

      // Convert transaction data to hex if needed
      const hexData = this.toHexString(transactionData);

      // Get wallet public key
      const walletPublicKey = this.currentCard?.walletPublicKey || this.currentCard?.publicKey || '';
      if (!walletPublicKey) {
        throw new Error('Wallet public key not available. Please scan card first.');
      }

      // Sign with Tangem SDK
      const signResult = await RNTangemSdk.sign({
        cardId: targetCardId,
        hashes: [hexData],
        walletPublicKey,
      });

      console.log('✅ Transaction signed successfully');

      const result: SignResult = {
        signature: signResult.signatures?.[0] || '',
        publicKey: walletPublicKey,
        cardId: targetCardId,
      };

      return result;
    } catch (error: any) {
      console.error('❌ Failed to sign transaction:', error);

      if (error.code === 'USER_CANCELLED') {
        throw new Error('Signing was cancelled by user');
      } else if (error.code === 'PIN_REQUIRED') {
        throw new Error('PIN is required. Please set access code first');
      }

      throw new Error(`Failed to sign transaction: ${error.message || error}`);
    }
  }

  /**
   * Authenticate user with Tangem card
   */
  async authenticateUser(): Promise<{ userId: string; publicKey: string }> {
    if (this.useMock) {
      return this.authenticateUserMock();
    }

    try {
      console.log('🔐 Authenticating with Tangem card...');

      const card = await this.scanCard();

      // Generate authentication challenge
      const challenge = `cypherguy_auth_${Date.now()}`;
      const signature = await this.signTransaction(challenge, card.cardId);

      console.log('✅ Authentication successful');

      return {
        userId: card.cardId,
        publicKey: signature.publicKey,
      };
    } catch (error: any) {
      console.error('❌ Authentication failed:', error);
      throw new Error(`Authentication failed: ${error.message || error}`);
    }
  }

  /**
   * Create new wallet on Tangem card
   */
  async createWallet(cardId?: string): Promise<TangemCard> {
    if (this.useMock) {
      console.warn('⚠️  createWallet() not available in mock mode');
      return this.currentCard!;
    }

    try {
      console.log('🆕 Creating new wallet on Tangem card...');

      const targetCardId = cardId || this.currentCard?.cardId;
      if (!targetCardId) {
        throw new Error('No card scanned');
      }

      const result = await RNTangemSdk.createWallet({ cardId: targetCardId });

      console.log('✅ Wallet created successfully:', result);

      // Re-scan card to get updated info
      return await this.scanCard();
    } catch (error: any) {
      console.error('❌ Failed to create wallet:', error);
      throw new Error(`Failed to create wallet: ${error.message || error}`);
    }
  }

  /**
   * Set access code (PIN) on Tangem card
   */
  async setAccessCode(code: string, cardId?: string): Promise<void> {
    if (this.useMock) {
      console.warn('⚠️  setAccessCode() not available in mock mode');
      return;
    }

    try {
      console.log('🔒 Setting access code on Tangem card...');

      const targetCardId = cardId || this.currentCard?.cardId;
      if (!targetCardId) {
        throw new Error('No card scanned');
      }

      await RNTangemSdk.setAccessCode({
        cardId: targetCardId,
        accessCode: code,
      });

      console.log('✅ Access code set successfully');

      // Update current card status
      if (this.currentCard) {
        this.currentCard.status = 'locked';
      }
    } catch (error: any) {
      console.error('❌ Failed to set access code:', error);
      throw new Error(`Failed to set access code: ${error.message || error}`);
    }
  }

  /**
   * Get currently scanned card
   */
  getCurrentCard(): TangemCard | null {
    return this.currentCard;
  }

  /**
   * Clear current card session
   */
  clearCard(): void {
    this.currentCard = null;
    console.log('🗑️ Card session cleared');
  }

  /**
   * Check if NFC is available on device
   */
  async checkNFCAvailability(): Promise<boolean> {
    if (this.useMock) {
      return true;
    }

    try {
      // Try to scan card to check NFC
      // This will throw appropriate error if NFC is not available
      await RNTangemSdk.scanCard();
      return true;
    } catch (error: any) {
      if (error.code === 'NFC_NOT_SUPPORTED') {
        return false;
      }
      // Other errors don't mean NFC is unavailable
      return true;
    }
  }

  /**
   * Toggle mock mode (useful for testing)
   */
  setMockMode(enabled: boolean): void {
    this.useMock = enabled;
    console.log(`🎭 Mock mode ${enabled ? 'enabled' : 'disabled'}`);
  }

  // ========== HELPER METHODS ==========

  private toHexString(data: string): string {
    // If already hex, return as is
    if (/^[0-9a-fA-F]+$/.test(data)) {
      return data;
    }

    // Convert string to hex
    return Buffer.from(data, 'utf8').toString('hex');
  }

  // ========== MOCK METHODS (for testing without physical card) ==========

  private async scanCardMock(): Promise<TangemCard> {
    console.log('🎭 [MOCK] Scanning Tangem card...');
    await this.simulateDelay(1500);

    const mockCard: TangemCard = {
      cardId: `CB${Math.random().toString(36).substr(2, 9).toUpperCase()}`,
      publicKey: this.generateMockPublicKey(),
      walletPublicKey: this.generateMockPublicKey(),
      blockchain: 'solana',
      status: 'active',
      firmwareVersion: '4.52',
      manufacturer: 'TANGEM AG',
      issuer: 'TANGEM',
    };

    this.currentCard = mockCard;
    console.log('✅ [MOCK] Card scanned:', mockCard.cardId);

    return mockCard;
  }

  private async signTransactionMock(
    transactionData: string,
    cardId?: string
  ): Promise<SignResult> {
    console.log('🎭 [MOCK] Signing transaction...');
    await this.simulateDelay(1000);

    const mockSignature: SignResult = {
      signature: this.generateMockSignature(),
      publicKey: this.currentCard?.publicKey || this.generateMockPublicKey(),
      cardId: cardId || this.currentCard!.cardId,
    };

    console.log('✅ [MOCK] Transaction signed');
    return mockSignature;
  }

  private async authenticateUserMock(): Promise<{
    userId: string;
    publicKey: string;
  }> {
    console.log('🎭 [MOCK] Authenticating user...');
    const card = await this.scanCardMock();
    const signature = await this.signTransactionMock(`auth_${Date.now()}`);

    console.log('✅ [MOCK] Authentication successful');
    return {
      userId: card.cardId,
      publicKey: signature.publicKey,
    };
  }

  private async simulateDelay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  private generateMockPublicKey(): string {
    const chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
    let result = '';
    for (let i = 0; i < 44; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  }

  private generateMockSignature(): string {
    let result = '';
    for (let i = 0; i < 128; i++) {
      result += Math.floor(Math.random() * 16).toString(16);
    }
    return result;
  }
}

// Export singleton with mock mode for development
// Set useMock: false when you have a physical Tangem card
export const tangemService = new TangemService({
  attestationMode: 'offline',
  defaultDerivationPaths: "m/44'/501'/0'/0/0", // Solana derivation path
  useMock: true, // Set to false to use real Tangem card
});

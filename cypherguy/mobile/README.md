# 🔐 CypherGuy Mobile

React Native mobile application for CypherGuy - Private AI-Powered DeFi Agent with Tangem Wallet integration.

## 🚀 Features

- **💳 Tangem Wallet Integration** - Hardware wallet authentication via NFC
- **💰 Private DeFi Credit** - Request credit with private KYC verification
- **🏢 RWA Compliance** - Real World Asset compliance checking
- **🔄 Dark Pool Trading** - Private trade execution
- **🤖 DeFi Automation** - Automated portfolio strategies

## 📋 Prerequisites

- Node.js 18+
- React Native development environment
- Android Studio (for Android) or Xcode (for iOS)
- NFC-enabled device for Tangem integration

## 🛠️ Setup

### 1. Install dependencies

```bash
npm install
```

### 2. Configure environment

The app connects to the CypherGuy backend at `http://localhost:8000` by default.

For production, update the `API_BASE_URL` in `src/services/ApiService.ts`.

### 3. Run on Android

```bash
npm run android
```

### 4. Run on iOS

```bash
cd ios && pod install && cd ..
npm run ios
```

### 5. Run on Web (Expo)

```bash
npm run web
```

## 🏗️ Project Structure

```
mobile/
├── src/
│   ├── services/
│   │   ├── TangemService.ts    # Tangem Wallet integration
│   │   └── ApiService.ts       # Backend API client
│   ├── components/             # Reusable UI components
│   ├── screens/                # App screens
│   └── types/                  # TypeScript types
├── App.tsx                     # Main app component
├── package.json
└── README.md
```

## 🔑 Tangem Integration

### ✅ REAL SDK IMPLEMENTED!

The **official Tangem SDK** is now fully integrated! 🎉

Package: [`tangem-sdk-react-native`](https://github.com/XRPL-Labs/tangem-sdk-react-native)

### Two Modes Available

#### 1. Mock Mode (Default - For Development)
```typescript
// src/services/TangemService.ts
export const tangemService = new TangemService({
  useMock: true  // ← Simulated mode, no physical card needed
});
```

Perfect for:
- Development without Tangem card
- Automated testing
- Demo on devices without NFC
- CI/CD pipelines

#### 2. Real Mode (With Physical Card)
```typescript
// src/services/TangemService.ts
export const tangemService = new TangemService({
  useMock: false,  // ← Real mode with physical card
  attestationMode: 'offline',
  defaultDerivationPaths: "m/44'/501'/0'/0/0"  // Solana path
});
```

Perfect for:
- Production use
- Testing with real hardware
- Hackathon demos with card
- End-to-end validation

### Quick Start

**With Mock (No Hardware):**
```bash
npm run android  # Works on emulator
npm run ios      # Works on simulator
npm run web      # Works in browser
```

**With Real Card:**
```bash
# 1. Change useMock: false in TangemService.ts
# 2. Get a Tangem card
# 3. Enable NFC on device
npm run android  # Physical device only
npm run ios      # iPhone 7+ required
```

### Full Documentation

See [TANGEM_INTEGRATION.md](./TANGEM_INTEGRATION.md) for complete API reference, error handling, and examples.

## 📡 Backend Integration

The app connects to the CypherGuy FastAPI backend for:

1. **Credit Requests** - `POST /credit`
2. **RWA Compliance** - `POST /rwa`
3. **Trade Execution** - `POST /trade`
4. **Automation Setup** - `POST /automation`

Make sure the backend is running:

```bash
cd ../backend
python main.py
```

## 🎨 UI/UX

- **Dark Theme** - Modern dark UI optimized for mobile
- **NFC Prompts** - Clear instructions for Tangem card interactions
- **Loading States** - Visual feedback for async operations
- **Error Handling** - User-friendly error messages

## 🔐 Security

- **Hardware Wallet Auth** - Private keys never leave Tangem card
- **Secure Communication** - HTTPS for production
- **NFC Security** - Encrypted NFC channel (production)
- **Session Management** - Secure user sessions

## 📱 Supported Platforms

- ✅ **Android** - Full support (NFC required)
- ✅ **iOS** - Full support (NFC required)
- ✅ **Web** - Limited support (no NFC)

## 🐛 Troubleshooting

### NFC Not Working

- Ensure NFC is enabled in device settings
- Check that your device supports NFC
- Make sure you're using a real Tangem card

### Backend Connection Failed

- Verify backend is running (`http://localhost:8000`)
- Check network connectivity
- For Android emulator, use `10.0.2.2:8000`
- For iOS simulator, use `localhost:8000`

### Build Errors

```bash
# Clear cache and rebuild
npm start -- --reset-cache
npx react-native run-android
```

## 🏆 Hackathon Demo

To demonstrate the app:

1. Start the backend: `cd ../backend && python main.py`
2. Start the mobile app: `npm run android` or `npm run ios`
3. Click "Connect Tangem Card" (simulates card tap)
4. Try each feature (Credit, RWA, Trade, Automation)
5. Check backend logs to see agent processing

## 🔮 Future Enhancements

- [ ] Real Tangem SDK integration
- [ ] Multi-wallet support (Phantom, Solflare)
- [ ] Chat interface for natural language interactions
- [ ] Push notifications for transaction status
- [ ] Biometric authentication
- [ ] QR code scanning for Solana Pay
- [ ] Portfolio tracking dashboard
- [ ] Transaction history

## 📚 Documentation

- [Tangem Wallet Docs](https://developers.tangem.com/)
- [React Native Docs](https://reactnative.dev/)
- [Solana Web3.js](https://solana-labs.github.io/solana-web3.js/)
- [CypherGuy Backend](/backend/README.md)

## 🤝 Contributing

This is a hackathon project. For improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

---

**Built with ❤️ for Solana Hackathon 2025**

ASI Alliance • Arcium • Tangem • Solana


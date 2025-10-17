'use client';

import React, { useState, useEffect } from 'react';
import { WalletMultiButton, WalletDisconnectButton } from '@solana/wallet-adapter-react-ui';
import { useWallet } from '@solana/wallet-adapter-react';
import { TangemAuth } from '@/components/auth/TangemAuth';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { CreditCard, Wallet, Shield, Zap } from 'lucide-react';

export default function HomePage() {
  const { connected, publicKey } = useWallet();
  const [authMethod, setAuthMethod] = useState<'wallet' | 'tangem' | null>(null);
  const [tangemPublicKey, setTangemPublicKey] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false);

  // Prevent hydration mismatch
  useEffect(() => {
    setMounted(true);
  }, []);

  const handleTangemSuccess = (publicKey: string) => {
    setTangemPublicKey(publicKey);
  };

  const handleTangemError = (error: string) => {
    console.error('Tangem authentication error:', error);
  };

  const isAuthenticated = connected || tangemPublicKey;

  if (isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              🦸 Welcome to CypherGuy!
            </h1>
            <p className="text-xl text-gray-600">
              Your personal DeFi assistant is ready
            </p>
          </div>

          <div className="max-w-4xl mx-auto">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {/* Credit Card */}
              <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-2">
                    <CreditCard className="w-6 h-6 text-green-600" />
                  </div>
                  <CardTitle className="text-lg">Private Credit</CardTitle>
                  <CardDescription>
                    Get loans without revealing your portfolio
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Button className="w-full">
                    Get Loan
                  </Button>
                </CardContent>
              </Card>

              {/* RWA Tokenization */}
              <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-2">
                    <Shield className="w-6 h-6 text-blue-600" />
                  </div>
                  <CardTitle className="text-lg">RWA Compliance</CardTitle>
                  <CardDescription>
                    Tokenize real assets with compliance
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Button className="w-full">
                    Tokenize Asset
                  </Button>
                </CardContent>
              </Card>

              {/* Dark Pool Trading */}
              <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-2">
                    <Zap className="w-6 h-6 text-purple-600" />
                  </div>
                  <CardTitle className="text-lg">Dark Pool</CardTitle>
                  <CardDescription>
                    Trade large amounts privately
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Button className="w-full">
                    Start Trading
                  </Button>
                </CardContent>
              </Card>

              {/* DeFi Automation */}
              <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center mb-2">
                    <Zap className="w-6 h-6 text-orange-600" />
                  </div>
                  <CardTitle className="text-lg">Auto DeFi</CardTitle>
                  <CardDescription>
                    Automatically optimize your portfolio
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Button className="w-full">
                    Enable Automation
                  </Button>
                </CardContent>
              </Card>
            </div>

            <div className="mt-8 text-center">
              <div className="inline-flex items-center space-x-4">
                {connected && (
                  <div className="flex items-center space-x-2">
                    <Wallet className="w-4 h-4 text-green-600" />
                    <span className="text-sm text-gray-600">
                      Connected: {publicKey?.toString().slice(0, 8)}...
                    </span>
                    <WalletDisconnectButton />
                  </div>
                )}
                {tangemPublicKey && (
                  <div className="flex items-center space-x-2">
                    <CreditCard className="w-4 h-4 text-green-600" />
                    <span className="text-sm text-gray-600">
                      Tangem: {tangemPublicKey.slice(0, 8)}...
                    </span>
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => setTangemPublicKey(null)}
                    >
                      Disconnect
                    </Button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            🦸 CypherGuy
          </h1>
          <p className="text-xl text-gray-600 mb-2">
            Your personal DeFi assistant
          </p>
          <p className="text-gray-500">
            Choose your preferred authentication method
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Wallet Authentication */}
          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Wallet className="w-8 h-8 text-blue-600" />
              </div>
              <CardTitle>Wallet Authentication</CardTitle>
              <CardDescription>
                Connect with Phantom, Solflare, or other Solana wallets
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              {mounted ? (
                <WalletMultiButton className="w-full" />
              ) : (
                <Button className="w-full" disabled>
                  Loading...
                </Button>
              )}
            </CardContent>
          </Card>

          {/* Tangem Authentication */}
          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader className="text-center">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <CreditCard className="w-8 h-8 text-purple-600" />
              </div>
              <CardTitle>Tangem Card</CardTitle>
              <CardDescription>
                Tap your Tangem card for hardware-level security
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <Button 
                onClick={() => setAuthMethod('tangem')}
                className="w-full"
                variant="outline"
              >
                Connect Tangem Card
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Tangem Authentication Modal */}
        {authMethod === 'tangem' && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg max-w-md w-full">
              <div className="p-4 border-b">
                <div className="flex justify-between items-center">
                  <h3 className="text-lg font-semibold">Tangem Authentication</h3>
                  <Button 
                    variant="ghost" 
                    size="sm"
                    onClick={() => setAuthMethod(null)}
                  >
                    ✕
                  </Button>
                </div>
              </div>
              <div className="p-4">
                <TangemAuth 
                  onAuthSuccess={handleTangemSuccess}
                  onAuthError={handleTangemError}
                />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
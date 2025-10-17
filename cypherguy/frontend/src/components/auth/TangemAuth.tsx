'use client';

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { CreditCard, Smartphone, Wifi } from 'lucide-react';

interface TangemAuthProps {
  onAuthSuccess: (publicKey: string) => void;
  onAuthError: (error: string) => void;
}

export const TangemAuth: React.FC<TangemAuthProps> = ({ onAuthSuccess, onAuthError }) => {
  const [isConnecting, setIsConnecting] = useState(false);
  const [step, setStep] = useState<'idle' | 'detecting' | 'tap' | 'success' | 'error'>('idle');
  const [error, setError] = useState<string | null>(null);

  // Mock Tangem detection (in real implementation, this would use Tangem SDK)
  const detectTangemCard = async () => {
    setIsConnecting(true);
    setStep('detecting');
    setError(null);

    try {
      // Simulate card detection
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Check if NFC is available
      if (!navigator.nfc) {
        throw new Error('NFC not available. Please ensure NFC is enabled on your device.');
      }

      setStep('tap');
      
      // Simulate tap to authenticate
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      // Mock successful authentication
      const mockPublicKey = 'Tangem_' + Math.random().toString(36).substr(2, 9);
      onAuthSuccess(mockPublicKey);
      setStep('success');
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to connect to Tangem card';
      setError(errorMessage);
      setStep('error');
      onAuthError(errorMessage);
    } finally {
      setIsConnecting(false);
    }
  };

  const reset = () => {
    setStep('idle');
    setError(null);
    setIsConnecting(false);
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader className="text-center">
        <div className="mx-auto mb-4 w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
          <CreditCard className="w-8 h-8 text-white" />
        </div>
        <CardTitle>Tangem Card Authentication</CardTitle>
        <CardDescription>
          Tap your Tangem card to authenticate securely
        </CardDescription>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {step === 'idle' && (
          <div className="text-center space-y-4">
            <div className="space-y-2">
              <div className="flex items-center justify-center space-x-2 text-sm text-gray-600">
                <Smartphone className="w-4 h-4" />
                <span>Ensure NFC is enabled</span>
              </div>
              <div className="flex items-center justify-center space-x-2 text-sm text-gray-600">
                <Wifi className="w-4 h-4" />
                <span>Hold card near your device</span>
              </div>
            </div>
            <Button 
              onClick={detectTangemCard}
              className="w-full"
              size="lg"
            >
              Connect Tangem Card
            </Button>
          </div>
        )}

        {step === 'detecting' && (
          <div className="text-center space-y-4">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
            <p className="text-sm text-gray-600">Detecting Tangem card...</p>
          </div>
        )}

        {step === 'tap' && (
          <div className="text-center space-y-4">
            <div className="animate-pulse">
              <CreditCard className="w-16 h-16 text-blue-500 mx-auto" />
            </div>
            <p className="text-sm text-gray-600">Tap your Tangem card to the back of your device</p>
            <div className="flex justify-center">
              <Button variant="outline" onClick={reset}>
                Cancel
              </Button>
            </div>
          </div>
        )}

        {step === 'success' && (
          <div className="text-center space-y-4">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto">
              <CreditCard className="w-8 h-8 text-green-600" />
            </div>
            <p className="text-sm text-green-600 font-medium">Authentication successful!</p>
            <p className="text-xs text-gray-500">Your Tangem card is now connected</p>
          </div>
        )}

        {step === 'error' && (
          <div className="text-center space-y-4">
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto">
              <CreditCard className="w-8 h-8 text-red-600" />
            </div>
            <p className="text-sm text-red-600 font-medium">Authentication failed</p>
            <p className="text-xs text-gray-500">{error}</p>
            <Button variant="outline" onClick={reset} className="w-full">
              Try Again
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

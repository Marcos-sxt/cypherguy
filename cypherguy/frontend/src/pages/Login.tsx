import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Wallet, Sparkles } from 'lucide-react';
import logo from '@/assets/cypherguy-logo.png';

export default function Login() {
  const navigate = useNavigate();
  const [isConnecting, setIsConnecting] = useState(false);

  const handleConnect = () => {
    setIsConnecting(true);
    // Simulate wallet connection
    setTimeout(() => {
      navigate('/dashboard');
    }, 2000);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 relative overflow-hidden">
      {/* Background glow effect */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-64 opacity-30 blur-3xl bg-gradient-to-b from-primary to-transparent" />

      <div className="relative z-10 w-full max-w-md animate-fade-in">
        {/* Logo */}
        <div className="flex justify-center mb-8">
          <div className="relative">
            <img 
              src={logo} 
              alt="CypherGuy" 
              className="w-24 h-24"
            />
            {isConnecting && (
              <div className="absolute inset-0 rounded-full pulse-glow" />
            )}
          </div>
        </div>

        {/* Greeting */}
        <div className="text-center mb-12 space-y-3">
          <h1 className="text-4xl font-bold">
            Hi! I'm <span className="gradient-text">CypherGuy</span> 🦸
          </h1>
          <p className="text-muted-foreground text-lg">
            Your AI-powered DeFi superhero assistant
          </p>
        </div>

        {/* Connection Card */}
        <div className="glass-card p-8 rounded-2xl space-y-6">
          <div className="text-center space-y-2">
            <Sparkles className="w-12 h-12 mx-auto text-primary mb-4" />
            <h2 className="text-xl font-semibold">Ready to get started?</h2>
            <p className="text-sm text-muted-foreground">
              Connect your Tangem card or wallet to begin your DeFi journey
            </p>
          </div>

          <Button
            variant="cyber"
            size="lg"
            className="w-full"
            onClick={handleConnect}
            disabled={isConnecting}
          >
            {isConnecting ? (
              <>
                <div className="w-5 h-5 border-2 border-primary-foreground border-t-transparent rounded-full animate-spin" />
                Connecting...
              </>
            ) : (
              <>
                <Wallet className="w-5 h-5" />
                Connect Wallet
              </>
            )}
          </Button>

          <div className="text-center">
            <p className="text-xs text-muted-foreground">
              Supports Tangem, Phantom, and more
            </p>
          </div>
        </div>

        {/* Security Badge */}
        <div className="mt-8 text-center">
          <p className="text-xs text-muted-foreground flex items-center justify-center gap-2">
            <span className="w-2 h-2 bg-success rounded-full animate-pulse" />
            Secured with end-to-end encryption
          </p>
        </div>
      </div>
    </div>
  );
}

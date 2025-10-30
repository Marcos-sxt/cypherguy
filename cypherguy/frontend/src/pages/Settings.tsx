import { useState } from 'react';
import Layout from '@/components/Layout';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { ChevronRight, Wallet, Shield, Bell, Info, LogOut } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import TransactionModal from '@/components/TransactionModal';

export default function Settings() {
  const navigate = useNavigate();
  const [notifications, setNotifications] = useState(true);
  const [showTxModal, setShowTxModal] = useState(false);

  const handleDisconnect = () => {
    navigate('/');
  };

  const settingsSections = [
    {
      title: 'Wallet',
      items: [
        {
          icon: Wallet,
          label: 'Connected Wallet',
          value: 'Tangem Card',
          onClick: () => {},
        },
        {
          icon: Shield,
          label: 'Security',
          value: 'Biometric Enabled',
          onClick: () => {},
        },
      ],
    },
    {
      title: 'Preferences',
      items: [
        {
          icon: Bell,
          label: 'Notifications',
          toggle: true,
          value: notifications,
          onClick: () => setNotifications(!notifications),
        },
      ],
    },
    {
      title: 'About',
      items: [
        {
          icon: Info,
          label: 'Privacy Policy',
          onClick: () => {},
        },
        {
          icon: Info,
          label: 'Terms of Service',
          onClick: () => {},
        },
        {
          icon: Info,
          label: 'Version',
          value: '1.0.0',
        },
      ],
    },
  ];

  return (
    <Layout>
      <div className="max-w-2xl mx-auto space-y-6 animate-fade-in">
        <div className="pt-4 pb-2">
          <h1 className="text-2xl font-bold">Settings</h1>
          <p className="text-muted-foreground">Manage your account and preferences</p>
        </div>

        {/* Settings Sections */}
        {settingsSections.map((section, idx) => (
          <div key={idx} className="space-y-3">
            <h2 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">
              {section.title}
            </h2>
            <div className="glass-card rounded-2xl overflow-hidden">
              {section.items.map((item, itemIdx) => {
                const Icon = item.icon;
                return (
                  <button
                    key={itemIdx}
                    onClick={item.onClick}
                    disabled={!item.onClick}
                    className={`w-full flex items-center gap-4 p-4 hover:bg-accent/10 transition-colors ${
                      itemIdx !== section.items.length - 1 ? 'border-b border-border/50' : ''
                    }`}
                  >
                    <Icon className="w-5 h-5 text-primary flex-shrink-0" />
                    <span className="flex-1 text-left font-medium">{item.label}</span>
                    {item.toggle ? (
                      <Switch checked={item.value as boolean} />
                    ) : item.value ? (
                      <span className="text-sm text-muted-foreground">{item.value}</span>
                    ) : (
                      <ChevronRight className="w-5 h-5 text-muted-foreground" />
                    )}
                  </button>
                );
              })}
            </div>
          </div>
        ))}

        {/* Test Transaction Button */}
        <Button
          variant="outline"
          className="w-full"
          onClick={() => setShowTxModal(true)}
        >
          Test Transaction Modal
        </Button>

        {/* Disconnect Button */}
        <Button
          variant="destructive"
          className="w-full"
          onClick={handleDisconnect}
        >
          <LogOut className="w-4 h-4" />
          Disconnect Wallet
        </Button>
      </div>

      <TransactionModal
        open={showTxModal}
        onOpenChange={setShowTxModal}
        status="confirmed"
        txHash="5Kd8Y9...xJ3mP2"
      />
    </Layout>
  );
}

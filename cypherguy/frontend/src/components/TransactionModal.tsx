import { CheckCircle2, XCircle, Loader2, ExternalLink } from 'lucide-react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';

interface TransactionModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  status: 'pending' | 'confirmed' | 'failed';
  txHash?: string;
}

export default function TransactionModal({
  open,
  onOpenChange,
  status,
  txHash,
}: TransactionModalProps) {
  const getStatusContent = () => {
    switch (status) {
      case 'pending':
        return {
          icon: <Loader2 className="w-16 h-16 text-primary animate-spin" />,
          title: 'Transaction Pending',
          description: 'Please wait while your transaction is being processed...',
          color: 'text-primary',
        };
      case 'confirmed':
        return {
          icon: <CheckCircle2 className="w-16 h-16 text-success" />,
          title: 'Transaction Confirmed',
          description: 'Your transaction has been successfully completed!',
          color: 'text-success',
        };
      case 'failed':
        return {
          icon: <XCircle className="w-16 h-16 text-destructive" />,
          title: 'Transaction Failed',
          description: 'There was an issue processing your transaction. Please try again.',
          color: 'text-destructive',
        };
    }
  };

  const content = getStatusContent();

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="glass-card border-border/50 max-w-sm">
        <DialogHeader>
          <DialogTitle className="sr-only">{content.title}</DialogTitle>
        </DialogHeader>

        <div className="flex flex-col items-center space-y-6 py-6">
          {/* Icon with glow effect */}
          <div className={status === 'pending' ? 'pulse-glow' : ''}>
            {content.icon}
          </div>

          {/* Status Text */}
          <div className="text-center space-y-2">
            <h3 className={`text-xl font-bold ${content.color}`}>
              {content.title}
            </h3>
            <p className="text-sm text-muted-foreground">
              {content.description}
            </p>
          </div>

          {/* Transaction Hash */}
          {txHash && status === 'confirmed' && (
            <div className="w-full glass-card p-4 rounded-lg space-y-2">
              <p className="text-xs text-muted-foreground">Transaction Hash</p>
              <div className="flex items-center gap-2">
                <code className="text-xs text-primary flex-1 truncate">
                  {txHash}
                </code>
                <Button variant="ghost" size="icon" className="flex-shrink-0 h-8 w-8">
                  <ExternalLink className="w-4 h-4" />
                </Button>
              </div>
            </div>
          )}

          {/* Action Button */}
          {status !== 'pending' && (
            <Button
              variant={status === 'confirmed' ? 'default' : 'destructive'}
              className="w-full"
              onClick={() => onOpenChange(false)}
            >
              {status === 'confirmed' ? 'Done' : 'Try Again'}
            </Button>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}

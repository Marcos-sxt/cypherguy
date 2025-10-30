import { TrendingUp, TrendingDown } from 'lucide-react';

interface PortfolioCardProps {
  balance: string;
  change: number;
  changePercent: number;
}

export default function PortfolioCard({ balance, change, changePercent }: PortfolioCardProps) {
  const isPositive = change >= 0;

  return (
    <div className="glass-card p-6 rounded-2xl hover-lift">
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-medium text-muted-foreground">Total Balance</h3>
          <div className={`flex items-center gap-1 text-sm font-medium ${
            isPositive ? 'text-success' : 'text-destructive'
          }`}>
            {isPositive ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
            {changePercent.toFixed(2)}%
          </div>
        </div>
        
        <div className="space-y-1">
          <h2 className="text-4xl font-bold gradient-text">${balance}</h2>
          <p className={`text-sm ${isPositive ? 'text-success' : 'text-destructive'}`}>
            {isPositive ? '+' : ''}{change.toFixed(2)} USD (24h)
          </p>
        </div>

        <div className="pt-4 border-t border-border/50">
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">Available</span>
            <span className="font-medium">${(parseFloat(balance) * 0.95).toFixed(2)}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

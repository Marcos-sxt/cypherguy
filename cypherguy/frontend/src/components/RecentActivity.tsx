import { ArrowUpRight, ArrowDownLeft, RefreshCw } from 'lucide-react';

interface Activity {
  id: string;
  type: 'send' | 'receive' | 'swap';
  amount: string;
  token: string;
  timestamp: string;
  status: 'completed' | 'pending';
}

const activities: Activity[] = [
  {
    id: '1',
    type: 'receive',
    amount: '0.5',
    token: 'SOL',
    timestamp: '2 hours ago',
    status: 'completed',
  },
  {
    id: '2',
    type: 'swap',
    amount: '100',
    token: 'USDC',
    timestamp: '5 hours ago',
    status: 'completed',
  },
  {
    id: '3',
    type: 'send',
    amount: '0.25',
    token: 'ETH',
    timestamp: '1 day ago',
    status: 'completed',
  },
];

export default function RecentActivity() {
  const getIcon = (type: Activity['type']) => {
    switch (type) {
      case 'send':
        return <ArrowUpRight className="w-5 h-5 text-primary" />;
      case 'receive':
        return <ArrowDownLeft className="w-5 h-5 text-success" />;
      case 'swap':
        return <RefreshCw className="w-5 h-5 text-warning" />;
    }
  };

  const getTypeLabel = (type: Activity['type']) => {
    return type.charAt(0).toUpperCase() + type.slice(1);
  };

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-semibold">Recent Activity</h2>

      <div className="space-y-3">
        {activities.map((activity) => (
          <div
            key={activity.id}
            className="glass-card p-4 rounded-xl hover-lift flex items-center gap-4"
          >
            <div className="w-10 h-10 rounded-full bg-secondary flex items-center justify-center flex-shrink-0">
              {getIcon(activity.type)}
            </div>

            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between mb-1">
                <p className="font-medium text-sm">{getTypeLabel(activity.type)}</p>
                <p className="font-semibold text-sm">
                  {activity.amount} {activity.token}
                </p>
              </div>
              <div className="flex items-center justify-between">
                <p className="text-xs text-muted-foreground">{activity.timestamp}</p>
                <span className="text-xs text-success">Completed</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

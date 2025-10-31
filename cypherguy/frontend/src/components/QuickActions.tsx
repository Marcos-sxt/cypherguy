import { useNavigate } from 'react-router-dom';
import { CreditCard, Moon, Building2, Bot, ArrowRight } from 'lucide-react';

const actions = [
  { 
    icon: CreditCard, 
    label: 'Get Loan', 
    color: 'from-primary to-primary-glow',
    message: 'I want to borrow some USDC'
  },
  { 
    icon: Moon, 
    label: 'Trade Privately', 
    color: 'from-purple-500 to-purple-700',
    message: 'I want to trade privately'
  },
  { 
    icon: Building2, 
    label: 'Tokenize Asset', 
    color: 'from-blue-500 to-blue-700',
    message: 'I want to tokenize a property'
  },
  { 
    icon: Bot, 
    label: 'Auto-Invest', 
    color: 'from-green-500 to-green-700',
    message: 'I want to optimize my portfolio automatically'
  },
];

export default function QuickActions() {
  const navigate = useNavigate();

  const handleActionClick = (message: string) => {
    // Navigate to chat with pre-filled message
    navigate('/chat', { state: { initialMessage: message } });
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">Quick Actions</h2>
        <ArrowRight className="w-5 h-5 text-muted-foreground" />
      </div>

      <div className="grid grid-cols-2 gap-3">
        {actions.map((action) => {
          const Icon = action.icon;
          return (
            <button
              key={action.label}
              onClick={() => handleActionClick(action.message)}
              className="glass-card p-6 rounded-2xl hover-lift text-left group relative overflow-hidden cursor-pointer"
            >
              <div className={`absolute inset-0 bg-gradient-to-br ${action.color} opacity-0 group-hover:opacity-10 transition-opacity duration-300`} />
              <div className="relative space-y-3">
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${action.color} flex items-center justify-center`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <p className="font-medium text-sm">{action.label}</p>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}

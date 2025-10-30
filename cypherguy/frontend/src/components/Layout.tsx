import { ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, MessageSquare, Settings, Wallet } from 'lucide-react';
import logo from '@/assets/cypherguy-logo.png';

interface LayoutProps {
  children: ReactNode;
  showNav?: boolean;
}

export default function Layout({ children, showNav = true }: LayoutProps) {
  const location = useLocation();

  const navItems = [
    { path: '/dashboard', icon: Home, label: 'Home' },
    { path: '/chat', icon: MessageSquare, label: 'Chat' },
    { path: '/settings', icon: Settings, label: 'Settings' },
  ];

  return (
    <div className="min-h-screen flex flex-col">
      {/* Top Header with Logo */}
      <header className="p-4 flex justify-center items-center relative">
        <div className="flex items-center gap-3">
          <img src={logo} alt="CypherGuy" className="w-10 h-10" />
          <h1 className="text-2xl font-bold gradient-text">CypherGuy</h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 px-4 pb-24 overflow-y-auto">
        {children}
      </main>

      {/* Bottom Navigation */}
      {showNav && (
        <nav className="fixed bottom-0 left-0 right-0 glass-card border-t border-border/50 px-4 py-3">
          <div className="max-w-2xl mx-auto flex justify-around items-center">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex flex-col items-center gap-1 px-4 py-2 rounded-lg transition-all duration-300 ${
                    isActive
                      ? 'text-primary glow-effect'
                      : 'text-muted-foreground hover:text-foreground'
                  }`}
                >
                  <Icon className={isActive ? 'w-6 h-6' : 'w-5 h-5'} />
                  <span className="text-xs font-medium">{item.label}</span>
                </Link>
              );
            })}
          </div>
        </nav>
      )}
    </div>
  );
}

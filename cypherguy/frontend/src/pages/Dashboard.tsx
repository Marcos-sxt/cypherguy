import Layout from '@/components/Layout';
import PortfolioCard from '@/components/PortfolioCard';
import QuickActions from '@/components/QuickActions';
import RecentActivity from '@/components/RecentActivity';

export default function Dashboard() {
  // Mock data
  const portfolioData = {
    balance: '12,847.32',
    change: 324.56,
    changePercent: 2.59,
  };

  return (
    <Layout>
      <div className="max-w-2xl mx-auto space-y-6 animate-fade-in">
        {/* Welcome Message */}
        <div className="pt-4 pb-2">
          <h1 className="text-2xl font-bold mb-1">Welcome back!</h1>
          <p className="text-muted-foreground">Here's your portfolio overview</p>
        </div>

        {/* Portfolio Card */}
        <PortfolioCard {...portfolioData} />

        {/* Quick Actions */}
        <QuickActions />

        {/* Recent Activity */}
        <RecentActivity />
      </div>
    </Layout>
  );
}

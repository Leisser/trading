"use client";

import React, { useState, useEffect } from 'react';
import { Icon } from "@iconify/react";
import { useRouter } from 'next/navigation';

interface AdminStats {
  total_users: number;
  active_users: number;
  pending_deposits: number;
  pending_withdrawals: number;
  total_platform_value: number;
  total_deposits_24h: number;
  total_withdrawals_24h: number;
}

interface PendingRequest {
  id: number;
  user_email: string;
  user_name: string;
  amount: number;
  cryptocurrency_symbol?: string;
  cryptocurrency_name?: string;
  wallet_name?: string;
  transaction_hash?: string;
  from_address?: string;
  status: string;
  created_at: string;
  review_notes?: string;
  confirmed_at?: string;
}

interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  is_superuser: boolean;
  is_staff: boolean;
  date_joined: string;
  last_login: string;
  total_balance_usd: number;
}

export default function BoardPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [isAdmin, setIsAdmin] = useState(false);
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [pendingDeposits, setPendingDeposits] = useState<PendingRequest[]>([]);
  const [allDeposits, setAllDeposits] = useState<PendingRequest[]>([]);
  const [pendingWithdrawals, setPendingWithdrawals] = useState<PendingRequest[]>([]);
  const [activeTab, setActiveTab] = useState<'overview' | 'deposit_requests' | 'all_deposits' | 'withdrawals'>('overview');
  
  // Users modal state
  const [showUsersModal, setShowUsersModal] = useState(false);
  const [users, setUsers] = useState<User[]>([]);
  const [usersLoading, setUsersLoading] = useState(false);
  
  // Trading settings state
  const [showTradingSettings, setShowTradingSettings] = useState(false);
  const [tradingMode, setTradingMode] = useState<'idle' | 'active'>('idle');
  const [idleProfitPercent, setIdleProfitPercent] = useState('5');
  const [idleDurationMin, setIdleDurationMin] = useState('30');
  const [activeWinRate, setActiveWinRate] = useState('20');
  const [activeProfitPercent, setActiveProfitPercent] = useState('10');
  const [activeLossPercent, setActiveLossPercent] = useState('80');
  const [activeDurationMin, setActiveDurationMin] = useState('5');
  const [useRealPrices, setUseRealPrices] = useState(false);

  useEffect(() => {
    checkAdminAccess();
  }, []);

  const checkAdminAccess = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        alert('Please sign in to access this page');
        router.push('/signin');
        return;
      }

      // Get user profile to check is_superuser
      const profileResponse = await fetch('http://localhost:8000/api/profile/', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!profileResponse.ok) {
        alert('Please sign in to access this page');
        router.push('/signin');
        return;
      }

      const userProfile = await profileResponse.json();
      
      // Check if user is superuser
      if (!userProfile.is_superuser) {
        alert('Access denied. This page is only for superadmins.');
        router.push('/');
        return;
      }

      // User is superuser, grant access
      setIsAdmin(true);
      loadAdminData();
    } catch (error) {
      console.error('Admin access check failed:', error);
      router.push('/');
    } finally {
      setLoading(false);
    }
  };

  const loadAdminData = async () => {
    try {
      const token = localStorage.getItem('access_token');
      
      // Load dashboard stats from API
      const statsResponse = await fetch('http://localhost:8000/api/dashboard/stats/', {
        headers: { 'Authorization': `Bearer ${token}` },
      });
      
      let dashboardStats = null;
      if (statsResponse.ok) {
        dashboardStats = await statsResponse.json();
      }
      
      // Load pending deposits
      const depositsResponse = await fetch('http://localhost:8000/api/admin/deposits/', {
        headers: { 'Authorization': `Bearer ${token}` },
      });
      
      let allDepositsData: PendingRequest[] = [];
      if (depositsResponse.ok) {
        allDepositsData = await depositsResponse.json();
        setPendingDeposits(allDepositsData.filter((d: PendingRequest) => d.status === 'pending'));
        setAllDeposits(allDepositsData);
      }

      // Load pending withdrawals
      const withdrawalsResponse = await fetch('http://localhost:8000/api/admin/withdrawals/', {
        headers: { 'Authorization': `Bearer ${token}` },
      });
      
      let allWithdrawals: PendingRequest[] = [];
      if (withdrawalsResponse.ok) {
        allWithdrawals = await withdrawalsResponse.json();
        setPendingWithdrawals(allWithdrawals.filter((w: PendingRequest) => w.status === 'pending'));
      }

      // Set stats from API data
      console.log('Dashboard Stats from API:', dashboardStats);
      console.log('Total Balance from API:', dashboardStats?.total_balance);
      console.log('Total Balance type:', typeof dashboardStats?.total_balance);
      
      setStats({
        total_users: dashboardStats?.total_users || 4,
        active_users: 1, // This isn't provided by the API yet
        pending_deposits: dashboardStats?.pending_deposits || 0,
        pending_withdrawals: dashboardStats?.pending_withdrawals || 0,
        total_platform_value: dashboardStats?.total_balance || 0,
        total_deposits_24h: 0, // This isn't provided by the API yet
        total_withdrawals_24h: 0, // This isn't provided by the API yet
      });
    } catch (error) {
      console.error('Failed to load admin data:', error);
    }
  };

  const loadUsersData = async () => {
    try {
      setUsersLoading(true);
      const token = localStorage.getItem('access_token');
      
      const response = await fetch('http://localhost:8000/api/admin/users/', {
        headers: { 'Authorization': `Bearer ${token}` },
      });
      
      if (response.ok) {
        const data = await response.json();
        setUsers(data.users || []);
      } else {
        console.error('Failed to load users data');
      }
    } catch (error) {
      console.error('Failed to load users data:', error);
    } finally {
      setUsersLoading(false);
    }
  };

  const handleUsersClick = () => {
    setShowUsersModal(true);
    loadUsersData();
  };
  
  const loadTradingSettings = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://localhost:8000/api/admin/settings/mode-status/', {
        headers: { 'Authorization': `Bearer ${token}` },
      });
      
      if (response.ok) {
        const data = await response.json();
        setTradingMode(data.current_mode);
        
        const settings = data.settings;
        setIdleProfitPercent(settings.idle_profit_percentage);
        setIdleDurationMin((settings.idle_duration_seconds / 60).toString());
        setActiveWinRate(settings.active_win_rate_percentage || '20');
        setActiveProfitPercent(settings.active_profit_percentage || '10');
        setActiveLossPercent(settings.active_loss_percentage);
        setActiveDurationMin((settings.active_duration_seconds / 60).toString());
        setUseRealPrices(settings.use_real_prices || false);
      }
    } catch (error) {
      console.error('Failed to load trading settings:', error);
    }
  };
  
  const handleTradingSettingsClick = () => {
    loadTradingSettings();
    setShowTradingSettings(true);
  };
  
  const handleSaveTradingSettings = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://localhost:8000/api/admin/settings/activity-based/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          idle_profit_percentage: parseFloat(idleProfitPercent),
          idle_duration_seconds: parseInt(idleDurationMin) * 60,
          active_win_rate_percentage: parseFloat(activeWinRate),
          active_profit_percentage: parseFloat(activeProfitPercent),
          active_loss_percentage: parseFloat(activeLossPercent),
          active_duration_seconds: parseInt(activeDurationMin) * 60,
          use_real_prices: useRealPrices
        })
      });
      
      if (response.ok) {
        alert('Trading settings updated successfully!');
        setShowTradingSettings(false);
      } else {
        alert('Failed to update settings');
      }
    } catch (error) {
      console.error('Failed to save settings:', error);
      alert('Failed to save settings');
    }
  };
  
  const handleSetToDefault = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://localhost:8000/api/admin/settings/default/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        alert('Settings reset to default!\n\nIdle Mode: 5% profit every 30 minutes\n\nActive Mode:\n• 20% win rate → 10% profit\n• 80% lose rate → 80% loss\n• Duration: 5 minutes');
        loadTradingSettings();
      } else {
        alert('Failed to reset settings');
      }
    } catch (error) {
      console.error('Failed to reset settings:', error);
      alert('Failed to reset settings');
    }
  };

  const handleApproveDeposit = async (depositId: number) => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`http://localhost:8000/api/admin/deposits/${depositId}/approve/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          action: 'approve',
          admin_notes: 'Approved via admin board'
        }),
      });

      if (response.ok) {
        alert('Deposit approved successfully!');
        loadAdminData();
      } else {
        const error = await response.json();
        alert(`Error: ${error.error || 'Failed to approve deposit'}`);
      }
    } catch (error) {
      console.error('Approve deposit error:', error);
      alert('Failed to approve deposit');
    }
  };

  const handleRejectDeposit = async (depositId: number) => {
    const reason = prompt('Enter rejection reason:');
    if (!reason) return;

    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`http://localhost:8000/api/admin/deposits/${depositId}/approve/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          action: 'reject',
          admin_notes: reason
        }),
      });

      if (response.ok) {
        alert('Deposit rejected');
        loadAdminData();
      } else {
        const error = await response.json();
        alert(`Error: ${error.error || 'Failed to reject deposit'}`);
      }
    } catch (error) {
      console.error('Reject deposit error:', error);
      alert('Failed to reject deposit');
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 8
    }).format(amount);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-darkmode pt-32 pb-16">
        <div className="container mx-auto max-w-7xl px-4">
          <div className="text-center">
            <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary mx-auto"></div>
            <p className="text-white mt-4">Checking admin access...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!isAdmin) {
    return null;
  }

  return (
    <div className="min-h-screen bg-darkmode pt-32 pb-16">
      <div className="container mx-auto max-w-7xl px-4">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-white text-4xl font-bold mb-2">Superadmin Board</h1>
              <p className="text-muted text-lg">Platform management and oversight</p>
            </div>
            <div className="flex items-center gap-2 bg-primary bg-opacity-20 px-4 py-2 rounded-lg">
              <Icon icon="tabler:shield-check" width="24" height="24" className="text-primary" />
              <span className="text-primary font-semibold">Superadmin Access</span>
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-dark_grey rounded-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <Icon icon="tabler:users" width="32" height="32" className="text-primary" />
                <div className="text-right">
                  <p className="text-white text-3xl font-bold">{stats.total_users}</p>
                  <p className="text-muted text-sm">Total Users</p>
                </div>
              </div>
              <div className="text-success text-sm mb-4">
                {stats.active_users} active
              </div>
              <div className="flex gap-2">
                <button
                  onClick={handleUsersClick}
                  className="flex-1 bg-primary text-white py-2 px-3 rounded-lg hover:bg-opacity-90 transition-all text-sm flex items-center justify-center gap-2"
                >
                  <Icon icon="tabler:eye" width="16" height="16" />
                  View
                </button>
                <button
                  onClick={() => router.push('/users')}
                  className="flex-1 bg-success text-white py-2 px-3 rounded-lg hover:bg-opacity-90 transition-all text-sm flex items-center justify-center gap-2"
                >
                  <Icon icon="tabler:users" width="16" height="16" />
                  Users
                </button>
              </div>
            </div>

            <div className="bg-dark_grey rounded-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <Icon icon="tabler:arrow-down-circle" width="32" height="32" className="text-success" />
                <div className="text-right">
                  <p className="text-white text-3xl font-bold">{stats.pending_deposits}</p>
                  <p className="text-muted text-sm">Pending Deposits</p>
                </div>
              </div>
              <div className="text-warning text-sm">
                Requires review
              </div>
            </div>

            <div className="bg-dark_grey rounded-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <Icon icon="tabler:arrow-up-circle" width="32" height="32" className="text-warning" />
                <div className="text-right">
                  <p className="text-white text-3xl font-bold">{stats.pending_withdrawals}</p>
                  <p className="text-muted text-sm">Pending Withdrawals</p>
                </div>
              </div>
              <div className="text-warning text-sm">
                Requires review
              </div>
            </div>

            <div className="bg-dark_grey rounded-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <Icon icon="tabler:wallet" width="32" height="32" className="text-secondary" />
                <div className="text-right">
                  <p className="text-white text-3xl font-bold">${formatCurrency(stats.total_platform_value)}</p>
                  <p className="text-muted text-sm">Platform Value</p>
                </div>
              </div>
              <div className="text-muted text-sm">
                Total in USD
              </div>
            </div>
          </div>
        )}
          
        {/* Trading Control Card */}
        {stats && (
          <div className="bg-gradient-to-br from-primary/20 to-dark_grey rounded-lg p-6 mb-8 border border-primary/30">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <Icon icon="tabler:settings" width="32" height="32" className="text-primary" />
                <div>
                  <h3 className="text-white text-xl font-bold">Trading Control</h3>
                  <p className="text-muted text-sm">Manage profit/loss settings</p>
                </div>
              </div>
              <div className={`px-4 py-2 rounded-lg ${tradingMode === 'active' ? 'bg-error/20 text-error' : 'bg-success/20 text-success'}`}>
                <span className="font-bold text-sm">{tradingMode === 'active' ? '🔴 ACTIVE' : '🟢 IDLE'}</span>
              </div>
            </div>
            
            <div className="grid md:grid-cols-2 gap-4 mb-4">
              <div className="bg-success/10 border border-success/20 rounded-lg p-4">
                <p className="text-success font-semibold mb-2">💰 Idle Mode</p>
                <p className="text-white text-sm">+{idleProfitPercent}% profit</p>
                <p className="text-muted text-xs">Every {idleDurationMin} minutes</p>
              </div>
              <div className="bg-error/10 border border-error/20 rounded-lg p-4">
                <p className="text-error font-semibold mb-2">📉 Active Mode</p>
                <p className="text-white text-sm">-{activeLossPercent}% loss</p>
                <p className="text-muted text-xs">Every {activeDurationMin} minutes</p>
              </div>
            </div>
            
            <div className="flex gap-2">
              <button
                onClick={handleTradingSettingsClick}
                className="flex-1 bg-primary text-white py-3 px-4 rounded-lg hover:bg-opacity-90 transition-all flex items-center justify-center gap-2"
              >
                <Icon icon="tabler:edit" width="18" height="18" />
                Configure
              </button>
              <button
                onClick={handleSetToDefault}
                className="flex-1 bg-success text-white py-3 px-4 rounded-lg hover:bg-opacity-90 transition-all flex items-center justify-center gap-2"
              >
                <Icon icon="tabler:refresh" width="18" height="18" />
                Set to Default
              </button>
            </div>
          </div>
        )}

        {/* Tabs */}
        <div className="flex flex-wrap gap-1 bg-dark_grey rounded-lg p-1 mb-8">
          {[
            { id: 'overview', label: 'Overview', icon: 'tabler:dashboard' },
            { id: 'deposit_requests', label: `Deposit Requests (${pendingDeposits.length})`, icon: 'tabler:clock' },
            { id: 'all_deposits', label: `All Deposits (${allDeposits.length})`, icon: 'tabler:arrow-down' },
            { id: 'withdrawals', label: `Withdrawals (${pendingWithdrawals.length})`, icon: 'tabler:arrow-up' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex-1 flex items-center justify-center gap-2 py-3 px-4 rounded-md transition-all min-w-[150px] ${
                activeTab === tab.id
                  ? 'bg-primary text-darkmode'
                  : 'text-muted hover:text-white'
              }`}
            >
              <Icon icon={tab.icon} width="20" height="20" />
              <span className="text-sm">{tab.label}</span>
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="bg-dark_grey rounded-lg p-6">
          {activeTab === 'overview' && (
            <div>
              <h3 className="text-white text-xl font-semibold mb-6">Platform Overview</h3>
              <div className="grid md:grid-cols-2 gap-6">
                {/* Quick Actions */}
                <div className="bg-darkmode rounded-lg p-6">
                  <h4 className="text-white text-lg font-medium mb-4">Quick Actions</h4>
                  <div className="space-y-3">
                    <button
                      onClick={() => setActiveTab('deposit_requests')}
                      className="w-full flex items-center justify-between p-4 bg-dark_grey hover:bg-opacity-80 rounded-lg transition-all"
                    >
                      <div className="flex items-center gap-3">
                        <Icon icon="tabler:arrow-down-circle" width="24" height="24" className="text-success" />
                        <span className="text-white">Review Deposit Requests</span>
                      </div>
                      {pendingDeposits.length > 0 && (
                        <span className="bg-warning text-darkmode px-3 py-1 rounded-full text-sm font-semibold">
                          {pendingDeposits.length}
                        </span>
                      )}
                    </button>

                    <button
                      onClick={() => setActiveTab('withdrawals')}
                      className="w-full flex items-center justify-between p-4 bg-dark_grey hover:bg-opacity-80 rounded-lg transition-all"
                    >
                      <div className="flex items-center gap-3">
                        <Icon icon="tabler:arrow-up-circle" width="24" height="24" className="text-warning" />
                        <span className="text-white">Review Withdrawals</span>
                      </div>
                      {pendingWithdrawals.length > 0 && (
                        <span className="bg-warning text-darkmode px-3 py-1 rounded-full text-sm font-semibold">
                          {pendingWithdrawals.length}
                        </span>
                      )}
                    </button>

                    <a
                      href="http://localhost:3001"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="w-full flex items-center justify-between p-4 bg-dark_grey hover:bg-opacity-80 rounded-lg transition-all"
                    >
                      <div className="flex items-center gap-3">
                        <Icon icon="tabler:settings" width="24" height="24" className="text-primary" />
                        <span className="text-white">Advanced Admin Panel</span>
                      </div>
                      <Icon icon="tabler:external-link" width="20" height="20" className="text-muted" />
                    </a>
                  </div>
                </div>

                {/* Recent Activity */}
                <div className="bg-darkmode rounded-lg p-6">
                  <h4 className="text-white text-lg font-medium mb-4">Recent Activity</h4>
                  <div className="space-y-3">
                    {pendingDeposits.length === 0 && pendingWithdrawals.length === 0 ? (
                      <p className="text-muted text-center py-8">No pending requests</p>
                    ) : (
                      <>
                        {pendingDeposits.slice(0, 3).map((deposit) => (
                          <div key={`deposit-${deposit.id}`} className="flex items-center gap-3 p-3 bg-dark_grey rounded">
                            <Icon icon="tabler:arrow-down" width="20" height="20" className="text-success" />
                            <div className="flex-1">
                              <p className="text-white text-sm">{deposit.user_email}</p>
                              <p className="text-muted text-xs">Deposit: {deposit.amount} {deposit.cryptocurrency_symbol}</p>
                            </div>
                            <span className="text-warning text-xs">Pending</span>
                          </div>
                        ))}
                        {pendingWithdrawals.slice(0, 3).map((withdrawal) => (
                          <div key={`withdrawal-${withdrawal.id}`} className="flex items-center gap-3 p-3 bg-dark_grey rounded">
                            <Icon icon="tabler:arrow-up" width="20" height="20" className="text-warning" />
                            <div className="flex-1">
                              <p className="text-white text-sm">{withdrawal.user_email}</p>
                              <p className="text-muted text-xs">Withdrawal: {withdrawal.amount}</p>
                            </div>
                            <span className="text-warning text-xs">Pending</span>
                          </div>
                        ))}
                      </>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'deposit_requests' && (
            <div>
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h3 className="text-white text-2xl font-semibold">User Deposit Requests</h3>
                  <p className="text-muted text-sm mt-1">Review and approve pending deposit requests from users</p>
                </div>
                <div className="bg-warning bg-opacity-20 px-4 py-2 rounded-lg">
                  <p className="text-warning font-semibold">{pendingDeposits.length} Pending</p>
                </div>
              </div>

              {pendingDeposits.length === 0 ? (
                <div className="text-center py-12 bg-darkmode rounded-lg">
                  <Icon icon="tabler:check-circle" width="64" height="64" className="text-success mx-auto mb-4" />
                  <p className="text-white text-lg font-medium mb-2">All caught up!</p>
                  <p className="text-muted">No pending deposit requests to review</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {pendingDeposits.map((deposit) => (
                    <div key={deposit.id} className="bg-darkmode rounded-lg p-6 border-l-4 border-warning">
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex items-center gap-3">
                          <div className="w-12 h-12 bg-warning bg-opacity-20 rounded-full flex items-center justify-center">
                            <Icon icon="tabler:clock" width="24" height="24" className="text-warning" />
                          </div>
                          <div>
                            <p className="text-white font-semibold text-lg">{deposit.user_name || deposit.user_email}</p>
                            <p className="text-muted text-sm">{deposit.user_email}</p>
                          </div>
                        </div>
                        <span className="bg-warning bg-opacity-20 text-warning px-4 py-2 rounded-full text-sm font-semibold uppercase">
                          {deposit.status}
                        </span>
                      </div>
                      
                      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4 p-4 bg-dark_grey rounded-lg">
                        <div>
                          <p className="text-muted text-xs mb-1">Request ID</p>
                          <p className="text-white font-mono">#{deposit.id}</p>
                        </div>
                        <div>
                          <p className="text-muted text-xs mb-1">Amount</p>
                          <p className="text-success font-semibold text-lg">{formatCurrency(deposit.amount)} {deposit.cryptocurrency_symbol}</p>
                        </div>
                        <div>
                          <p className="text-muted text-xs mb-1">Cryptocurrency</p>
                          <p className="text-white">{deposit.cryptocurrency_name || deposit.cryptocurrency_symbol}</p>
                        </div>
                        <div>
                          <p className="text-muted text-xs mb-1">Deposit Wallet</p>
                          <p className="text-white text-sm">{deposit.wallet_name || 'N/A'}</p>
                        </div>
                      </div>

                      {(deposit.transaction_hash || deposit.from_address) && (
                        <div className="mb-4 p-4 bg-dark_grey rounded-lg">
                          {deposit.transaction_hash && (
                            <div className="mb-2">
                              <p className="text-muted text-xs mb-1">Transaction Hash</p>
                              <p className="text-white text-sm font-mono break-all">{deposit.transaction_hash}</p>
                            </div>
                          )}
                          {deposit.from_address && (
                            <div>
                              <p className="text-muted text-xs mb-1">From Address</p>
                              <p className="text-white text-sm font-mono break-all">{deposit.from_address}</p>
                            </div>
                          )}
                        </div>
                      )}

                      <div className="mb-4">
                        <p className="text-muted text-xs mb-1">Submitted</p>
                        <p className="text-white text-sm">{formatDate(deposit.created_at)}</p>
                      </div>

                      <div className="flex gap-3 pt-4 border-t border-dark_border">
                        <button
                          onClick={() => handleApproveDeposit(deposit.id)}
                          className="flex-1 bg-success text-white py-3 px-6 rounded-lg hover:bg-opacity-90 transition-all flex items-center justify-center gap-2 font-semibold"
                        >
                          <Icon icon="tabler:check" width="20" height="20" />
                          Approve & Credit User
                        </button>
                        <button
                          onClick={() => handleRejectDeposit(deposit.id)}
                          className="flex-1 bg-error text-white py-3 px-6 rounded-lg hover:bg-opacity-90 transition-all flex items-center justify-center gap-2 font-semibold"
                        >
                          <Icon icon="tabler:x" width="20" height="20" />
                          Reject Request
                        </button>
                      </div>

                      <div className="mt-4 p-3 bg-primary bg-opacity-10 border border-primary border-opacity-30 rounded">
                        <p className="text-primary text-xs">
                          <Icon icon="tabler:info-circle" width="14" height="14" className="inline mr-1" />
                          Approving will create a Deposit record, credit the user's wallet, and update wallet statistics.
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'all_deposits' && (
            <div>
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h3 className="text-white text-2xl font-semibold">All Deposit Requests</h3>
                  <p className="text-muted text-sm mt-1">View all deposit requests (pending, confirmed, and rejected)</p>
                </div>
                <div className="bg-primary bg-opacity-20 px-4 py-2 rounded-lg">
                  <p className="text-primary font-semibold">{allDeposits.length} Total</p>
                </div>
              </div>

              {allDeposits.length === 0 ? (
                <div className="text-center py-12 bg-darkmode rounded-lg">
                  <Icon icon="tabler:inbox" width="64" height="64" className="text-muted mx-auto mb-4" />
                  <p className="text-muted">No deposit requests found</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {allDeposits.map((deposit) => (
                    <div 
                      key={deposit.id} 
                      className={`bg-darkmode rounded-lg p-6 border-l-4 ${
                        deposit.status === 'confirmed' ? 'border-success' :
                        deposit.status === 'rejected' ? 'border-error' :
                        'border-warning'
                      }`}
                    >
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex items-center gap-3">
                          <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                            deposit.status === 'confirmed' ? 'bg-success bg-opacity-20' :
                            deposit.status === 'rejected' ? 'bg-error bg-opacity-20' :
                            'bg-warning bg-opacity-20'
                          }`}>
                            <Icon 
                              icon={
                                deposit.status === 'confirmed' ? 'tabler:check-circle' :
                                deposit.status === 'rejected' ? 'tabler:x-circle' :
                                'tabler:clock'
                              }
                              width="24" 
                              height="24" 
                              className={
                                deposit.status === 'confirmed' ? 'text-success' :
                                deposit.status === 'rejected' ? 'text-error' :
                                'text-warning'
                              }
                            />
                          </div>
                          <div>
                            <p className="text-white font-semibold">{deposit.user_name || deposit.user_email}</p>
                            <p className="text-muted text-sm">{deposit.user_email}</p>
                          </div>
                        </div>
                        <span className={`px-4 py-2 rounded-full text-sm font-semibold uppercase ${
                          deposit.status === 'confirmed' ? 'bg-success bg-opacity-20 text-success' :
                          deposit.status === 'rejected' ? 'bg-error bg-opacity-20 text-error' :
                          'bg-warning bg-opacity-20 text-warning'
                        }`}>
                          {deposit.status}
                        </span>
                      </div>
                      
                      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4 p-4 bg-dark_grey rounded-lg">
                        <div>
                          <p className="text-muted text-xs mb-1">Request ID</p>
                          <p className="text-white font-mono">#{deposit.id}</p>
                        </div>
                        <div>
                          <p className="text-muted text-xs mb-1">Amount</p>
                          <p className="text-white font-semibold">{formatCurrency(deposit.amount)} {deposit.cryptocurrency_symbol}</p>
                        </div>
                        <div>
                          <p className="text-muted text-xs mb-1">Cryptocurrency</p>
                          <p className="text-white">{deposit.cryptocurrency_name || deposit.cryptocurrency_symbol}</p>
                        </div>
                        <div>
                          <p className="text-muted text-xs mb-1">Wallet</p>
                          <p className="text-white text-sm">{deposit.wallet_name || 'N/A'}</p>
                        </div>
                      </div>

                      <div className="grid md:grid-cols-2 gap-4 text-sm">
                        <div>
                          <p className="text-muted text-xs mb-1">Submitted</p>
                          <p className="text-white">{formatDate(deposit.created_at)}</p>
                        </div>
                        {deposit.confirmed_at && (
                          <div>
                            <p className="text-muted text-xs mb-1">Confirmed</p>
                            <p className="text-white">{formatDate(deposit.confirmed_at)}</p>
                          </div>
                        )}
                      </div>

                      {deposit.review_notes && (
                        <div className="mt-4 p-3 bg-dark_grey rounded">
                          <p className="text-muted text-xs mb-1">Admin Notes</p>
                          <p className="text-white text-sm">{deposit.review_notes}</p>
                        </div>
                      )}

                      {deposit.status === 'pending' && (
                        <div className="flex gap-3 mt-4 pt-4 border-t border-dark_border">
                          <button
                            onClick={() => handleApproveDeposit(deposit.id)}
                            className="flex-1 bg-success text-white py-2 px-4 rounded-lg hover:bg-opacity-90 transition-all flex items-center justify-center gap-2"
                          >
                            <Icon icon="tabler:check" width="18" height="18" />
                            Approve
                          </button>
                          <button
                            onClick={() => handleRejectDeposit(deposit.id)}
                            className="flex-1 bg-error text-white py-2 px-4 rounded-lg hover:bg-opacity-90 transition-all flex items-center justify-center gap-2"
                          >
                            <Icon icon="tabler:x" width="18" height="18" />
                            Reject
                          </button>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'withdrawals' && (
            <div>
              <h3 className="text-white text-xl font-semibold mb-6">Pending Withdrawals</h3>
              {pendingWithdrawals.length === 0 ? (
                <div className="text-center py-12">
                  <Icon icon="tabler:inbox" width="64" height="64" className="text-muted mx-auto mb-4" />
                  <p className="text-muted">No pending withdrawals</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {pendingWithdrawals.map((withdrawal) => (
                    <div key={withdrawal.id} className="bg-darkmode rounded-lg p-6">
                      <div className="flex items-center justify-between mb-4">
                        <div>
                          <p className="text-white font-medium">{withdrawal.user_name || withdrawal.user_email}</p>
                          <p className="text-muted text-sm">{withdrawal.user_email}</p>
                        </div>
                        <span className="bg-warning bg-opacity-20 text-warning px-3 py-1 rounded-full text-sm">
                          {withdrawal.status}
                        </span>
                      </div>
                      
                      <div className="grid md:grid-cols-2 gap-4 mb-4">
                        <div>
                          <p className="text-muted text-sm">Amount</p>
                          <p className="text-white font-semibold">{formatCurrency(withdrawal.amount)}</p>
                        </div>
                        <div>
                          <p className="text-muted text-sm">Submitted</p>
                          <p className="text-white text-sm">{formatDate(withdrawal.created_at)}</p>
                        </div>
                      </div>

                      <div className="flex gap-3">
                        <button
                          className="flex-1 bg-success text-white py-2 px-4 rounded-lg hover:bg-opacity-90 transition-all flex items-center justify-center gap-2"
                        >
                          <Icon icon="tabler:check" width="20" height="20" />
                          Approve
                        </button>
                        <button
                          className="flex-1 bg-error text-white py-2 px-4 rounded-lg hover:bg-opacity-90 transition-all flex items-center justify-center gap-2"
                        >
                          <Icon icon="tabler:x" width="20" height="20" />
                          Reject
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer Info */}
        <div className="mt-8 p-4 bg-primary bg-opacity-10 border border-primary border-opacity-30 rounded-lg">
          <div className="flex items-start gap-3">
            <Icon icon="tabler:info-circle" width="24" height="24" className="text-primary flex-shrink-0" />
            <div>
              <p className="text-primary font-semibold mb-1">Superadmin Board Information</p>
              <p className="text-muted text-sm">
                This page is only accessible to superadmins (is_superuser = True). 
                Use this board to review and approve pending deposits and withdrawals, 
                monitor platform statistics, and perform administrative tasks.
              </p>
              <p className="text-muted text-sm mt-2">
                For advanced features, visit the <a href="http://localhost:3001" target="_blank" className="text-primary hover:underline">Vue.js Admin Dashboard</a>.
              </p>
            </div>
          </div>
        </div>

        {/* Trading Settings Modal */}
        {showTradingSettings && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 overflow-y-auto">
            <div className="bg-darkmode rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto my-8">
              <div className="flex items-center justify-between p-6 border-b border-dark_border">
                <h2 className="text-white text-2xl font-bold">Trading Control Settings</h2>
                <button
                  onClick={() => setShowTradingSettings(false)}
                  className="text-muted hover:text-white transition-colors"
                >
                  <Icon icon="tabler:x" width="24" height="24" />
                </button>
              </div>
              
              <div className="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
                {/* Current Mode Display */}
                <div className={`mb-6 p-4 rounded-lg ${tradingMode === 'active' ? 'bg-error/10 border border-error/20' : 'bg-success/10 border border-success/20'}`}>
                  <div className="flex items-center gap-3 mb-2">
                    <Icon icon={tradingMode === 'active' ? 'tabler:chart-down' : 'tabler:chart-up'} width="24" height="24" className={tradingMode === 'active' ? 'text-error' : 'text-success'} />
                    <p className={`font-bold ${tradingMode === 'active' ? 'text-error' : 'text-success'}`}>
                      Current Mode: {tradingMode === 'active' ? 'ACTIVE TRADING' : 'IDLE MODE'}
                    </p>
                  </div>
                  <p className="text-muted text-sm">
                    {tradingMode === 'active' 
                      ? '🔴 Users have traded in the last 10 minutes - Probability-based outcomes active'
                      : '🟢 No recent trading activity - PROFIT mode active'}
                  </p>
                </div>
                
                {/* Idle Mode Settings */}
                <div className="bg-success/5 border border-success/20 rounded-lg p-6 mb-4">
                  <h3 className="text-success font-semibold text-lg mb-4 flex items-center gap-2">
                    <Icon icon="tabler:moneybag" width="20" height="20" />
                    Idle Mode Settings (No Active Trading)
                  </h3>
                  
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <label className="text-muted text-sm mb-2 block">Profit Percentage (%)</label>
                      <input
                        type="number"
                        value={idleProfitPercent}
                        onChange={(e) => setIdleProfitPercent(e.target.value)}
                        className="w-full bg-darkmode border border-dark_border rounded-lg px-4 py-3 text-white focus:outline-none focus:border-success"
                        placeholder="5"
                      />
                    </div>
                    <div>
                      <label className="text-muted text-sm mb-2 block">Duration (minutes)</label>
                      <input
                        type="number"
                        value={idleDurationMin}
                        onChange={(e) => setIdleDurationMin(e.target.value)}
                        className="w-full bg-darkmode border border-dark_border rounded-lg px-4 py-3 text-white focus:outline-none focus:border-success"
                        placeholder="30"
                      />
                    </div>
                  </div>
                  <p className="text-muted text-xs mt-2">
                    📊 Result: Users gain +{idleProfitPercent}% every {idleDurationMin} minutes when no one is trading
                  </p>
                </div>
                
                {/* Active Mode Settings */}
                <div className="bg-error/5 border border-error/20 rounded-lg p-6 mb-6">
                  <h3 className="text-error font-semibold text-lg mb-4 flex items-center gap-2">
                    <Icon icon="tabler:chart-line-down" width="20" height="20" />
                    Active Mode Settings (Users Trading)
                  </h3>
                  
                  <div className="bg-primary/10 border border-primary/30 rounded-lg p-4 mb-4">
                    <h4 className="text-primary font-semibold text-sm mb-3 flex items-center gap-2">
                      <Icon icon="tabler:percentage" width="16" height="16" />
                      Profit Probability (NEW!)
                    </h4>
                    <div className="grid md:grid-cols-2 gap-4">
                      <div>
                        <label className="text-muted text-xs mb-2 block">Win Rate (%)</label>
                        <input
                          type="number"
                          min="0"
                          max="100"
                          value={activeWinRate}
                          onChange={(e) => setActiveWinRate(e.target.value)}
                          className="w-full bg-darkmode border border-dark_border rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary"
                          placeholder="20"
                        />
                        <p className="text-muted text-xs mt-1">Chance of profit (0-100%)</p>
                      </div>
                      <div>
                        <label className="text-muted text-xs mb-2 block">Profit Amount (%)</label>
                        <input
                          type="number"
                          value={activeProfitPercent}
                          onChange={(e) => setActiveProfitPercent(e.target.value)}
                          className="w-full bg-darkmode border border-dark_border rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary"
                          placeholder="10"
                        />
                        <p className="text-muted text-xs mt-1">Profit when users win</p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <label className="text-muted text-sm mb-2 block">Loss Percentage (%)</label>
                      <input
                        type="number"
                        value={activeLossPercent}
                        onChange={(e) => setActiveLossPercent(e.target.value)}
                        className="w-full bg-darkmode border border-dark_border rounded-lg px-4 py-3 text-white focus:outline-none focus:border-error"
                        placeholder="80"
                      />
                    </div>
                    <div>
                      <label className="text-muted text-sm mb-2 block">Duration (minutes)</label>
                      <input
                        type="number"
                        value={activeDurationMin}
                        onChange={(e) => setActiveDurationMin(e.target.value)}
                        className="w-full bg-darkmode border border-dark_border rounded-lg px-4 py-3 text-white focus:outline-none focus:border-error"
                        placeholder="5"
                      />
                    </div>
                  </div>
                  <div className="bg-darkmode/50 rounded-lg p-3 mt-3">
                    <p className="text-muted text-xs">
                      📊 <span className="font-semibold">Result:</span> When users are actively trading:
                    </p>
                    <p className="text-success text-xs mt-1">
                      • {activeWinRate}% chance → +{activeProfitPercent}% profit in {activeDurationMin} min
                    </p>
                    <p className="text-error text-xs">
                      • {100 - parseFloat(activeWinRate)}% chance → -{activeLossPercent}% loss in {activeDurationMin} min
                    </p>
                  </div>
                </div>
                
                {/* Real Prices Toggle */}
                <div className="bg-primary/5 border border-primary/20 rounded-lg p-6 mb-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-primary font-semibold text-lg mb-1 flex items-center gap-2">
                        <Icon icon="tabler:world" width="20" height="20" />
                        Real Price Integration
                      </h3>
                      <p className="text-muted text-sm">
                        Enable fetching real cryptocurrency prices from exchanges (CoinGecko/CCXT)
                      </p>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className={`text-sm font-semibold ${useRealPrices ? 'text-success' : 'text-muted'}`}>
                        {useRealPrices ? 'ENABLED' : 'DISABLED'}
                      </span>
                      <button
                        onClick={() => setUseRealPrices(!useRealPrices)}
                        className={`relative inline-flex h-8 w-14 items-center rounded-full transition-colors ${
                          useRealPrices ? 'bg-success' : 'bg-dark_border'
                        }`}
                      >
                        <span
                          className={`inline-block h-6 w-6 transform rounded-full bg-white transition-transform ${
                            useRealPrices ? 'translate-x-7' : 'translate-x-1'
                          }`}
                        />
                      </button>
                    </div>
                  </div>
                  {useRealPrices && (
                    <div className="mt-4 bg-success/10 border border-success/30 rounded-lg p-3">
                      <p className="text-success text-xs flex items-center gap-2">
                        <Icon icon="tabler:check" width="16" height="16" />
                        <span className="font-semibold">Real prices active</span> - Charts will display live market data from Binance/CoinGecko
                      </p>
                    </div>
                  )}
                </div>
                
                {/* Action Buttons */}
                <div className="flex gap-3">
                  <button
                    onClick={handleSaveTradingSettings}
                    className="flex-1 bg-primary text-white py-3 px-6 rounded-lg hover:bg-opacity-90 transition-all font-semibold"
                  >
                    Save Settings
                  </button>
                  <button
                    onClick={handleSetToDefault}
                    className="flex-1 bg-success text-white py-3 px-6 rounded-lg hover:bg-opacity-90 transition-all font-semibold"
                  >
                    Set to Default
                  </button>
                  <button
                    onClick={() => setShowTradingSettings(false)}
                    className="bg-dark_grey text-white py-3 px-6 rounded-lg hover:bg-opacity-90 transition-all"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
        
        {/* Users Modal */}
        {showUsersModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-darkmode rounded-lg max-w-4xl w-full max-h-[80vh] overflow-hidden">
              <div className="flex items-center justify-between p-6 border-b border-dark_border">
                <h2 className="text-white text-2xl font-bold">All Users</h2>
                <button
                  onClick={() => setShowUsersModal(false)}
                  className="text-muted hover:text-white transition-colors"
                >
                  <Icon icon="tabler:x" width="24" height="24" />
                </button>
              </div>
              
              <div className="p-6 overflow-y-auto max-h-[60vh]">
                {usersLoading ? (
                  <div className="text-center py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
                    <p className="text-muted">Loading users...</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {users.map((user) => (
                      <div key={user.id} className="bg-dark_grey rounded-lg p-4">
                        <div className="flex items-center justify-between mb-3">
                          <div className="flex items-center gap-3">
                            <div className="w-10 h-10 bg-primary bg-opacity-20 rounded-full flex items-center justify-center">
                              <Icon icon="tabler:user" width="20" height="20" className="text-primary" />
                            </div>
                            <div>
                              <p className="text-white font-medium">
                                {user.first_name && user.last_name 
                                  ? `${user.first_name} ${user.last_name}` 
                                  : user.email}
                              </p>
                              <p className="text-muted text-sm">{user.email}</p>
                            </div>
                          </div>
                          <div className="text-right">
                            <p className="text-white text-lg font-bold">
                              ${user.total_balance_usd.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                            </p>
                            <div className="flex items-center gap-2 mt-1">
                              <span className={`px-2 py-1 rounded-full text-xs ${
                                user.is_active 
                                  ? 'bg-success bg-opacity-20 text-success' 
                                  : 'bg-error bg-opacity-20 text-error'
                              }`}>
                                {user.is_active ? 'Active' : 'Inactive'}
                              </span>
                              {user.is_superuser && (
                                <span className="px-2 py-1 rounded-full text-xs bg-warning bg-opacity-20 text-warning">
                                  Admin
                                </span>
                              )}
                              {user.is_staff && (
                                <span className="px-2 py-1 rounded-full text-xs bg-primary bg-opacity-20 text-primary">
                                  Staff
                                </span>
                              )}
                            </div>
                          </div>
                        </div>
                        
                        <div className="grid md:grid-cols-2 gap-4 text-sm">
                          <div>
                            <p className="text-muted">Joined</p>
                            <p className="text-white">{new Date(user.date_joined).toLocaleDateString()}</p>
                          </div>
                          <div>
                            <p className="text-muted">Last Login</p>
                            <p className="text-white">
                              {user.last_login 
                                ? new Date(user.last_login).toLocaleDateString()
                                : 'Never'
                              }
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}


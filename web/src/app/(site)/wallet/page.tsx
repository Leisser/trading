"use client";

import React, { useState, useEffect } from 'react';
import { Icon } from "@iconify/react";
import { apiEndpoint } from '@/config/api';

interface WalletData {
  balance: number;
  address: string;
  is_active: boolean;
}

interface CryptoBalance {
  id: number;
  cryptocurrency: number;
  cryptocurrency_symbol: string;
  cryptocurrency_name: string;
  balance: number;
  locked_balance: number;
  available_balance: number;
  current_price: number;
  balance_usd: number;
  total_deposited: number;
  total_withdrawn: number;
}

interface MultiCurrencyWallet {
  id: number;
  wallet_address: string;
  total_balance_usd: number;
  balances: CryptoBalance[];
  count: number;
}

interface Transaction {
  id: number;
  type: 'deposit' | 'withdrawal';
  amount: number;
  cryptocurrency: string;
  status: string;
  created_at: string;
  transaction_hash?: string;
  destination_address?: string;
  wallet_address?: string;
}

interface DepositWallet {
  id: number;
  cryptocurrency: string;
  cryptocurrency_name: string;
  wallet_address: string;
  wallet_name: string;
  is_primary: boolean;
  network: string;
  min_confirmations: number;
}

interface Cryptocurrency {
  id: number;
  symbol: string;
  name: string;
  current_price: number;
  is_active: boolean;
  is_tradeable: boolean;
}

interface Trade {
  id: number | string;
  type?: 'trade' | 'strategy';
  cryptocurrency: string;
  cryptocurrency_symbol: string;
  trade_type: 'buy' | 'sell' | 'swap';
  amount: number;
  price: number;
  total_value: number;
  leverage: number;
  status: 'pending' | 'executed' | 'cancelled' | 'failed';
  pnl: number;
  profit_loss: number;
  fees: number;
  created_at: string;
  executed_at?: string;
  strategy_name?: string;
  reason?: string;
}

export default function WalletPage() {
  const [wallet, setWallet] = useState<WalletData | null>(null);
  const [multiCurrencyWallet, setMultiCurrencyWallet] = useState<MultiCurrencyWallet | null>(null);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [trades, setTrades] = useState<Trade[]>([]);
  const [depositWallets, setDepositWallets] = useState<DepositWallet[]>([]);
  const [cryptocurrencies, setCryptocurrencies] = useState<Cryptocurrency[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'balances' | 'trades' | 'deposit' | 'withdraw'>('balances');
  
  // Form states
  const [depositAmount, setDepositAmount] = useState('');
  const [selectedCryptoCurrency, setSelectedCryptoCurrency] = useState<number | ''>('');
  const [selectedDepositWallet, setSelectedDepositWallet] = useState<number | ''>('');
  const [withdrawAmount, setWithdrawAmount] = useState('');
  const [withdrawAddress, setWithdrawAddress] = useState('');
  const [withdrawCryptoCurrency, setWithdrawCryptoCurrency] = useState<number | ''>('');

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('access_token');
    if (!token) {
      alert('Please sign in to access your wallet');
      window.location.href = '/signin';
      return;
    }
    
    loadWalletData();
    loadMultiCurrencyWallet();
    loadTransactions();
    loadTrades();
    loadCryptocurrencies();
    loadDepositWallets();
  }, []);

  const loadWalletData = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(apiEndpoint('/api/balance/'), {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        setWallet(data);
      }
    } catch (error) {
      console.error('Failed to load wallet data:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadMultiCurrencyWallet = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(apiEndpoint('/api/crypto-balances/'), {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        setMultiCurrencyWallet(data);
      }
    } catch (error) {
      console.error('Failed to load multi-currency wallet:', error);
    }
  };

  const loadTransactions = async () => {
    try {
      const token = localStorage.getItem('access_token');
      
      // Load deposits
      const depositsResponse = await fetch(apiEndpoint('/api/deposit/request/'), {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      // Load withdrawals
      const withdrawalsResponse = await fetch(apiEndpoint('/api/withdrawal/request/'), {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      const deposits = depositsResponse.ok ? await depositsResponse.json() : [];
      const withdrawals = withdrawalsResponse.ok ? await withdrawalsResponse.json() : [];
      
      // Combine and sort transactions
      const allTransactions = [
        ...deposits.map((d: any) => ({ ...d, type: 'deposit' })),
        ...withdrawals.map((w: any) => ({ ...w, type: 'withdrawal' }))
      ].sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
      
      setTransactions(allTransactions);
    } catch (error) {
      console.error('Failed to load transactions:', error);
    }
  };

  const loadTrades = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(apiEndpoint('/api/trading/history/'), {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        setTrades(data.results || data);
      }
    } catch (error) {
      console.error('Failed to load trades:', error);
    }
  };

  const loadCryptocurrencies = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(apiEndpoint('/api/cryptocurrencies/'), {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        setCryptocurrencies(data.results || data);
        
        // Set default selected crypto to first one if available
        if ((data.results || data).length > 0) {
          setSelectedCryptoCurrency((data.results || data)[0].id);
          setWithdrawCryptoCurrency((data.results || data)[0].id);
        }
      } else {
        console.error('Failed to load cryptocurrencies:', response.status, response.statusText);
      }
    } catch (error) {
      console.error('Failed to load cryptocurrencies:', error);
    }
  };

  const loadDepositWallets = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(apiEndpoint('/api/deposit/wallets/'), {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        // API now returns {wallets: [...], count: N}
        const wallets = data.wallets || data;
        setDepositWallets(wallets);
      } else {
        console.error('Failed to load deposit wallets:', response.status, response.statusText);
      }
    } catch (error) {
      console.error('Failed to load deposit wallets:', error);
    }
  };

  // Get deposit wallets filtered by selected cryptocurrency
  const getFilteredDepositWallets = () => {
    if (!selectedCryptoCurrency) return [];
    const selectedCrypto = cryptocurrencies.find(c => c.id === selectedCryptoCurrency);
    if (!selectedCrypto) return [];
    
    return depositWallets.filter(w => w.cryptocurrency === selectedCrypto.symbol);
  };

  const handleDeposit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedCryptoCurrency || !selectedDepositWallet) {
      alert('Please select both cryptocurrency and deposit wallet');
      return;
    }
    
    try {
      const token = localStorage.getItem('access_token');
      const selectedWallet = depositWallets.find(w => w.id === selectedDepositWallet);
      
      const response = await fetch(apiEndpoint('/api/deposit/request/'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          amount: parseFloat(depositAmount),
          deposit_wallet: selectedDepositWallet,
          transaction_hash: '',
          from_address: ''  // User can optionally provide this
        }),
      });
      
      if (response.ok) {
        const result = await response.json();
        alert('Deposit request submitted successfully! Please send funds to the wallet address.');
        setDepositAmount('');
        setSelectedDepositWallet('');
        loadTransactions();
        loadMultiCurrencyWallet();
      } else {
        const error = await response.json();
        console.error('Deposit error response:', error);
        alert(`Error: ${error.error || JSON.stringify(error)}`);
      }
    } catch (error) {
      console.error('Deposit error:', error);
      alert('Failed to submit deposit request');
    }
  };

  const handleWithdraw = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!withdrawCryptoCurrency) {
      alert('Please select a cryptocurrency');
      return;
    }
    
    try {
      const token = localStorage.getItem('access_token');
      const selectedCrypto = cryptocurrencies.find(c => c.id === withdrawCryptoCurrency);
      
      const response = await fetch(apiEndpoint('/api/withdrawal/request/'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          amount: parseFloat(withdrawAmount),
          cryptocurrency: selectedCrypto?.symbol,
          destination_address: withdrawAddress
        }),
      });
      
      if (response.ok) {
        alert('Withdrawal request submitted successfully!');
        setWithdrawAmount('');
        setWithdrawAddress('');
        loadTransactions();
        loadWalletData();
        loadMultiCurrencyWallet();
      } else {
        const error = await response.json();
        alert(`Error: ${error.error || 'Failed to submit withdrawal request'}`);
      }
    } catch (error) {
      console.error('Withdrawal error:', error);
      alert('Failed to submit withdrawal request');
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
        <div className="container mx-auto max-w-6xl px-4">
          <div className="text-center">
            <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary mx-auto"></div>
            <p className="text-white mt-4">Loading wallet...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-darkmode pt-32 pb-16">
      <div className="container mx-auto max-w-6xl px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-white text-4xl font-bold mb-4">My Wallet</h1>
          <p className="text-muted text-lg">Manage your funds, deposits, and withdrawals</p>
        </div>

        {/* Balance Card */}
        <div className="bg-gradient-to-r from-primary to-secondary rounded-lg p-8 mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-darkmode text-lg font-medium mb-2">Total Portfolio Value</h2>
              <p className="text-darkmode text-4xl font-bold">
                ${multiCurrencyWallet ? formatCurrency(multiCurrencyWallet.total_balance_usd) : '0.00'}
              </p>
              <p className="text-darkmode text-sm mt-2 opacity-80">
                {multiCurrencyWallet?.count || 0} Different Cryptocurrencies
              </p>
            </div>
            <div className="text-darkmode">
              <Icon icon="tabler:wallet" width="64" height="64" />
            </div>
          </div>
          <div className="mt-4 pt-4 border-t border-darkmode border-opacity-20">
            <p className="text-darkmode text-sm">
              Multi-Currency Wallet: {multiCurrencyWallet?.wallet_address || 'Creating...'}
            </p>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex flex-wrap space-x-1 bg-dark_grey rounded-lg p-1 mb-8">
          {[
            { id: 'balances', label: 'My Balances', icon: 'tabler:coins' },
            { id: 'trades', label: 'Trade History', icon: 'tabler:chart-candle' },
            { id: 'overview', label: 'Transactions', icon: 'tabler:chart-line' },
            { id: 'deposit', label: 'Deposit', icon: 'tabler:arrow-down' },
            { id: 'withdraw', label: 'Withdraw', icon: 'tabler:arrow-up' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex-1 flex items-center justify-center gap-2 py-3 px-4 rounded-md transition-all ${
                activeTab === tab.id
                  ? 'bg-primary text-darkmode'
                  : 'text-muted hover:text-white'
              }`}
            >
              <Icon icon={tab.icon} width="20" height="20" />
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="bg-dark_grey rounded-lg p-6">
          {activeTab === 'balances' && (
            <div>
              <h3 className="text-white text-xl font-semibold mb-6">Cryptocurrency Balances</h3>
              {!multiCurrencyWallet || multiCurrencyWallet.balances.length === 0 ? (
                <div className="text-center py-12">
                  <Icon icon="tabler:wallet-off" width="64" height="64" className="text-muted mx-auto mb-4" />
                  <p className="text-muted mb-4">No cryptocurrency balances yet</p>
                  <p className="text-sm text-muted">Make a deposit to add funds to your wallet</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {multiCurrencyWallet.balances.map((balance) => (
                    <div key={balance.id} className="flex items-center justify-between p-4 bg-darkmode rounded-lg hover:bg-opacity-80 transition-all">
                      <div className="flex items-center gap-4">
                        <div className="w-12 h-12 rounded-full bg-primary bg-opacity-20 flex items-center justify-center">
                          <span className="text-primary font-bold text-lg">
                            {balance.cryptocurrency_symbol.charAt(0)}
                          </span>
                        </div>
                        <div>
                          <p className="text-white font-medium">{balance.cryptocurrency_name}</p>
                          <p className="text-muted text-sm">{balance.cryptocurrency_symbol}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-white font-semibold">
                          {formatCurrency(balance.balance)} {balance.cryptocurrency_symbol}
                        </p>
                        <p className="text-success text-sm">
                          ≈ ${formatCurrency(balance.balance_usd)}
                        </p>
                        <p className="text-muted text-xs mt-1">
                          Available: {formatCurrency(balance.available_balance)}
                        </p>
                      </div>
                    </div>
                  ))}
                  
                  {/* Summary Card */}
                  <div className="mt-6 p-4 bg-primary bg-opacity-10 rounded-lg border border-primary border-opacity-30">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div>
                        <p className="text-muted text-sm">Total Value</p>
                        <p className="text-white font-semibold">${formatCurrency(multiCurrencyWallet.total_balance_usd)}</p>
                      </div>
                      <div>
                        <p className="text-muted text-sm">Assets</p>
                        <p className="text-white font-semibold">{multiCurrencyWallet.count}</p>
                      </div>
                      <div>
                        <p className="text-muted text-sm">Total Deposited</p>
                        <p className="text-white font-semibold">
                          {formatCurrency(multiCurrencyWallet.balances.reduce((sum, b) => sum + b.total_deposited, 0))}
                        </p>
                      </div>
                      <div>
                        <p className="text-muted text-sm">Total Withdrawn</p>
                        <p className="text-white font-semibold">
                          {formatCurrency(multiCurrencyWallet.balances.reduce((sum, b) => sum + b.total_withdrawn, 0))}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'trades' && (
            <div>
              <h3 className="text-white text-xl font-semibold mb-6">Trade History</h3>
              {trades.length === 0 ? (
                <div className="text-center py-12">
                  <Icon icon="tabler:chart-candle" width="64" height="64" className="text-muted mx-auto mb-4" />
                  <p className="text-muted mb-2">No trades yet</p>
                  <p className="text-sm text-muted">Start trading to see your history here</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {trades.map((trade) => (
                    <div key={trade.id} className="bg-darkmode rounded-lg p-5 hover:bg-opacity-80 transition-all">
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex items-center gap-3">
                          {/* Trade Type Badge */}
                          <div className={`px-3 py-1 rounded-full text-xs font-semibold ${
                            trade.trade_type === 'buy' 
                              ? 'bg-success bg-opacity-20 text-success' 
                              : trade.trade_type === 'sell'
                              ? 'bg-error bg-opacity-20 text-error'
                              : 'bg-primary bg-opacity-20 text-primary'
                          }`}>
                            {trade.trade_type.toUpperCase()}
                          </div>
                          
                          {/* Strategy Badge */}
                          {trade.type === 'strategy' && (
                            <div className="px-2 py-1 rounded-full text-xs font-semibold bg-purple-500 bg-opacity-20 text-purple-400">
                              STRATEGY
                            </div>
                          )}
                          
                          {/* Cryptocurrency */}
                          <div>
                            <p className="text-white font-semibold text-lg">{trade.cryptocurrency_symbol}</p>
                            <p className="text-muted text-xs">
                              {formatDate(trade.created_at)}
                              {trade.strategy_name && (
                                <span className="ml-2 text-purple-400">• {trade.strategy_name}</span>
                              )}
                            </p>
                          </div>
                        </div>
                        
                        {/* Status */}
                        <div className="flex items-center gap-2">
                          <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                            trade.status === 'executed' ? 'bg-success bg-opacity-20 text-success' :
                            trade.status === 'pending' ? 'bg-warning bg-opacity-20 text-warning' :
                            trade.status === 'cancelled' ? 'bg-muted bg-opacity-20 text-muted' :
                            'bg-error bg-opacity-20 text-error'
                          }`}>
                            {trade.status}
                          </span>
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-3">
                        {/* Amount */}
                        <div>
                          <p className="text-muted text-xs mb-1">Amount</p>
                          <p className="text-white text-sm font-medium">
                            {trade.amount.toFixed(8)} {trade.cryptocurrency_symbol}
                          </p>
                        </div>
                        
                        {/* Price */}
                        <div>
                          <p className="text-muted text-xs mb-1">Price</p>
                          <p className="text-white text-sm font-medium">
                            ${trade.price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                          </p>
                        </div>
                        
                        {/* Total Value */}
                        <div>
                          <p className="text-muted text-xs mb-1">Total Value</p>
                          <p className="text-white text-sm font-medium">
                            ${trade.total_value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                          </p>
                        </div>
                        
                        {/* P&L */}
                        <div>
                          <p className="text-muted text-xs mb-1">Profit/Loss</p>
                          <p className={`text-sm font-semibold ${
                            trade.pnl > 0 ? 'text-success' : trade.pnl < 0 ? 'text-error' : 'text-muted'
                          }`}>
                            {trade.pnl >= 0 ? '+' : ''}${trade.pnl.toFixed(2)}
                          </p>
                        </div>
                      </div>
                      
                      {/* Additional Info Row */}
                      <div className="flex items-center justify-between pt-3 border-t border-dark_border">
                        <div className="flex items-center gap-4 text-xs">
                          {trade.leverage > 1 && (
                            <div className="flex items-center gap-1">
                              <Icon icon="tabler:arrows-diagonal" width="14" height="14" className="text-primary" />
                              <span className="text-primary font-semibold">{trade.leverage}x Leverage</span>
                            </div>
                          )}
                          {trade.fees > 0 && (
                            <div className="flex items-center gap-1">
                              <Icon icon="tabler:coin" width="14" height="14" className="text-muted" />
                              <span className="text-muted">Fee: ${trade.fees.toFixed(4)}</span>
                            </div>
                          )}
                        </div>
                        <div className="text-xs text-muted">
                          {trade.type === 'strategy' ? 'Strategy Execution' : 'Trade'} #{typeof trade.id === 'string' ? trade.id.replace('strategy_', '') : trade.id}
                        </div>
                      </div>
                    </div>
                  ))}
                  
                  {/* Summary Card */}
                  {trades.length > 0 && (
                    <div className="mt-6 p-5 bg-primary bg-opacity-10 rounded-lg border border-primary border-opacity-30">
                      <h4 className="text-primary font-semibold mb-3">Trading Summary</h4>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div>
                          <p className="text-muted text-sm">Total Trades</p>
                          <p className="text-white font-semibold text-lg">{trades.length}</p>
                        </div>
                        <div>
                          <p className="text-muted text-sm">Winning Trades</p>
                          <p className="text-success font-semibold text-lg">
                            {trades.filter(t => t.pnl > 0).length}
                          </p>
                        </div>
                        <div>
                          <p className="text-muted text-sm">Losing Trades</p>
                          <p className="text-error font-semibold text-lg">
                            {trades.filter(t => t.pnl < 0).length}
                          </p>
                        </div>
                        <div>
                          <p className="text-muted text-sm">Total P&L</p>
                          <p className={`font-semibold text-lg ${
                            trades.reduce((sum, t) => sum + t.pnl, 0) > 0 ? 'text-success' : 
                            trades.reduce((sum, t) => sum + t.pnl, 0) < 0 ? 'text-error' : 'text-muted'
                          }`}>
                            {trades.reduce((sum, t) => sum + t.pnl, 0) >= 0 ? '+' : ''}
                            ${trades.reduce((sum, t) => sum + t.pnl, 0).toFixed(2)}
                          </p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {activeTab === 'overview' && (
            <div>
              <h3 className="text-white text-xl font-semibold mb-6">Recent Transactions</h3>
              {transactions.length === 0 ? (
                <div className="text-center py-12">
                  <Icon icon="tabler:inbox" width="64" height="64" className="text-muted mx-auto mb-4" />
                  <p className="text-muted">No transactions yet</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {transactions.slice(0, 10).map((transaction) => (
                    <div key={`${transaction.type}-${transaction.id}`} className="flex items-center justify-between p-4 bg-darkmode rounded-lg">
                      <div className="flex items-center gap-4">
                        <div className={`p-2 rounded-full ${
                          transaction.type === 'deposit' ? 'bg-success bg-opacity-20' : 'bg-warning bg-opacity-20'
                        }`}>
                          <Icon 
                            icon={transaction.type === 'deposit' ? 'tabler:arrow-down' : 'tabler:arrow-up'} 
                            width="20" 
                            height="20" 
                            className={transaction.type === 'deposit' ? 'text-success' : 'text-warning'}
                          />
                        </div>
                        <div>
                          <p className="text-white font-medium capitalize">{transaction.type}</p>
                          <p className="text-muted text-sm">{formatDate(transaction.created_at)}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className={`font-semibold ${
                          transaction.type === 'deposit' ? 'text-success' : 'text-warning'
                        }`}>
                          {transaction.type === 'deposit' ? '+' : '-'}${formatCurrency(transaction.amount)}
                        </p>
                        <p className="text-muted text-sm">{transaction.cryptocurrency}</p>
                        <span className={`inline-block px-2 py-1 rounded text-xs ${
                          transaction.status === 'approved' ? 'bg-success bg-opacity-20 text-success' :
                          transaction.status === 'pending' ? 'bg-warning bg-opacity-20 text-warning' :
                          'bg-error bg-opacity-20 text-error'
                        }`}>
                          {transaction.status}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'deposit' && (
            <div>
              <h3 className="text-white text-xl font-semibold mb-6">Deposit Funds</h3>
              <div className="grid md:grid-cols-2 gap-8">
                <div>
                  <form onSubmit={handleDeposit} className="space-y-6">
                    <div>
                      <label className="block text-white text-sm font-medium mb-2">
                        Select Cryptocurrency
                      </label>
                      <select
                        value={selectedCryptoCurrency}
                        onChange={(e) => {
                          setSelectedCryptoCurrency(Number(e.target.value));
                          setSelectedDepositWallet(''); // Reset wallet selection when crypto changes
                        }}
                        className="w-full px-4 py-3 bg-darkmode border border-dark_border rounded-lg text-white focus:outline-none focus:border-primary"
                        disabled={cryptocurrencies.length === 0}
                        required
                      >
                        <option value="">Choose a cryptocurrency...</option>
                        {cryptocurrencies.map((crypto) => (
                          <option key={crypto.id} value={crypto.id}>
                            {crypto.name} ({crypto.symbol})
                          </option>
                        ))}
                      </select>
                      {cryptocurrencies.length === 0 && (
                        <p className="text-warning text-sm mt-2">
                          Loading cryptocurrencies...
                        </p>
                      )}
                    </div>

                    <div>
                      <label className="block text-white text-sm font-medium mb-2">
                        Select Deposit Wallet
                      </label>
                      <select
                        value={selectedDepositWallet}
                        onChange={(e) => setSelectedDepositWallet(Number(e.target.value))}
                        className="w-full px-4 py-3 bg-darkmode border border-dark_border rounded-lg text-white focus:outline-none focus:border-primary"
                        disabled={!selectedCryptoCurrency || getFilteredDepositWallets().length === 0}
                        required
                      >
                        <option value="">Choose a wallet...</option>
                        {getFilteredDepositWallets().map((wallet) => (
                          <option key={wallet.id} value={wallet.id}>
                            {wallet.wallet_name} - {wallet.network}
                          </option>
                        ))}
                      </select>
                      {selectedCryptoCurrency && getFilteredDepositWallets().length === 0 && (
                        <p className="text-warning text-sm mt-2">
                          No deposit wallets available for this cryptocurrency
                        </p>
                      )}
                    </div>
                    
                    <div>
                      <label className="block text-white text-sm font-medium mb-2">
                        Amount
                      </label>
                      <input
                        type="number"
                        step="0.00000001"
                        value={depositAmount}
                        onChange={(e) => setDepositAmount(e.target.value)}
                        placeholder="Enter amount"
                        className="w-full px-4 py-3 bg-darkmode border border-dark_border rounded-lg text-white focus:outline-none focus:border-primary"
                        required
                      />
                    </div>
                    
                    <button
                      type="submit"
                      className="w-full bg-primary text-darkmode py-3 px-6 rounded-lg font-semibold hover:bg-opacity-90 transition-all"
                    >
                      Submit Deposit Request
                    </button>
                  </form>
                </div>
                
                <div>
                  <h4 className="text-white text-lg font-medium mb-4">Deposit Instructions</h4>
                  <div className="bg-darkmode p-4 rounded-lg">
                    {!selectedCryptoCurrency || !selectedDepositWallet ? (
                      <div className="text-center py-8">
                        <Icon icon="tabler:info-circle" width="48" height="48" className="text-muted mx-auto mb-3" />
                        <p className="text-muted text-sm">Select cryptocurrency and wallet to view deposit instructions</p>
                      </div>
                    ) : (() => {
                      const selectedCrypto = cryptocurrencies.find(c => c.id === selectedCryptoCurrency);
                      const selectedWallet = depositWallets.find(w => w.id === selectedDepositWallet);
                      
                      return selectedWallet && selectedCrypto ? (
                        <div>
                          <div className="mb-4 p-3 bg-primary bg-opacity-10 border border-primary border-opacity-30 rounded">
                            <p className="text-primary text-sm font-semibold mb-1">Selected Wallet</p>
                            <p className="text-white text-sm">{selectedWallet.wallet_name}</p>
                            <p className="text-muted text-xs">{selectedCrypto.name} ({selectedCrypto.symbol})</p>
                          </div>
                          
                          <p className="text-muted text-sm mb-2">Send {selectedCrypto.symbol} to:</p>
                          <div className="flex items-center gap-2 mb-4">
                            <p className="text-white font-mono text-sm break-all flex-1 bg-dark_grey p-2 rounded">
                              {selectedWallet.wallet_address}
                            </p>
                            <button
                              type="button"
                              onClick={() => {
                                navigator.clipboard.writeText(selectedWallet.wallet_address);
                                alert('Address copied to clipboard!');
                              }}
                              className="px-3 py-2 bg-primary text-darkmode rounded hover:bg-opacity-90 transition-all text-sm whitespace-nowrap"
                            >
                              <Icon icon="tabler:copy" width="16" height="16" className="inline mr-1" />
                              Copy
                            </button>
                          </div>
                          <div className="bg-warning bg-opacity-10 border border-warning border-opacity-30 rounded p-3 text-sm">
                            <p className="text-warning font-semibold mb-2">⚠️ Important Instructions:</p>
                            <ul className="list-disc list-inside space-y-1 text-muted">
                              <li>Only send {selectedCrypto.symbol} to this address</li>
                              <li>Network: {selectedWallet.network || 'Mainnet'}</li>
                              <li>Deposits require admin approval</li>
                              <li>Processing time: 1-24 hours</li>
                              <li>Minimum deposit: 0.001 {selectedCrypto.symbol}</li>
                              <li>Wrong network = Lost funds!</li>
                            </ul>
                          </div>
                        </div>
                      ) : null;
                    })()}
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'withdraw' && (
            <div>
              <h3 className="text-white text-xl font-semibold mb-6">Withdraw Funds</h3>
              <div className="max-w-md">
                <form onSubmit={handleWithdraw} className="space-y-6">
                  <div>
                    <label className="block text-white text-sm font-medium mb-2">
                      Select Cryptocurrency
                    </label>
                    <select
                      value={withdrawCryptoCurrency}
                      onChange={(e) => setWithdrawCryptoCurrency(Number(e.target.value))}
                      className="w-full px-4 py-3 bg-darkmode border border-dark_border rounded-lg text-white focus:outline-none focus:border-primary"
                      disabled={cryptocurrencies.length === 0}
                      required
                    >
                      <option value="">Choose a cryptocurrency...</option>
                      {cryptocurrencies.map((crypto) => (
                        <option key={crypto.id} value={crypto.id}>
                          {crypto.name} ({crypto.symbol})
                        </option>
                      ))}
                    </select>
                    {cryptocurrencies.length === 0 && (
                      <p className="text-warning text-sm mt-2">
                        Loading cryptocurrencies...
                      </p>
                    )}
                  </div>
                  
                  <div>
                    <label className="block text-white text-sm font-medium mb-2">
                      Amount
                    </label>
                    <input
                      type="number"
                      step="0.00000001"
                      value={withdrawAmount}
                      onChange={(e) => setWithdrawAmount(e.target.value)}
                      placeholder="Enter amount"
                      className="w-full px-4 py-3 bg-darkmode border border-dark_border rounded-lg text-white focus:outline-none focus:border-primary"
                      required
                    />
                    {withdrawCryptoCurrency && multiCurrencyWallet && (() => {
                      const selectedCrypto = cryptocurrencies.find(c => c.id === withdrawCryptoCurrency);
                      const balance = multiCurrencyWallet.balances.find(b => b.cryptocurrency_symbol === selectedCrypto?.symbol);
                      return balance ? (
                        <p className="text-success text-sm mt-1">
                          Available: {formatCurrency(balance.available_balance)} {selectedCrypto?.symbol}
                        </p>
                      ) : (
                        <p className="text-warning text-sm mt-1">
                          No balance available for {selectedCrypto?.symbol}
                        </p>
                      );
                    })()}
                  </div>
                  
                  <div>
                    <label className="block text-white text-sm font-medium mb-2">
                      Destination Address
                    </label>
                    <input
                      type="text"
                      value={withdrawAddress}
                      onChange={(e) => setWithdrawAddress(e.target.value)}
                      placeholder="Enter wallet address"
                      className="w-full px-4 py-3 bg-darkmode border border-dark_border rounded-lg text-white focus:outline-none focus:border-primary"
                      required
                    />
                  </div>
                  
                  <button
                    type="submit"
                    className="w-full bg-warning text-darkmode py-3 px-6 rounded-lg font-semibold hover:bg-opacity-90 transition-all"
                  >
                    Submit Withdrawal Request
                  </button>
                </form>
                
                <div className="mt-6 p-4 bg-darkmode rounded-lg">
                  <div className="text-warning text-sm">
                    <p>⚠️ Withdrawal Notice:</p>
                    <ul className="list-disc list-inside mt-2 space-y-1">
                      <li>All withdrawals require admin approval</li>
                      <li>Processing time: 1-48 hours</li>
                      <li>Minimum withdrawal: $10.00</li>
                      <li>Double-check your destination address</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

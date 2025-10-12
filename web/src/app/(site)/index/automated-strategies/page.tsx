"use client";

import React, { useState, useEffect, useCallback } from 'react';
import { Icon } from "@iconify/react";
import Link from "next/link";
import { useRouter } from 'next/navigation';
import { authService } from '@/services/authService';
import { apiEndpoint } from '@/config/api';
import OngoingTrades from '@/components/OngoingTrades';

interface TradingPair {
  id: string;
  symbol: string;
  base_currency: string;
  quote_currency: string;
  current_price: number;
  price_change_24h: number;
  volume_24h: number;
  is_active: boolean;
}

interface ChartData {
  timestamp: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

interface Strategy {
  type: 'arbitrage' | 'momentum' | 'grid' | 'mean_reversion' | 'dca';
  name: string;
  description: string;
  risk: 'high' | 'medium' | 'low';
  icon: string;
  color: string;
}

export default function AutomatedStrategiesPage() {
  const router = useRouter();
  const [selectedPair, setSelectedPair] = useState<TradingPair | null>(null);
  const [tradingPairs, setTradingPairs] = useState<TradingPair[]>([]);
  const [chartData, setChartData] = useState<ChartData[]>([]);
  const [userBalance, setUserBalance] = useState(0);
  const [priceSource, setPriceSource] = useState<string>('live');
  const [timeInterval, setTimeInterval] = useState<'seconds' | 'minutes' | 'hours'>('seconds');
  const [entryPrice, setEntryPrice] = useState(0);
  
  // Strategy form states
  const [selectedStrategy, setSelectedStrategy] = useState<Strategy | null>(null);
  const [investmentAmount, setInvestmentAmount] = useState('');
  const [strategyParams, setStrategyParams] = useState({
    interval: '1h',
    gridLevels: '10',
    dcaFrequency: 'daily',
    targetProfit: '5'
  });

  const strategies: Strategy[] = [
    {
      type: 'arbitrage',
      name: 'Arbitrage',
      description: 'Exploit price differences across exchanges',
      risk: 'high',
      icon: 'tabler:arrows-exchange',
      color: '#ef4444'
    },
    {
      type: 'momentum',
      name: 'Momentum',
      description: 'Follow strong price trends',
      risk: 'high',
      icon: 'tabler:trending-up',
      color: '#f59e0b'
    },
    {
      type: 'grid',
      name: 'Grid Trading',
      description: 'Buy low, sell high in ranges',
      risk: 'high',
      icon: 'tabler:grid-dots',
      color: '#3b82f6'
    },
    {
      type: 'mean_reversion',
      name: 'Mean Reversion',
      description: 'Trade on price corrections',
      risk: 'medium',
      icon: 'tabler:chart-line',
      color: '#10b981'
    },
    {
      type: 'dca',
      name: 'DCA (Dollar Cost Average)',
      description: 'Invest fixed amounts regularly',
      risk: 'low',
      icon: 'tabler:calendar',
      color: '#6366f1'
    }
  ];

  // Initial data load (runs once on mount)
  useEffect(() => {
    loadTradingData();
    loadUserBalance();
  }, []);

  // Load chart data when selectedPair or timeInterval changes
  useEffect(() => {
    if (selectedPair) {
      console.log('📊 Loading chart for:', selectedPair.symbol);
      console.log('⏱️ Time interval:', timeInterval);
      loadChartDataFromBackend();
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedPair, timeInterval]);

  // Live price updates based on time interval setting
  useEffect(() => {
    if (!selectedPair) return;
    
    // Determine update frequency based on time interval
    let updateInterval = 2000; // Default: 2 seconds
    switch (timeInterval) {
      case 'seconds':
        updateInterval = 2000; // Update every 2 seconds
        break;
      case 'minutes':
        updateInterval = 60000; // Update every 1 minute
        break;
      case 'hours':
        updateInterval = 3600000; // Update every 1 hour
        break;
    }
    
    const interval = setInterval(() => {
      updateLivePrice();
    }, updateInterval);
    
    return () => clearInterval(interval);
  }, [selectedPair, timeInterval]);

  const loadTradingData = async () => {
    try {
      console.log('📡 Loading trading pairs from backend...');
      const response = await authService.makeAuthenticatedRequest(apiEndpoint('/api/cryptocurrencies/'));
      
      if (response.ok) {
        const data = await response.json();
        console.log('✅ Backend response:', data);
        
        // Handle paginated response (data.results array)
        const cryptoList = data.results || data;
        
        if (!Array.isArray(cryptoList)) {
          console.error('❌ Invalid response format:', data);
          alert('Invalid data format from backend');
          return;
        }
        
        // Transform backend data to TradingPair format
        const pairs: TradingPair[] = cryptoList.map((crypto: any) => ({
          id: `${crypto.symbol}-USDT`,
          symbol: `${crypto.symbol}/USDT`,
          base_currency: crypto.symbol,
          quote_currency: 'USDT',
          current_price: parseFloat(crypto.current_price || 0),
          price_change_24h: parseFloat(crypto.price_change_24h || 0),
          volume_24h: parseFloat(crypto.volume_24h || 0),
          is_active: true
        }));
        
        console.log(`✅ Loaded ${pairs.length} trading pairs from backend`);
        setTradingPairs(pairs);
        
        if (!selectedPair && pairs.length > 0) {
          setSelectedPair(pairs[0]);
          console.log('✅ Selected default pair:', pairs[0].symbol);
        }
      } else {
        console.error('❌ Failed to load trading pairs:', response.status);
        alert('Failed to load trading data from backend. Please refresh the page.');
      }
    } catch (error) {
      console.error('❌ Error loading trading data:', error);
      alert('Failed to connect to backend. Please check your connection.');
    }
  };

  const loadUserBalance = async () => {
    try {
      const response = await authService.makeAuthenticatedRequest(apiEndpoint('/api/balance/'));
      
      if (response.ok) {
        const data = await response.json();
        setUserBalance(data.total_balance_usd || 0);
      } else if (response.status === 401) {
        router.push('/signin');
      }
    } catch (error) {
      console.error('Failed to load balance:', error);
    }
  };

  const loadChartDataFromBackend = useCallback(async () => {
    if (!selectedPair) {
      console.log('⚠️ No selected pair, skipping chart data load');
      return;
    }
    
    try {
      console.log('📊 Loading chart data from backend...');
      console.log(`   Symbol: ${selectedPair.base_currency}`);
      console.log(`   Time interval: ${timeInterval}`);
      
      let limit = 30;
      let interval = 'seconds';
      
      switch (timeInterval) {
        case 'seconds':
          limit = 30;
          interval = 'seconds';
          break;
        case 'minutes':
          limit = 30;
          interval = 'minutes';
          break;
        case 'hours':
          limit = 24;
          interval = 'hours';
          break;
      }
      
      const url = apiEndpoint(`/api/admin/market/combined-chart/?symbol=${selectedPair.base_currency}&limit=${limit}&interval=${interval}`);
      console.log('   API URL:', url);
      
      const response = await authService.makeAuthenticatedRequest(url);
      
      if (response.ok) {
        const data = await response.json();
        console.log('📈 Backend chart data loaded:', data);
        
        if (data.chart_data && data.chart_data.length > 0) {
          setChartData(data.chart_data);
          setPriceSource(data.price_source || 'unknown');
          
          if (data.chart_data.length > 0) {
            setEntryPrice(data.chart_data[0].close);
          }
          
          console.log(`✅ SUCCESS: Loaded ${data.chart_data.length} chart data points from backend (${data.price_source})`);
        } else {
          console.error('❌ Backend returned empty chart_data array');
          setChartData([]);
        }
      } else {
        console.error(`❌ API returned ${response.status}:`, await response.text());
        setChartData([]);
      }
    } catch (error) {
      console.error('❌ Error loading chart data from backend:', error);
      setChartData([]);
    }
  }, [selectedPair, timeInterval]);

  const updateLivePrice = async () => {
    if (!selectedPair) {
      console.log('⚠️ No selected pair for price update');
      return;
    }
    
    try {
      const response = await authService.makeAuthenticatedRequest(
        apiEndpoint(`/api/admin/market/price-auto/?symbol=${selectedPair.base_currency}`)
      );
      
      if (response.ok) {
        const data = await response.json();
        const newPrice = data.price;
        
        console.log(`💹 New price for ${selectedPair.base_currency}: $${newPrice}`);
        
        if (chartData.length > 0) {
          const lastCandle = chartData[chartData.length - 1];
          const newCandle: ChartData = {
            timestamp: new Date().toISOString(),
            open: lastCandle.close,
            high: Math.max(lastCandle.close, newPrice),
            low: Math.min(lastCandle.close, newPrice),
            close: newPrice,
            volume: Math.random() * 500000
          };
          
          console.log('📊 Adding new candle to chart');
          setChartData(prev => [...prev.slice(1), newCandle]);
          
          console.log('💾 Storing data point in backend...');
          await storeDataPointInBackend(newCandle);
        } else {
          console.log('⚠️ Chart data empty, cannot add new candle');
        }
      }
    } catch (error) {
      console.error('❌ Error updating live price:', error);
    }
  };

  const storeDataPointInBackend = async (dataPoint: ChartData) => {
    if (!selectedPair) return;
    
    try {
      await authService.makeAuthenticatedRequest(
        apiEndpoint('/api/admin/market/store-data-point/'),
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            symbol: selectedPair.base_currency,
            timestamp: dataPoint.timestamp,
            open_price: dataPoint.open,
            high_price: dataPoint.high,
            low_price: dataPoint.low,
            close_price: dataPoint.close,
            volume: dataPoint.volume,
            source: priceSource
          })
        }
      );
    } catch (error) {
      console.error('Error storing data point:', error);
    }
  };

  const handleStartStrategy = async () => {
    try {
      if (!selectedStrategy || !selectedPair || !investmentAmount) {
        alert('Please fill in all required fields');
        return;
      }

      const amount = parseFloat(investmentAmount);
      if (isNaN(amount) || amount <= 0) {
        alert('Please enter a valid investment amount');
        return;
      }

      if (amount > userBalance) {
        alert(`Insufficient balance. Available: $${userBalance.toFixed(2)}`);
        return;
      }

      console.log('🚀 Starting automated strategy...');

      // Call backend API to start strategy (using biased trading system)
      const response = await authService.makeAuthenticatedRequest(
        apiEndpoint('/api/trading/execute/'),
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            trade_type: 'buy',
            cryptocurrency: selectedPair.base_currency,
            amount: amount,
            price: selectedPair.current_price,
            leverage: 1,
            strategy_type: selectedStrategy.type,
            strategy_params: strategyParams
          })
        }
      );

      if (response.ok) {
        const result = await response.json();
        console.log('✅ Strategy execution result:', result);

        const outcome = result.outcome?.expected_outcome || 'unknown';
        const outcomeDisplay = outcome === 'win' ? '✅ PROFITABLE' : outcome === 'loss' ? '❌ LOSS' : '⏳ PENDING';
        const pnl = parseFloat(result.pnl || 0);
        const fees = parseFloat(result.fees || 0);
        const finalAmount = amount + pnl - fees;
        const profitLossPercent = ((pnl / amount) * 100).toFixed(2);
        const duration = result.outcome?.duration_seconds || 0;

        alert(
          `${selectedStrategy.name} Strategy Executed!\n\n` +
          `Pair: ${selectedPair.symbol}\n` +
          `Investment: $${amount.toFixed(2)}\n` +
          `Outcome: ${outcomeDisplay}\n` +
          `P&L: $${pnl.toFixed(2)} (${profitLossPercent}%)\n` +
          `Fees: $${fees.toFixed(2)}\n` +
          `Final Amount: $${finalAmount.toFixed(2)}\n` +
          `Duration: ${duration}s\n\n` +
          `✅ Trade completed via admin-controlled biased system\n` +
          `Expected Close: ${result.outcome?.target_close_time || 'N/A'}`
        );

        // Reload balance
        await loadUserBalance();
        setInvestmentAmount('');
      } else if (response.status === 401) {
        alert('Session expired. Please sign in again.');
        router.push('/signin');
      } else {
        const error = await response.json();
        alert(`Failed to start strategy: ${error.error || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Failed to start strategy:', error);
      alert('Failed to start strategy. Please check your connection and try again.');
    }
  };

  const renderLineChart = () => {
    if (chartData.length === 0) return null;
    
    const maxPrice = Math.max(...chartData.map(d => d.close));
    const minPrice = Math.min(...chartData.map(d => d.close));
    let priceRange = maxPrice - minPrice;
    
    // Handle stablecoins or zero price range (add 1% padding)
    if (priceRange === 0 || priceRange < 0.0001) {
      priceRange = maxPrice * 0.01; // 1% of price
      if (priceRange === 0) priceRange = 0.01; // Absolute minimum
    }
    
    const points = chartData.map((point, index) => {
      const x = (index / (chartData.length - 1)) * 800;
      const y = 250 - ((point.close - minPrice) / priceRange) * 200;
      return `${x},${y}`;
    }).join(' ');
    
    const areaPath = `M 0,250 L ${points} L 800,250 Z`;
    
    return (
      <div className="relative h-full">
        <svg width="100%" height="100%" viewBox="0 0 800 250" preserveAspectRatio="none">
          <defs>
            <linearGradient id="strategyGradient" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stopColor="#8b5cf6" stopOpacity="0.8" />
              <stop offset="50%" stopColor="#8b5cf6" stopOpacity="0.4" />
              <stop offset="100%" stopColor="#8b5cf6" stopOpacity="0" />
            </linearGradient>
            <linearGradient id="maGradient" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stopColor="#f59e0b" stopOpacity="0.3" />
              <stop offset="100%" stopColor="#f59e0b" stopOpacity="0" />
            </linearGradient>
          </defs>
          <path
            d={areaPath}
            fill="url(#strategyGradient)"
          />
          <polyline
            points={points}
            fill="none"
            stroke="#8b5cf6"
            strokeWidth="2"
          />
          {/* Moving Average Line */}
          <polyline
            points={chartData.map((point, index) => {
              const x = (index / (chartData.length - 1)) * 800;
              const avgPrice = chartData.slice(Math.max(0, index - 10), index + 1)
                .reduce((sum, d) => sum + d.close, 0) / Math.min(11, index + 1);
              const y = 250 - ((avgPrice - minPrice) / priceRange) * 200;
              return `${x},${y}`;
            }).join(' ')}
            fill="none"
            stroke="#f59e0b"
            strokeWidth="1"
            strokeDasharray="5,5"
          />
        </svg>
      </div>
    );
  };

  const renderVolumeChart = () => {
    if (chartData.length === 0) return null;
    
    const maxVolume = Math.max(...chartData.map(d => d.volume));
    
    return (
      <svg width="100%" height="100%" viewBox="0 0 800 60" preserveAspectRatio="none">
        {chartData.map((point, index) => {
          const x = (index / chartData.length) * 800;
          const barWidth = 800 / chartData.length * 0.8;
          const barHeight = (point.volume / maxVolume) * 60;
          
          return (
            <rect
              key={index}
              x={x}
              y={60 - barHeight}
              width={barWidth}
              height={barHeight}
              fill="#6366f1"
              opacity="0.6"
            />
          );
        })}
      </svg>
    );
  };

  return (
    <div className="min-h-screen bg-darkmode pt-32 pb-16">
      <div className="container mx-auto lg:max-w-screen-2xl px-4">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <Link href="/index" className="text-primary hover:text-primary/80 transition-colors">
              <Icon icon="tabler:arrow-left" width="24" height="24" />
            </Link>
            <div>
              <h1 className="text-white text-3xl font-bold">Automated Trading Strategies</h1>
              <p className="text-muted">AI-Powered • 24/7 Execution • No Human Oversight</p>
            </div>
          </div>
          <div className="bg-dark_grey rounded-lg px-6 py-3">
            <p className="text-muted text-sm">Available Balance</p>
            <p className="text-white text-xl font-bold">${userBalance.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
          </div>
        </div>

        {/* Risk Warning */}
        <div className="bg-gradient-to-r from-warning/10 to-error/10 border border-warning/30 rounded-lg p-4 mb-6">
          <div className="flex items-center gap-3">
            <Icon icon="tabler:robot" width="20" height="20" className="text-warning" />
            <p className="text-muted text-sm">
              🤖 Automated strategies execute without human oversight and can compound losses quickly
            </p>
          </div>
        </div>

        <div className="grid lg:grid-cols-12 gap-6">
          {/* Left Panel - Strategy Selection */}
          <div className="lg:col-span-3 space-y-4">
            <div className="bg-dark_grey rounded-lg p-4">
              <h3 className="text-white font-semibold mb-4">Select Strategy</h3>
              <div className="space-y-2">
                {strategies.map((strategy) => (
                  <button
                    key={strategy.type}
                    onClick={() => setSelectedStrategy(strategy)}
                    className={`w-full text-left p-4 rounded-lg transition-all ${
                      selectedStrategy?.type === strategy.type
                        ? 'bg-primary bg-opacity-20 border border-primary'
                        : 'bg-darkmode hover:bg-darkmode/70'
                    }`}
                  >
                    <div className="flex items-center gap-3 mb-2">
                      <Icon icon={strategy.icon} width="24" height="24" style={{ color: strategy.color }} />
                      <span className="text-white font-medium text-sm">{strategy.name}</span>
                    </div>
                    <p className="text-muted text-xs mb-2">{strategy.description}</p>
                    <span className={`text-xs px-2 py-1 rounded ${
                      strategy.risk === 'high' 
                        ? 'bg-error/20 text-error'
                        : strategy.risk === 'medium'
                        ? 'bg-warning/20 text-warning'
                        : 'bg-success/20 text-success'
                    }`}>
                      {strategy.risk.toUpperCase()} RISK
                    </span>
                  </button>
                ))}
              </div>
            </div>

            <div className="bg-dark_grey rounded-lg p-4">
              <h3 className="text-white font-semibold mb-4">Trading Pairs</h3>
              <div className="space-y-2">
                {tradingPairs.map((pair) => (
                  <button
                    key={pair.id}
                    onClick={() => setSelectedPair(pair)}
                    className={`w-full text-left p-3 rounded-lg transition-all ${
                      selectedPair?.id === pair.id
                        ? 'bg-primary bg-opacity-20 border border-primary'
                        : 'bg-darkmode hover:bg-darkmode/70'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-white font-medium text-sm">{pair.symbol}</span>
                      <span className={`text-xs px-2 py-1 rounded ${
                        pair.price_change_24h >= 0 ? 'bg-success/20 text-success' : 'bg-error/20 text-error'
                      }`}>
                        {pair.price_change_24h >= 0 ? '+' : ''}{pair.price_change_24h.toFixed(2)}%
                      </span>
                    </div>
                    <div className="text-white text-xs">${pair.current_price.toLocaleString()}</div>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Center Panel - Chart & Analysis */}
          <div className="lg:col-span-6 bg-dark_grey rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-white text-2xl font-bold">{selectedPair?.symbol}</h3>
                <p className="text-muted text-sm">Current Price: ${selectedPair?.current_price.toLocaleString()}</p>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-success rounded-full animate-pulse"></div>
                <span className="text-success text-sm">Live Data</span>
              </div>
            </div>
            
            {/* Time Interval Selector */}
            <div className="flex items-center gap-2 mb-4">
              <span className="text-muted text-sm mr-2">Time Interval:</span>
              {(['seconds', 'minutes', 'hours'] as const).map((interval) => (
                <button
                  key={interval}
                  onClick={() => setTimeInterval(interval)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                    timeInterval === interval
                      ? 'bg-primary text-white'
                      : 'bg-darkmode text-muted hover:bg-darkmode/70'
                  }`}
                >
                  {interval.charAt(0).toUpperCase() + interval.slice(1)}
                </button>
              ))}
            </div>

            {/* Price Chart */}
            <div className="bg-darkmode rounded-lg p-4 mb-4">
              <div className="h-64">
                {renderLineChart()}
              </div>
              <div className="flex items-center gap-4 mt-2 text-xs">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-0.5 bg-purple-500"></div>
                  <span className="text-muted">Price</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-0.5 bg-warning" style={{ borderTop: '1px dashed' }}></div>
                  <span className="text-muted">MA (10)</span>
                </div>
              </div>
            </div>

            {/* Volume Chart */}
            <div className="bg-darkmode rounded-lg p-4 mb-4">
              <h4 className="text-muted text-sm mb-2">Volume</h4>
              <div className="h-16">
                {renderVolumeChart()}
              </div>
            </div>

            {/* Strategy Performance Indicators */}
            <div className="grid grid-cols-4 gap-4">
              <div className="bg-darkmode rounded-lg p-3">
                <p className="text-muted text-xs mb-1">24h Volume</p>
                <p className="text-white font-bold text-sm">${(selectedPair?.volume_24h || 0 / 1000).toFixed(0)}K</p>
              </div>
              <div className="bg-darkmode rounded-lg p-3">
                <p className="text-muted text-xs mb-1">Volatility</p>
                <p className="text-warning font-bold text-sm">Medium</p>
              </div>
              <div className="bg-darkmode rounded-lg p-3">
                <p className="text-muted text-xs mb-1">Trend</p>
                <p className="text-success font-bold text-sm">Bullish</p>
              </div>
              <div className="bg-darkmode rounded-lg p-3">
                <p className="text-muted text-xs mb-1">Signal</p>
                <p className="text-primary font-bold text-sm">Buy</p>
              </div>
            </div>
          </div>

          {/* Right Panel - Strategy Configuration */}
          <div className="lg:col-span-3 bg-dark_grey rounded-lg p-6">
            <h3 className="text-white font-semibold mb-4">Configure Strategy</h3>
            
            {selectedStrategy ? (
              <>
                <div className="mb-6 p-4 rounded-lg" style={{ backgroundColor: `${selectedStrategy.color}20`, border: `1px solid ${selectedStrategy.color}40` }}>
                  <div className="flex items-center gap-3 mb-2">
                    <Icon icon={selectedStrategy.icon} width="32" height="32" style={{ color: selectedStrategy.color }} />
                    <div>
                      <h4 className="text-white font-semibold">{selectedStrategy.name}</h4>
                      <p className="text-muted text-xs">{selectedStrategy.description}</p>
                    </div>
                  </div>
                </div>

                {/* Investment Amount */}
                <div className="mb-4">
                  <label className="text-muted text-sm mb-2 block">Investment Amount (USD)</label>
                  <input
                    type="number"
                    value={investmentAmount}
                    onChange={(e) => setInvestmentAmount(e.target.value)}
                    className="w-full bg-darkmode border border-dark_border rounded-lg px-4 py-3 text-white focus:outline-none focus:border-primary"
                    placeholder="0.00"
                  />
                </div>

                {/* Strategy-specific Parameters */}
                {selectedStrategy.type === 'grid' && (
                  <div className="mb-4">
                    <label className="text-muted text-sm mb-2 block">Grid Levels</label>
                    <input
                      type="number"
                      value={strategyParams.gridLevels}
                      onChange={(e) => setStrategyParams({...strategyParams, gridLevels: e.target.value})}
                      className="w-full bg-darkmode border border-dark_border rounded-lg px-4 py-3 text-white focus:outline-none focus:border-primary"
                    />
                  </div>
                )}

                {selectedStrategy.type === 'dca' && (
                  <div className="mb-4">
                    <label className="text-muted text-sm mb-2 block">Frequency</label>
                    <select
                      value={strategyParams.dcaFrequency}
                      onChange={(e) => setStrategyParams({...strategyParams, dcaFrequency: e.target.value})}
                      className="w-full bg-darkmode border border-dark_border rounded-lg px-4 py-3 text-white focus:outline-none focus:border-primary"
                    >
                      <option value="hourly">Hourly</option>
                      <option value="daily">Daily</option>
                      <option value="weekly">Weekly</option>
                    </select>
                  </div>
                )}

                <div className="mb-4">
                  <label className="text-muted text-sm mb-2 block">Update Interval</label>
                  <select
                    value={strategyParams.interval}
                    onChange={(e) => setStrategyParams({...strategyParams, interval: e.target.value})}
                    className="w-full bg-darkmode border border-dark_border rounded-lg px-4 py-3 text-white focus:outline-none focus:border-primary"
                  >
                    <option value="1m">1 Minute</option>
                    <option value="5m">5 Minutes</option>
                    <option value="15m">15 Minutes</option>
                    <option value="1h">1 Hour</option>
                    <option value="4h">4 Hours</option>
                  </select>
                </div>

                <div className="mb-4">
                  <label className="text-muted text-sm mb-2 block">Target Profit %</label>
                  <input
                    type="number"
                    value={strategyParams.targetProfit}
                    onChange={(e) => setStrategyParams({...strategyParams, targetProfit: e.target.value})}
                    className="w-full bg-darkmode border border-dark_border rounded-lg px-4 py-3 text-white focus:outline-none focus:border-primary"
                    placeholder="5"
                  />
                </div>

                {/* Risk Warning */}
                <div className={`mb-4 p-3 rounded-lg ${
                  selectedStrategy.risk === 'high'
                    ? 'bg-error/10 border border-error/20'
                    : selectedStrategy.risk === 'medium'
                    ? 'bg-warning/10 border border-warning/20'
                    : 'bg-success/10 border border-success/20'
                }`}>
                  <p className={`text-xs ${
                    selectedStrategy.risk === 'high'
                      ? 'text-error'
                      : selectedStrategy.risk === 'medium'
                      ? 'text-warning'
                      : 'text-success'
                  }`}>
                    ⚠️ {selectedStrategy.risk.toUpperCase()} RISK: This strategy executes automatically and can result in significant losses.
                  </p>
                </div>

                {/* Start Strategy Button */}
                <button
                  onClick={handleStartStrategy}
                  className="w-full py-4 rounded-lg font-semibold transition-all bg-gradient-to-r from-primary to-purple-600 hover:opacity-90 text-white mb-3"
                >
                  Start Automated Strategy
                </button>

                {/* Expected Returns */}
                <div className="bg-darkmode rounded-lg p-4">
                  <p className="text-muted text-xs mb-2">Estimated Returns</p>
                  <div className="flex items-center justify-between">
                    <span className="text-white text-sm">Daily</span>
                    <span className="text-success font-bold">+2-5%</span>
                  </div>
                  <div className="flex items-center justify-between mt-1">
                    <span className="text-white text-sm">Monthly</span>
                    <span className="text-success font-bold">+30-50%</span>
                  </div>
                  <p className="text-muted text-xs mt-2">* Past performance does not guarantee future results</p>
                </div>
              </>
            ) : (
              <div className="text-center py-12">
                <Icon icon="tabler:robot" width="48" height="48" className="text-muted mx-auto mb-4" />
                <p className="text-muted">Select a strategy to configure</p>
              </div>
            )}
          </div>
        </div>
      </div>
      
      {/* Ongoing Trades Section */}
      <div className="container mx-auto max-w-7xl px-4 mt-8">
        <OngoingTrades />
      </div>
    </div>
  );
}
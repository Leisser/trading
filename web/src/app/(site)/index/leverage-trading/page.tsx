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

export default function LeverageTradingPage() {
  const router = useRouter();
  const [selectedPair, setSelectedPair] = useState<TradingPair | null>(null);
  const [tradingPairs, setTradingPairs] = useState<TradingPair[]>([]);
  const [chartData, setChartData] = useState<ChartData[]>([]);
  const [userBalance, setUserBalance] = useState(0);
  const [priceSource, setPriceSource] = useState<string>('live');
  const [timeInterval, setTimeInterval] = useState<'seconds' | 'minutes' | 'hours'>('seconds');
  const [entryPrice, setEntryPrice] = useState(0);
  
  // Order form states
  const [orderSide, setOrderSide] = useState<'buy' | 'sell'>('buy');
  const [orderAmount, setOrderAmount] = useState('');
  const [leverage, setLeverage] = useState(1);
  const [takeProfitPrice, setTakeProfitPrice] = useState('');
  const [stopLossPrice, setStopLossPrice] = useState('');

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

  const handlePlaceLeverageOrder = async () => {
    try {
      if (!selectedPair || !orderAmount) {
        alert('Please fill in all required fields');
        return;
      }

      const amount = parseFloat(orderAmount);
      if (isNaN(amount) || amount <= 0) {
        alert('Please enter a valid order amount');
        return;
      }

      if (amount > userBalance) {
        alert(`Insufficient balance. Available: $${userBalance.toFixed(2)}`);
        return;
      }

      const positionSize = amount * leverage;
      const liquidationPrice = orderSide === 'buy'
        ? (selectedPair.current_price * (1 - (1 / leverage)))
        : (selectedPair.current_price * (1 + (1 / leverage)));

      console.log('🚀 Placing leverage order...');

      // Call backend API to place leverage order (using biased trading system)
      const response = await authService.makeAuthenticatedRequest(
        apiEndpoint('/api/trading/execute/'),
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            trade_type: orderSide === 'buy' ? 'buy' : 'sell',
            cryptocurrency: selectedPair.base_currency,
            amount: amount,
            price: selectedPair.current_price,
            leverage: leverage,
            take_profit: takeProfitPrice ? parseFloat(takeProfitPrice) : null,
            stop_loss: stopLossPrice ? parseFloat(stopLossPrice) : null,
            liquidation_price: liquidationPrice
          })
        }
      );

      if (response.ok) {
        const result = await response.json();
        console.log('✅ Leverage order result:', result);

        const outcome = result.outcome?.expected_outcome || 'unknown';
        const outcomeDisplay = outcome === 'win' ? '✅ PROFITABLE' : outcome === 'loss' ? '❌ LOSS' : '⏳ PENDING';
        const pnl = parseFloat(result.pnl || 0);
        const fees = parseFloat(result.fees || 0);
        const finalAmount = amount + pnl - fees;
        const profitLossPercent = ((pnl / amount) * 100).toFixed(2);
        const duration = result.outcome?.duration_seconds || 0;

        alert(
          `Leverage Order Executed!\n\n` +
          `Pair: ${selectedPair.symbol}\n` +
          `Side: ${orderSide.toUpperCase()}\n` +
          `Leverage: ${leverage}x\n` +
          `Margin: $${amount.toFixed(2)}\n` +
          `Position Size: $${positionSize.toFixed(2)}\n\n` +
          `Outcome: ${outcomeDisplay}\n` +
          `P&L: $${pnl.toFixed(2)} (${profitLossPercent}%)\n` +
          `Fees: $${fees.toFixed(2)}\n` +
          `Final Amount: $${finalAmount.toFixed(2)}\n` +
          `Duration: ${duration}s\n\n` +
          `Liquidation Price: $${liquidationPrice.toFixed(2)}\n` +
          `Expected Close: ${result.outcome?.target_close_time || 'N/A'}\n\n` +
          `✅ Trade completed via admin-controlled biased system`
        );

        // Reload balance
        await loadUserBalance();
        setOrderAmount('');
        setTakeProfitPrice('');
        setStopLossPrice('');
      } else if (response.status === 401) {
        alert('Session expired. Please sign in again.');
        router.push('/signin');
      } else {
        const error = await response.json();
        alert(`Failed to place order: ${error.error || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Failed to place order:', error);
      alert('Failed to place order. Please check your connection and try again.');
    }
  };

  const calculateProfitLoss = () => {
    if (!selectedPair || !orderAmount) return { profit: 0, loss: 0, percentage: 0 };
    
    const investment = parseFloat(orderAmount);
    const priceChange = selectedPair.current_price * 0.01; // 1% change
    const profit = investment * leverage * (priceChange / selectedPair.current_price);
    const profitPercentage = (profit / investment) * 100;
    
    return {
      profit: Math.abs(profit),
      loss: Math.abs(profit),
      percentage: Math.abs(profitPercentage)
    };
  };

  const renderCandlestickChart = () => {
    const maxPrice = Math.max(...chartData.map(d => d.high));
    const minPrice = Math.min(...chartData.map(d => d.low));
    let priceRange = maxPrice - minPrice;
    
    // Debug: Log chart data for troubleshooting
    console.log('📊 Candlestick Chart Debug:', {
      symbol: selectedPair,
      dataPoints: chartData.length,
      maxPrice,
      minPrice,
      priceRange,
      sampleData: chartData.slice(0, 3)
    });
    
    // Handle stablecoins or zero price range (add 1% padding)
    if (priceRange === 0 || priceRange < 0.0001) {
      priceRange = maxPrice * 0.01; // 1% of price
      if (priceRange === 0) priceRange = 0.01; // Absolute minimum
      console.log('🔧 Zero range detected, using padding:', priceRange);
    }
    
    return (
      <div className="relative h-full">
        <svg width="100%" height="100%" viewBox="0 0 900 350" preserveAspectRatio="none">
          {/* Background gradient */}
          <defs>
            <linearGradient id="chartBackground" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stopColor="#1f2937" />
              <stop offset="100%" stopColor="#111827" />
            </linearGradient>
          </defs>
          <rect width="900" height="350" fill="url(#chartBackground)" />
          
          {/* Grid lines */}
          {[0, 25, 50, 75, 100].map((pct) => (
            <line
              key={pct}
              x1="0"
              y1={(pct / 100) * 350}
              x2="900"
              y2={(pct / 100) * 350}
              stroke={pct === 50 ? "#4b5563" : "#374151"}
              strokeWidth={pct === 50 ? "1" : "0.5"}
              strokeDasharray={pct === 50 ? "none" : "5,5"}
              opacity="0.6"
            />
          ))}
          
          {/* Vertical grid lines for time periods */}
          {chartData.map((_, index) => {
            if (index % Math.max(1, Math.floor(chartData.length / 10)) === 0) {
              const x = (index / chartData.length) * 900;
              return (
                <line
                  key={`v-${index}`}
                  x1={x}
                  y1="0"
                  x2={x}
                  y2="350"
                  stroke="#374151"
                  strokeWidth="0.5"
                  strokeDasharray="5,5"
                  opacity="0.3"
                />
              );
            }
            return null;
          })}
          
          {chartData.map((candle, index) => {
            const x = (index / chartData.length) * 900;
            const candleWidth = Math.max(2, 900 / chartData.length * 0.8); // Minimum width of 2px
            const centerX = x + candleWidth / 2;
            
            const openY = 350 - ((candle.open - minPrice) / priceRange) * 350;
            const closeY = 350 - ((candle.close - minPrice) / priceRange) * 350;
            const highY = 350 - ((candle.high - minPrice) / priceRange) * 350;
            const lowY = 350 - ((candle.low - minPrice) / priceRange) * 350;
            
            const isGreen = candle.close > candle.open;
            const color = isGreen ? '#10b981' : '#ef4444';
            const bodyTop = Math.min(openY, closeY);
            const bodyHeight = Math.max(1, Math.abs(closeY - openY)); // Minimum height of 1px
            
            return (
              <g key={index}>
                {/* Wick (high-low line) */}
                <line
                  x1={centerX}
                  y1={highY}
                  x2={centerX}
                  y2={lowY}
                  stroke={color}
                  strokeWidth="1"
                  opacity="0.8"
                />
                
                {/* Body */}
                <rect
                  x={x + 1}
                  y={bodyTop}
                  width={candleWidth - 2}
                  height={bodyHeight}
                  fill={isGreen ? color : 'transparent'}
                  stroke={color}
                  strokeWidth="1"
                  rx="1"
                  ry="1"
                />
                
                {/* Open/Close ticks for better visibility */}
                {candleWidth > 4 && (
                  <>
                    {/* Open tick */}
                    <line
                      x1={x}
                      y1={openY}
                      x2={x + 2}
                      y2={openY}
                      stroke={color}
                      strokeWidth="1.5"
                    />
                    {/* Close tick */}
                    <line
                      x1={x + candleWidth - 2}
                      y1={closeY}
                      x2={x + candleWidth}
                      y2={closeY}
                      stroke={color}
                      strokeWidth="1.5"
                    />
                  </>
                )}
              </g>
            );
          })}
          
          {/* Price labels on the right */}
          <g className="price-labels">
            {[0, 25, 50, 75, 100].map((pct) => {
              const price = minPrice + (priceRange * (100 - pct) / 100);
              const y = (pct / 100) * 350;
              return (
                <text
                  key={pct}
                  x="905"
                  y={y + 5}
                  fontSize="12"
                  fill="#9ca3af"
                  textAnchor="start"
                >
                  ${price.toFixed(2)}
                </text>
              );
            })}
          </g>
          
          {/* Current price indicator */}
          {chartData.length > 0 && (
            <g className="current-price">
              <line
                x1="0"
                y1={350 - ((chartData[chartData.length - 1].close - minPrice) / priceRange) * 350}
                x2="900"
                y2={350 - ((chartData[chartData.length - 1].close - minPrice) / priceRange) * 350}
                stroke="#f59e0b"
                strokeWidth="1"
                strokeDasharray="3,3"
                opacity="0.7"
              />
              <text
                x="905"
                y={350 - ((chartData[chartData.length - 1].close - minPrice) / priceRange) * 350 + 5}
                fontSize="12"
                fill="#f59e0b"
                fontWeight="bold"
              >
                ${chartData[chartData.length - 1].close.toFixed(2)}
              </text>
            </g>
          )}
        </svg>
      </div>
    );
  };

  const pnl = calculateProfitLoss();

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
              <h1 className="text-white text-3xl font-bold">Leverage Trading</h1>
              <p className="text-muted">Up to 100x Leverage • Amplified Profits & Losses</p>
            </div>
          </div>
          <div className="bg-dark_grey rounded-lg px-6 py-3">
            <p className="text-muted text-sm">Available Balance</p>
            <p className="text-white text-xl font-bold">${userBalance.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
          </div>
        </div>

        {/* Risk Warning */}
        <div className="bg-gradient-to-r from-success/10 to-error/10 border border-error/30 rounded-lg p-4 mb-6">
          <div className="flex items-center gap-3">
            <Icon icon="tabler:flame" width="20" height="20" className="text-error" />
            <p className="text-muted text-sm">
              💥 EXTREME RISK: Leverage trading can result in total loss of your position. A 1% price move with 100x leverage = 100% profit or loss!
            </p>
          </div>
        </div>

        <div className="grid lg:grid-cols-12 gap-6">
          {/* Left Panel - Trading Pairs */}
          <div className="lg:col-span-3 bg-dark_grey rounded-lg p-4">
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
                    <span className="text-white font-medium">{pair.symbol}</span>
                    <span className={`text-xs px-2 py-1 rounded ${
                      pair.price_change_24h >= 0 ? 'bg-success/20 text-success' : 'bg-error/20 text-error'
                    }`}>
                      {pair.price_change_24h >= 0 ? '+' : ''}{pair.price_change_24h.toFixed(2)}%
                    </span>
                  </div>
                  <div className="text-white text-sm">${pair.current_price.toLocaleString()}</div>
                  <div className="text-muted text-xs">Vol: ${(pair.volume_24h / 1000).toFixed(0)}K</div>
                </button>
              ))}
            </div>

            {/* Leverage Quick Info */}
            <div className="mt-6 space-y-2">
              <div className="bg-success/10 border border-success/20 rounded-lg p-3">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-success text-xs font-semibold">1x</span>
                  <span className="text-muted text-xs">Normal</span>
                </div>
                <div className="text-white text-xs">1% move = 1% P/L</div>
              </div>
              <div className="bg-warning/10 border border-warning/20 rounded-lg p-3">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-warning text-xs font-semibold">10x</span>
                  <span className="text-muted text-xs">High Risk</span>
                </div>
                <div className="text-white text-xs">1% move = 10% P/L</div>
              </div>
              <div className="bg-error/10 border border-error/20 rounded-lg p-3">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-error text-xs font-semibold">100x</span>
                  <span className="text-muted text-xs">Extreme</span>
                </div>
                <div className="text-white text-xs">1% move = 100% P/L</div>
              </div>
            </div>
          </div>

          {/* Center Panel - Chart */}
          <div className="lg:col-span-6 bg-dark_grey rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-white text-2xl font-bold">{selectedPair?.symbol}</h3>
                <p className="text-muted text-sm">Current Price: ${selectedPair?.current_price.toLocaleString()}</p>
              </div>
              <div className={`px-3 py-2 rounded-lg ${
                selectedPair && selectedPair.price_change_24h >= 0
                  ? 'bg-success/20 text-success'
                  : 'bg-error/20 text-error'
              }`}>
                <span className="font-bold">
                  {selectedPair && selectedPair.price_change_24h >= 0 ? '+' : ''}
                  {selectedPair?.price_change_24h.toFixed(2)}%
                </span>
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
              <div className="ml-auto flex items-center gap-2">
                <div className="w-2 h-2 bg-success rounded-full animate-pulse"></div>
                <span className="text-success text-xs">Live</span>
              </div>
            </div>

            <div className="bg-darkmode rounded-lg p-4 mb-4">
              <div className="h-96">
                {renderCandlestickChart()}
              </div>
            </div>

            {/* Leverage P/L Calculator */}
            <div className="bg-gradient-to-r from-primary/10 to-success/10 border border-primary/30 rounded-lg p-6">
              <h4 className="text-white font-semibold mb-4">Profit/Loss Calculator (1% Price Move)</h4>
              <div className="grid grid-cols-3 gap-4">
                <div className="bg-darkmode/50 rounded-lg p-4">
                  <p className="text-muted text-xs mb-2">1x Leverage</p>
                  <p className="text-success text-lg font-bold">+${pnl.profit.toFixed(2)}</p>
                  <p className="text-error text-lg font-bold">-${pnl.loss.toFixed(2)}</p>
                </div>
                <div className="bg-darkmode/50 rounded-lg p-4">
                  <p className="text-muted text-xs mb-2">10x Leverage</p>
                  <p className="text-success text-lg font-bold">+${(pnl.profit * 10).toFixed(2)}</p>
                  <p className="text-error text-lg font-bold">-${(pnl.loss * 10).toFixed(2)}</p>
                </div>
                <div className="bg-darkmode/50 rounded-lg p-4">
                  <p className="text-muted text-xs mb-2">100x Leverage</p>
                  <p className="text-success text-lg font-bold">+${(pnl.profit * 100).toFixed(2)}</p>
                  <p className="text-error text-lg font-bold">-${(pnl.loss * 100).toFixed(2)}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Right Panel - Order Form */}
          <div className="lg:col-span-3 bg-dark_grey rounded-lg p-6">
            <h3 className="text-white font-semibold mb-4">Place Leverage Order</h3>
            
            {/* Buy/Sell Selection */}
            <div className="grid grid-cols-2 gap-2 mb-4">
              <button
                onClick={() => setOrderSide('buy')}
                className={`py-3 rounded-lg font-medium transition-all ${
                  orderSide === 'buy'
                    ? 'bg-success text-white'
                    : 'bg-darkmode text-muted hover:text-white'
                }`}
              >
                Long (Buy)
              </button>
              <button
                onClick={() => setOrderSide('sell')}
                className={`py-3 rounded-lg font-medium transition-all ${
                  orderSide === 'sell'
                    ? 'bg-error text-white'
                    : 'bg-darkmode text-muted hover:text-white'
                }`}
              >
                Short (Sell)
              </button>
            </div>

            {/* Leverage Selector */}
            <div className="mb-4">
              <div className="flex items-center justify-between mb-2">
                <label className="text-muted text-sm">Leverage</label>
                <span className={`text-lg font-bold ${
                  leverage >= 50 ? 'text-error' : leverage >= 10 ? 'text-warning' : 'text-success'
                }`}>
                  {leverage}x
                </span>
              </div>
              <input
                type="range"
                min="1"
                max="100"
                value={leverage}
                onChange={(e) => setLeverage(parseInt(e.target.value))}
                className="w-full h-2 bg-darkmode rounded-lg appearance-none cursor-pointer"
              />
              <div className="flex justify-between mt-2">
                {[1, 10, 25, 50, 100].map((lev) => (
                  <button
                    key={lev}
                    onClick={() => setLeverage(lev)}
                    className={`text-xs px-2 py-1 rounded ${
                      leverage === lev
                        ? 'bg-primary text-white'
                        : 'text-muted hover:text-white'
                    }`}
                  >
                    {lev}x
                  </button>
                ))}
              </div>
            </div>

            {/* Amount */}
            <div className="mb-4">
              <label className="text-muted text-sm mb-2 block">Margin Amount (USD)</label>
              <input
                type="number"
                value={orderAmount}
                onChange={(e) => setOrderAmount(e.target.value)}
                className="w-full bg-darkmode border border-dark_border rounded-lg px-4 py-3 text-white focus:outline-none focus:border-primary"
                placeholder="0.00"
              />
              <p className="text-muted text-xs mt-1">
                Position Size: ${(parseFloat(orderAmount || '0') * leverage).toLocaleString()}
              </p>
            </div>

            {/* Take Profit */}
            <div className="mb-4">
              <label className="text-muted text-sm mb-2 block">Take Profit Price (Optional)</label>
              <input
                type="number"
                value={takeProfitPrice}
                onChange={(e) => setTakeProfitPrice(e.target.value)}
                className="w-full bg-darkmode border border-dark_border rounded-lg px-4 py-3 text-white focus:outline-none focus:border-primary"
                placeholder={selectedPair ? `> ${selectedPair.current_price}` : '0.00'}
              />
            </div>

            {/* Stop Loss */}
            <div className="mb-4">
              <label className="text-muted text-sm mb-2 block">Stop Loss Price (Optional)</label>
              <input
                type="number"
                value={stopLossPrice}
                onChange={(e) => setStopLossPrice(e.target.value)}
                className="w-full bg-darkmode border border-dark_border rounded-lg px-4 py-3 text-white focus:outline-none focus:border-primary"
                placeholder={selectedPair ? `< ${selectedPair.current_price}` : '0.00'}
              />
            </div>

            {/* Liquidation Warning */}
            {selectedPair && orderAmount && (
              <div className="mb-4 p-4 bg-error/10 border border-error/20 rounded-lg">
                <p className="text-error text-xs font-semibold mb-1">Liquidation Price</p>
                <p className="text-white text-lg font-bold">
                  ${(orderSide === 'buy'
                    ? (selectedPair.current_price * (1 - (1 / leverage)))
                    : (selectedPair.current_price * (1 + (1 / leverage)))
                  ).toFixed(2)}
                </p>
                <p className="text-muted text-xs mt-1">
                  Your position will be liquidated if price reaches this level
                </p>
              </div>
            )}

            {/* Place Order Button */}
            <button
              onClick={handlePlaceLeverageOrder}
              className={`w-full py-4 rounded-lg font-semibold transition-all mb-3 ${
                orderSide === 'buy'
                  ? 'bg-gradient-to-r from-success to-green-600 hover:opacity-90 text-white'
                  : 'bg-gradient-to-r from-error to-red-600 hover:opacity-90 text-white'
              }`}
            >
              Open {orderSide === 'buy' ? 'Long' : 'Short'} Position {leverage}x
            </button>

            {/* Risk Warning */}
            <div className={`p-3 rounded-lg ${
              leverage >= 50
                ? 'bg-error/10 border border-error/20'
                : leverage >= 10
                ? 'bg-warning/10 border border-warning/20'
                : 'bg-success/10 border border-success/20'
            }`}>
              <p className={`text-xs ${
                leverage >= 50 ? 'text-error' : leverage >= 10 ? 'text-warning' : 'text-success'
              }`}>
                {leverage >= 50 && '🔥 EXTREME RISK: Position can be liquidated with <2% price move'}
                {leverage >= 10 && leverage < 50 && '⚠️ HIGH RISK: Position can be liquidated with <10% price move'}
                {leverage < 10 && '✅ MODERATE RISK: Trade within your limits'}
              </p>
            </div>
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
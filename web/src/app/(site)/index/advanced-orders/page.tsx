"use client";

import React, { useState, useEffect, useCallback } from 'react';
import { Icon } from "@iconify/react";
import Link from "next/link";
import { useRouter } from 'next/navigation';
import { useMarketWebSocket } from '@/hooks/useMarketWebSocket';
import { useTradeWebSocket } from '@/hooks/useTradeWebSocket';
import { authService } from '@/services/authService';
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

export default function AdvancedOrdersPage() {
  const router = useRouter();
  const [selectedPair, setSelectedPair] = useState<TradingPair | null>(null);
  const [tradingPairs, setTradingPairs] = useState<TradingPair[]>([]);
  const [chartData, setChartData] = useState<ChartData[]>([]);
  const [chartType, setChartType] = useState<'candlestick' | 'line'>('candlestick');
  const [timeInterval, setTimeInterval] = useState<'seconds' | 'minutes' | 'hours'>('seconds');
  const [userBalance, setUserBalance] = useState(0);
  
  // Order form states
  const [orderType, setOrderType] = useState<'stop_loss' | 'trailing_stop' | 'stop_limit'>('stop_loss');
  const [orderSide, setOrderSide] = useState<'buy' | 'sell'>('buy');
  const [orderAmount, setOrderAmount] = useState('');
  const [stopPrice, setStopPrice] = useState('');
  const [limitPrice, setLimitPrice] = useState('');
  const [trailingPercent, setTrailingPercent] = useState('5');
  const [leverage, setLeverage] = useState(1);
  const [lastUpdateTime, setLastUpdateTime] = useState<string>('');
  const [priceFlash, setPriceFlash] = useState(false);
  const [entryPrice, setEntryPrice] = useState<number | null>(null);
  
  // Strategy states
  const [strategyType, setStrategyType] = useState('hold');
  const [targetPrice, setTargetPrice] = useState('');
  const [strategyAmount, setStrategyAmount] = useState('');
  const [strategyLeverage, setStrategyLeverage] = useState(1);
  const [strategyPairs, setStrategyPairs] = useState<any[]>([]);
  const [newDataAnimation, setNewDataAnimation] = useState(false);
  
  // Load strategy pairs from localStorage on component mount
  useEffect(() => {
    const savedStrategies = localStorage.getItem('strategyPairs');
    if (savedStrategies) {
      try {
        const parsedStrategies = JSON.parse(savedStrategies);
        setStrategyPairs(parsedStrategies);
      } catch (error) {
        console.error('Failed to parse saved strategies:', error);
      }
    }
  }, []);
  
  // Save strategy pairs to localStorage whenever they change
  useEffect(() => {
    if (strategyPairs.length > 0) {
      localStorage.setItem('strategyPairs', JSON.stringify(strategyPairs));
    }
  }, [strategyPairs]);
  const [priceSource, setPriceSource] = useState<'real' | 'simulated' | 'live' | 'unknown'>('unknown');
  
  // WebSocket for live market data
  const { marketData, isConnected } = useMarketWebSocket({
    symbol: selectedPair?.base_currency || 'BTC',
    enabled: true
  });

  // WebSocket for live trade updates
  const { lastUpdate: tradeUpdate, isConnected: isTradeConnected } = useTradeWebSocket();

  // Handle trade updates from WebSocket
  useEffect(() => {
    if (tradeUpdate) {
      if (tradeUpdate.type === 'trade_update') {
        // Update strategy pair with new trade_sum and price
        setStrategyPairs(prev => prev.map(sp => {
          if (sp.id === tradeUpdate.trade_id?.toString()) {
            return {
              ...sp,
              tradeSum: tradeUpdate.trade_sum || sp.tradeSum,
              currentPrice: parseFloat(tradeUpdate.current_price || sp.currentPrice),
              pnl: parseFloat(tradeUpdate.pnl || sp.pnl),
              lastUpdate: tradeUpdate.timestamp || new Date().toISOString()
            };
          }
          return sp;
        }));
      } else if (tradeUpdate.type === 'trade_completed') {
        // Mark strategy as completed
        setStrategyPairs(prev => prev.map(sp => {
          if (sp.id === tradeUpdate.trade_id?.toString()) {
            return {
              ...sp,
              status: 'completed',
              tradeSum: 0,
              lastUpdate: tradeUpdate.timestamp || new Date().toISOString()
            };
          }
          return sp;
        }));
      } else if (tradeUpdate.type === 'balance_update') {
        // Balance was updated (e.g., trade stopped)
        console.log(`💰 Balance updated: ${tradeUpdate.balance} ${tradeUpdate.currency}`);
        if (tradeUpdate.reason === 'trade_stopped') {
          alert(`Trade stopped. ${tradeUpdate.amount_returned} USDT returned to your balance.`);
        }
      }
    }
  }, [tradeUpdate]);

  useEffect(() => {
    loadTradingData();
    loadUserBalance();
    loadChartDataFromBackend();
  }, [selectedPair]);
  
  // Callback for live price updates from backend
  const updateLivePrice = useCallback(async () => {
    console.log('🔄 Fetching live price from backend...');
    
    try {
      const token = authService.getAccessToken();
      if (!token || !selectedPair) return;
      
      // Fetch current price from backend (auto-switches between real/simulated based on admin settings)
      const response = await authService.makeAuthenticatedRequest(`http://localhost:8000/api/admin/market/price-auto/?symbol=${selectedPair.base_currency}`);
      
      if (!response.ok) {
        console.error('Failed to fetch price');
        return;
      }
      
      const data = await response.json();
      console.log('📊 Backend price data:', data);
      console.log(`🌐 Price source: ${data.source?.toUpperCase() || 'UNKNOWN'}`);
      
      // Update price source indicator
      setPriceSource(data.source || 'unknown');
      
      // Set last update time
      const now = new Date();
      setLastUpdateTime(now.toLocaleTimeString());
      
      // Trigger price flash animation
      setPriceFlash(true);
      setTimeout(() => setPriceFlash(false), 500);
      
      // Trigger new data animation
      setNewDataAnimation(true);
      setTimeout(() => setNewDataAnimation(false), 1000);
      
      // Update chart with new data point
      setChartData(prev => {
        if (prev.length === 0) return prev;
        
        const lastCandle = prev[prev.length - 1];
        const newPrice = data.price;
        
        const newCandle: ChartData = {
          timestamp: data.timestamp,
          open: lastCandle.close,
          high: Math.max(lastCandle.close, newPrice) * 1.003,
          low: Math.min(lastCandle.close, newPrice) * 0.997,
          close: newPrice,
          volume: Math.random() * 500000
        };
        
        // Store the new data point in backend
        storeDataPointInBackend(newCandle, data.source);
        
        console.log('📈 New price from backend:', newPrice.toFixed(2));
        if (data.change_from_entry) {
          console.log('📊 Change from entry:', data.change_from_entry.toFixed(2) + '%');
        }
        
        return [...prev.slice(-29), newCandle];
      });
      
      // Update current price
      setSelectedPair(prev => {
        if (!prev) return null;
        return {
          ...prev,
          current_price: data.price,
          price_change_24h: data.change_from_entry || prev.price_change_24h
        };
      });
      
    } catch (error) {
      console.error('❌ Error updating price:', error);
    }
  }, [selectedPair]);
  
  // Separate effect for live price updates
  useEffect(() => {
    if (!selectedPair) return;
    
    console.log('⏰ Starting live price updates every 2 seconds...');
    
    // Poll for price updates every 2 seconds (faster for more visible updates)
    const interval = setInterval(() => {
      updateLivePrice();
    }, 2000);
    
    return () => {
      console.log('🛑 Stopping live price updates');
      clearInterval(interval);
    };
  }, [selectedPair, updateLivePrice]);
  
  // Update chart data when WebSocket data arrives
  useEffect(() => {
    if (marketData && selectedPair) {
      console.log('📊 Updating chart from WebSocket:', marketData);
      
      // Trigger new data animation
      setNewDataAnimation(true);
      setTimeout(() => setNewDataAnimation(false), 1000);
      
      const newCandle: ChartData = {
        timestamp: marketData.timestamp,
        open: marketData.open,
        high: marketData.high,
        low: marketData.low,
        close: marketData.close,
        volume: marketData.volume
      };
      
      // Add new candle and keep last 30 candles
      setChartData(prev => [...prev.slice(-29), newCandle]);
      
      // Update selected pair price
      setSelectedPair(prev => prev ? {...prev, current_price: marketData.close, price_change_24h: marketData.change_24h} : null);
    }
  }, [marketData]);

  const loadTradingData = async () => {
    const mockPairs: TradingPair[] = [
      {
        id: 'BTC-USD',
        symbol: 'BTC/USD',
        base_currency: 'BTC',
        quote_currency: 'USD',
        current_price: 43250.50,
        price_change_24h: 2.45,
        volume_24h: 1250000,
        is_active: true
      },
      {
        id: 'ETH-USD',
        symbol: 'ETH/USD',
        base_currency: 'ETH',
        quote_currency: 'USD',
        current_price: 2650.75,
        price_change_24h: -1.23,
        volume_24h: 850000,
        is_active: true
      }
    ];
    setTradingPairs(mockPairs);
    if (!selectedPair && mockPairs.length > 0) {
      setSelectedPair(mockPairs[0]);
    }
  };

  const loadUserBalance = async () => {
    try {
      const token = authService.getAccessToken();
      if (!token) {
        setUserBalance(0);
        return;
      }
      
      // Use authService which handles automatic token refresh
      const response = await authService.makeAuthenticatedRequest('http://localhost:8000/api/balance/');
      
      if (response.ok) {
        const data = await response.json();
        setUserBalance(data.total_balance_usd || 0);
      }
    } catch (error) {
      console.error('Failed to load balance:', error);
      setUserBalance(0);
    }
  };

  // Seeded random function for consistent data
  const seededRandom = (seed: number) => {
    const x = Math.sin(seed++) * 10000;
    return x - Math.floor(x);
  };

  const loadChartDataFromBackend = useCallback(async () => {
    if (!selectedPair) return;
    
    try {
      console.log('📊 Loading chart data from backend...');
      console.log(`⏱️ Time interval: ${timeInterval}`);
      
      // Determine number of data points and interval based on timeInterval setting
      let limit = 30; // Default to 30 historical points
      let interval = 'seconds'; // Default interval
      
      switch (timeInterval) {
        case 'seconds':
          limit = 30; // 30 points * 2 seconds = 1 minute of data
          interval = 'seconds';
          break;
        case 'minutes':
          limit = 30; // 30 points * 1 minute = 30 minutes of data
          interval = 'minutes';
          break;
        case 'hours':
          limit = 24; // 24 points * 1 hour = 24 hours of data
          interval = 'hours';
          break;
      }
      
      // Fetch combined chart data (historical + current price)
      const response = await authService.makeAuthenticatedRequest(
        `http://localhost:8000/api/admin/market/combined-chart/?symbol=${selectedPair.base_currency}&limit=${limit}&interval=${interval}`
      );
      
      if (response.ok) {
        const data = await response.json();
        console.log('📈 Backend chart data loaded:', data);
        
        if (data.chart_data && data.chart_data.length > 0) {
          setChartData(data.chart_data);
          setPriceSource(data.price_source || 'unknown');
          
          // Set entry price (first data point)
          if (data.chart_data.length > 0) {
            setEntryPrice(data.chart_data[0].close);
          }
          
          console.log(`✅ Loaded ${data.chart_data.length} chart data points from backend`);
        } else {
          console.log('⚠️ No chart data available from backend, using fallback');
          generateFallbackChartData();
        }
      } else {
        console.error('Failed to load chart data from backend, using fallback');
        generateFallbackChartData();
      }
    } catch (error) {
      console.error('Error loading chart data from backend:', error);
      generateFallbackChartData();
    }
  }, [selectedPair]);

  const generateFallbackChartData = useCallback(() => {
    // Fallback function if backend data is not available
    const data: ChartData[] = [];
    let basePrice = selectedPair?.current_price || 43000;
    
    // Set entry price (first data point)
    setEntryPrice(basePrice);
    
    // Generate 30 simple data points
    for (let i = 30; i >= 0; i--) {
      const date = new Date();
      date.setMinutes(date.getMinutes() - (i * 2)); // 2 minutes apart
      
      const volatility = basePrice * 0.02;
      const open = basePrice + (Math.random() - 0.5) * volatility;
      const close = basePrice + (Math.random() - 0.5) * volatility;
      const high = Math.max(open, close) + Math.random() * volatility * 0.5;
      const low = Math.min(open, close) - Math.random() * volatility * 0.5;
      const volume = Math.random() * 1000000;
      
      data.push({
        timestamp: date.toISOString(),
        open,
        high,
        low,
        close,
        volume
      });
      
      basePrice = close;
    }
    
    setChartData(data);
    setPriceSource('live');
  }, [selectedPair]);

  const storeDataPointInBackend = useCallback(async (dataPoint: ChartData, source: string = 'live') => {
    if (!selectedPair) return;
    
    try {
      const response = await authService.makeAuthenticatedRequest(
        'http://localhost:8000/api/admin/market/store-data-point/',
        {
          method: 'POST',
          body: JSON.stringify({
            symbol: selectedPair.base_currency,
            timestamp: dataPoint.timestamp,
            open_price: dataPoint.open,
            high_price: dataPoint.high,
            low_price: dataPoint.low,
            close_price: dataPoint.close,
            volume: dataPoint.volume,
            source: source
          })
        }
      );
      
      if (response.ok) {
        console.log('✅ Data point stored in backend');
      } else {
        console.log('⚠️ Failed to store data point in backend');
      }
    } catch (error) {
      console.log('⚠️ Error storing data point in backend:', error);
    }
  }, [selectedPair]);
  
  // Reload chart data when time interval changes
  useEffect(() => {
    if (selectedPair) {
      console.log('⏱️ Time interval changed to:', timeInterval);
      loadChartDataFromBackend();
    }
  }, [timeInterval, selectedPair, loadChartDataFromBackend]);

  const formatTimeLabel = (timestamp: string) => {
    const date = new Date(timestamp);
    
    switch (timeInterval) {
      case 'seconds':
        return date.toLocaleTimeString('en-US', { 
          hour: '2-digit', 
          minute: '2-digit',
          second: '2-digit'
        });
      case 'minutes':
        return date.toLocaleTimeString('en-US', { 
          hour: '2-digit', 
          minute: '2-digit'
        });
      case 'hours':
        return date.toLocaleTimeString('en-US', { 
          hour: '2-digit',
          hour12: true
        });
      default:
        return date.toLocaleTimeString('en-US', { 
          hour: '2-digit', 
          minute: '2-digit',
          second: '2-digit'
        });
    }
  };

  const handlePlaceOrder = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        alert('Please sign in to place orders');
        router.push('/signin');
        return;
      }

      if (!selectedPair || !orderAmount || !stopPrice) {
        alert('Please fill in all required fields');
        return;
      }

      const response = await fetch('http://localhost:8000/api/trading/execute/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          trade_type: orderSide,
          cryptocurrency: selectedPair.base_currency,
          amount: orderAmount,
          price: stopPrice,
          leverage: leverage
        })
      });

      if (!response.ok) {
        const error = await response.json();
        alert(`Error: ${error.error}`);
        return;
      }

      const data = await response.json();
      
      let message = `${orderType.toUpperCase()} Order Executed!\n\n`;
      message += `Pair: ${selectedPair.symbol}\n`;
      message += `Side: ${orderSide.toUpperCase()}\n`;
      message += `Amount: ${orderAmount}\n`;
      message += `Price: $${stopPrice}\n`;
      message += `Leverage: ${leverage}x\n`;
      message += `Fees: $${data.fees.toFixed(2)}\n`;
      
      if (data.outcome) {
        message += `\n📊 Trade Info:\n`;
        message += `Expected Result: ${data.outcome.expected_outcome === 'win' ? '📈 PROFIT' : '📉 LOSS'}\n`;
        message += `Expected %: ${data.outcome.expected_percentage.toFixed(2)}%\n`;
        message += `Duration: ${data.outcome.duration_seconds}s\n`;
      }
      
      alert(message);
      
      // Reload balance
      loadUserBalance();
      
      setOrderAmount('');
      setStopPrice('');
      setLimitPrice('');
    } catch (error) {
      console.error('Failed to place order:', error);
      alert('Failed to place order. Please try again.');
    }
  };

  const handleAddStrategy = async () => {
    if (!selectedPair || !targetPrice || !strategyAmount) {
      alert('Please fill in all required fields');
      return;
    }

    // Calculate required margin
    const totalCost = parseFloat(strategyAmount) * selectedPair.current_price;
    const requiredMargin = totalCost / strategyLeverage;
    const tradingFee = totalCost * 0.001; // 0.1% fee
    const totalDeduction = requiredMargin + tradingFee;

    // Deduct from user balance via API
    try {
      const response = await authService.makeAuthenticatedRequest(
        'http://localhost:8000/api/trading/deduct-balance/',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            amount: totalDeduction,
            cryptocurrency_symbol: selectedPair.base_currency,
            trade_type: 'hold',
            leverage: strategyLeverage,
            description: `Strategy Trade: ${selectedPair.symbol}`,
            trade_amount: strategyAmount,
            entry_price: selectedPair.current_price
          })
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        alert(errorData.error || 'Insufficient balance or error deducting amount');
        return;
      }

      const deductionData = await response.json();

      const newStrategyPair = {
        id: deductionData.trade_id?.toString() || Date.now().toString(), // Use backend trade ID
        backendTradeId: deductionData.trade_id, // Store backend trade ID
        pair: selectedPair,
        type: strategyType,
        targetPrice: targetPrice,
        amount: strategyAmount,
        tradeSum: strategyAmount, // Initialize trade_sum to amount
        leverage: strategyLeverage,
        currentPrice: selectedPair.current_price,
        entryPrice: selectedPair.current_price,
        createdAt: new Date().toISOString(),
        status: 'active', // active, completed, stopped
        pnl: 0,
        pnlPercentage: 0,
        deductedAmount: totalDeduction, // Track how much was deducted
        trades: [] // Track individual trades for this strategy
      };

      setStrategyPairs(prev => [...prev, newStrategyPair]);
      
      // Clear form
      setTargetPrice('');
      setStrategyAmount('');
      setStrategyLeverage(1);
      
      alert(`Strategy pair added successfully! ${totalDeduction.toFixed(2)} USDT deducted from balance.`);
    } catch (error) {
      console.error('Error creating strategy:', error);
      alert('Failed to create strategy. Please try again.');
    }
  };

  // Simulate continuous trading for stored strategies
  const simulateStrategyTrading = useCallback(() => {
    setStrategyPairs(prevStrategies => {
      return prevStrategies.map(strategy => {
        // Check if trade_sum has reached zero
        if (parseFloat(strategy.tradeSum || strategy.amount) <= 0) {
          return {
            ...strategy,
            status: 'completed',
            tradeSum: 0,
            lastUpdate: new Date().toISOString()
          };
        }
        
        if (strategy.status !== 'active') return strategy;
        
        // Simulate price movement (random walk)
        const priceChange = (Math.random() - 0.5) * 0.02; // ±1% change
        const newPrice = strategy.currentPrice * (1 + priceChange);
        
        // Calculate P&L based on entry price
        const entryPrice = strategy.entryPrice || strategy.currentPrice;
        const priceDiff = newPrice - entryPrice;
        const pnlPercentage = (priceDiff / entryPrice) * 100;
        const pnl = parseFloat(strategy.amount) * priceDiff * strategy.leverage;
        
        // Simulate trading execution - decrease trade_sum
        const currentTradeSum = parseFloat(strategy.tradeSum || strategy.amount);
        const tradingRate = 0.02; // Trade 2% of remaining per interval
        const tradedAmount = currentTradeSum * tradingRate;
        const newTradeSum = Math.max(0, currentTradeSum - tradedAmount);
        
        // Calculate progress based on trade_sum remaining
        const tradeSumProgress = ((parseFloat(strategy.amount) - newTradeSum) / parseFloat(strategy.amount)) * 100;
        
        // Calculate progress towards target price
        let priceProgress = 0;
        if (strategy.type === 'buy') {
          priceProgress = (newPrice / parseFloat(strategy.targetPrice)) * 100;
        } else if (strategy.type === 'sell') {
          priceProgress = (parseFloat(strategy.targetPrice) / newPrice) * 100;
        } else {
          // Hold strategy - calculate based on price movement
          priceProgress = Math.min(100, Math.abs(pnlPercentage));
        }
        
        // Create ongoing trade entry
        const ongoingTrade = {
          id: strategy.id,
          pair: strategy.pair.symbol,
          type: strategy.type,
          amount: strategy.amount,
          tradeSum: newTradeSum,
          entryPrice: entryPrice,
          currentPrice: newPrice,
          leverage: strategy.leverage,
          pnl: pnl,
          pnlPercentage: pnlPercentage,
          status: newTradeSum > 0 ? 'open' : 'completed',
          timestamp: strategy.createdAt,
          tradeSumProgress: tradeSumProgress
        };
        
        return {
          ...strategy,
          currentPrice: newPrice,
          tradeSum: newTradeSum.toFixed(8),
          progress: tradeSumProgress,
          priceProgress: Math.min(100, priceProgress),
          pnl: pnl,
          pnlPercentage: pnlPercentage,
          lastUpdate: new Date().toISOString(),
          ongoingTrade: ongoingTrade
        };
      });
    });
  }, []);

  // Run strategy simulation every 5 seconds
  useEffect(() => {
    const interval = setInterval(simulateStrategyTrading, 5000);
    return () => clearInterval(interval);
  }, [simulateStrategyTrading]);

  const renderCandlestickChart = () => {
    if (chartData.length === 0) return null;
    
    // Use first candle as entry price for percentage calculation
    const entry = entryPrice || chartData[0].close;
    
    // Calculate CUMULATIVE percentage changes - each candle builds on the previous
    const percentageData: Array<{ timestamp: string; openPct: number; highPct: number; lowPct: number; closePct: number }> = [];
    
    chartData.forEach((candle, index) => {
      if (index === 0) {
        // First candle starts at 0%
        percentageData.push({
          timestamp: candle.timestamp,
          openPct: 0,
          highPct: ((candle.high - candle.open) / candle.open) * 100,
          lowPct: ((candle.low - candle.open) / candle.open) * 100,
          closePct: ((candle.close - candle.open) / candle.open) * 100,
        });
      } else {
        // Subsequent candles build on previous close
        const prevClose = chartData[index - 1].close;
        const prevCumulativePct: number = percentageData[index - 1].closePct;
        
        percentageData.push({
          timestamp: candle.timestamp,
          openPct: prevCumulativePct + ((candle.open - prevClose) / prevClose) * 100,
          highPct: prevCumulativePct + ((candle.high - prevClose) / prevClose) * 100,
          lowPct: prevCumulativePct + ((candle.low - prevClose) / prevClose) * 100,
          closePct: prevCumulativePct + ((candle.close - prevClose) / prevClose) * 100,
        });
      }
    });
    
    const maxPct = Math.max(...percentageData.map((d) => d.highPct));
    const minPct = Math.min(...percentageData.map((d) => d.lowPct));
    
    // Dynamic Y-axis with centered graph
    const maxAbsPct = Math.max(Math.abs(maxPct), Math.abs(minPct));
    const maxYValue = Math.min(Math.ceil(maxAbsPct / 10) * 10 + 10, 100);
    const yAxisLabels = [];
    for (let i = 0; i <= maxYValue; i += 10) {
      yAxisLabels.push(i);
    }
    
    // Center the baseline - if we have both profit and loss, center it
    const chartHeight = 280; // Total usable height
    const baselineY = chartHeight / 2 + 30; // Center vertically (30px offset for top margin)
    const yScale = ((chartHeight / 2) / maxYValue) * 5.0; // Scale to fit in half the height, then 5x taller
    
    return (
      <div className="relative h-full">
        <svg width="100%" height="100%" viewBox="0 0 900 340" preserveAspectRatio="none">
          {/* Baseline (entry price at 0%) - Hidden */}
          <line
            x1="0"
            y1={baselineY}
            x2="900"
            y2={baselineY}
            stroke="transparent"
            strokeWidth="0"
          />
          
          {/* Grid lines */}
          {yAxisLabels.map((pct) => (
            <line
              key={pct}
              x1="0"
              y1={baselineY - pct * yScale}
              x2="900"
              y2={baselineY - pct * yScale}
              stroke="#374151"
              strokeWidth="0.5"
              strokeDasharray="5,5"
            />
          ))}
          
          {/* Candlesticks */}
          {percentageData.map((candle, index) => {
            const x = 60 + (index / chartData.length) * 840;
            const candleWidth = 840 / chartData.length * 0.7;
            const isLastCandle = index === percentageData.length - 1;
            
            // Plot cumulative values - positive values go up, negative stay as is
            const openY = baselineY - candle.openPct * yScale;
            const closeY = baselineY - candle.closePct * yScale;
            const highY = baselineY - candle.highPct * yScale;
            const lowY = baselineY - candle.lowPct * yScale;
            
            // Green if this candle moved up, red if it moved down
            const candleGain = candle.closePct - candle.openPct;
            const color = candleGain >= 0 ? '#10b981' : '#ef4444';
            
            const bodyTop = Math.min(openY, closeY);
            const bodyHeight = Math.abs(closeY - openY);
            
            return (
              <g key={index}>
                <line
                  x1={x + candleWidth / 2}
                  y1={highY}
                  x2={x + candleWidth / 2}
                  y2={lowY}
                  stroke={color}
                  strokeWidth="2"
                  opacity="0.9"
                />
                <rect
                  x={x}
                  y={bodyTop}
                  width={candleWidth}
                  height={bodyHeight || 3}
                  fill={color}
                  opacity="0.9"
                />
              </g>
            );
          })}
          
          {/* Time labels on X-axis */}
          {chartData.filter((_, i) => i % 3 === 0).map((candle, index) => {
            const actualIndex = index * 3;
            const x = 60 + (actualIndex / chartData.length) * 840;
            const time = formatTimeLabel(candle.timestamp);
            
            return (
              <text
                key={`time-${actualIndex}`}
                x={x}
                y="330"
                fill="#9ca3af"
                fontSize="11"
                fontWeight="bold"
                textAnchor="middle"
              >
                {time}
              </text>
            );
          })}
        </svg>
      </div>
    );
  };

  const renderLineChart = () => {
    if (chartData.length === 0) return null;
    
    // Use first candle as entry price
    const entry = entryPrice || chartData[0].close;
    
    // Calculate CUMULATIVE percentage changes - builds from previous point
    const percentageData: Array<{ timestamp: string; pct: number }> = [];
    
    chartData.forEach((candle, index) => {
      if (index === 0) {
        percentageData.push({
          timestamp: candle.timestamp,
          pct: ((candle.close - entry) / entry) * 100
        });
      } else {
        const prevClose = chartData[index - 1].close;
        const prevPct: number = percentageData[index - 1].pct;
        percentageData.push({
          timestamp: candle.timestamp,
          pct: prevPct + ((candle.close - prevClose) / prevClose) * 100
        });
      }
    });
    
    const maxPct = Math.max(...percentageData.map((d) => d.pct));
    const minPct = Math.min(...percentageData.map((d) => d.pct));
    
    // Dynamic Y-axis with centered graph
    const maxAbsPct = Math.max(Math.abs(maxPct), Math.abs(minPct));
    const maxYValue = Math.min(Math.ceil(maxAbsPct / 10) * 10 + 10, 100);
    const yAxisLabels = [];
    for (let i = 0; i <= maxYValue; i += 10) {
      yAxisLabels.push(i);
    }
    
    // Center the baseline - if we have both profit and loss, center it
    const chartHeight = 280; // Total usable height
    const baselineY = chartHeight / 2 + 30; // Center vertically (30px offset for top margin)
    const yScale = ((chartHeight / 2) / maxYValue) * 5.0; // Scale to fit in half the height, then 5x taller
    
    // Create line segments with individual colors based on gain/loss
    const lineSegments: Array<{ x1: number; y1: number; x2: number; y2: number; color: string }> = [];
    
    for (let i = 0; i < percentageData.length - 1; i++) {
      const x1 = 60 + (i / (chartData.length - 1)) * 840;
      const y1 = baselineY - percentageData[i].pct * yScale;
      const x2 = 60 + ((i + 1) / (chartData.length - 1)) * 840;
      const y2 = baselineY - percentageData[i + 1].pct * yScale;
      
      // Green if this segment goes up (gain), red if it goes down (loss)
      const isGain = percentageData[i + 1].pct >= percentageData[i].pct;
      const color = isGain ? '#10b981' : '#ef4444';
      
      lineSegments.push({ x1, y1, x2, y2, color });
    }
    
    // Create area path for overall fill
    let areaPath = `M 60,${baselineY}`;
    percentageData.forEach((data, index) => {
      const x = 60 + (index / (chartData.length - 1)) * 840;
      const y = baselineY - data.pct * yScale;
      areaPath += ` L ${x},${y}`;
    });
    areaPath += ` L ${60 + 840},${baselineY} Z`;
    
    // Determine overall color based on final position
    const finalPct = percentageData[percentageData.length - 1]?.pct || 0;
    const isOverallProfit = finalPct >= 0;
    
    return (
      <div className="relative h-full">
        <svg width="100%" height="100%" viewBox="0 0 900 340" preserveAspectRatio="none">
          <defs>
            <linearGradient id="profitGradient" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stopColor="#10b981" stopOpacity="0.8" />
              <stop offset="50%" stopColor="#10b981" stopOpacity="0.4" />
              <stop offset="100%" stopColor="#10b981" stopOpacity="0" />
            </linearGradient>
            <linearGradient id="lossGradient" x1="0" x2="0" y1="1" y2="0">
              <stop offset="0%" stopColor="#ef4444" stopOpacity="0.8" />
              <stop offset="50%" stopColor="#ef4444" stopOpacity="0.4" />
              <stop offset="100%" stopColor="#ef4444" stopOpacity="0" />
            </linearGradient>
          </defs>
          
          {/* Baseline (entry price at 0%) - Hidden */}
          <line
            x1="0"
            y1={baselineY}
            x2="900"
            y2={baselineY}
            stroke="transparent"
            strokeWidth="0"
          />
          
          {/* Grid lines */}
          {yAxisLabels.map((pct) => (
            <line
              key={pct}
              x1="0"
              y1={baselineY - pct * yScale}
              x2="900"
              y2={baselineY - pct * yScale}
              stroke="#374151"
              strokeWidth="0.5"
              strokeDasharray="5,5"
            />
          ))}
          
          {/* Cumulative area fill */}
          <path
            d={areaPath}
            fill={isOverallProfit ? 'url(#profitGradient)' : 'url(#lossGradient)'}
            opacity="0.3"
          />
          
          {/* Colored line segments - green for gains, red for losses */}
          {lineSegments.map((segment, index) => {
            const isLastSegment = index === lineSegments.length - 1;
            return (
              <line
                key={`segment-${index}`}
                x1={segment.x1}
                y1={segment.y1}
                x2={segment.x2}
                y2={segment.y2}
                stroke={segment.color}
                strokeWidth="4"
                strokeLinecap="round"
                opacity="0.9"
              />
            );
          })}
          
          
          {/* Time labels */}
          {chartData.filter((_, i) => i % 3 === 0).map((candle, index) => {
            const actualIndex = index * 3;
            const x = 60 + (actualIndex / (chartData.length - 1)) * 840;
            const time = formatTimeLabel(candle.timestamp);
            
            return (
              <text
                key={`time-${actualIndex}`}
                x={x}
                y="330"
                fill="#9ca3af"
                fontSize="11"
                fontWeight="bold"
                textAnchor="middle"
              >
                {time}
              </text>
            );
          })}
        </svg>
      </div>
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
              <h1 className="text-white text-3xl font-bold">Advanced Orders Trading</h1>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="bg-dark_grey rounded-lg px-4 py-2 flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-success animate-pulse' : 'bg-error'}`}></div>
              <span className={`text-xs ${isConnected ? 'text-success' : 'text-error'}`}>
                {isConnected ? 'Live Data' : 'Disconnected'}
              </span>
            </div>
            {priceSource !== 'unknown' && (
              <div className={`rounded-lg px-4 py-2 flex items-center gap-2 ${
                priceSource === 'real' 
                  ? 'bg-primary/20 border border-primary/40' 
                  : 'bg-warning/20 border border-warning/40'
              }`}>
                <Icon 
                  icon={priceSource === 'real' ? 'tabler:world' : 'tabler:chart-dots'} 
                  width="16" 
                  height="16" 
                  className={priceSource === 'real' ? 'text-primary' : 'text-warning'}
                />
                <span className={`text-xs font-semibold ${priceSource === 'real' ? 'text-primary' : 'text-warning'}`}>
                  {priceSource === 'real' ? 'Real Prices' : 'Live Prices'}
                </span>
              </div>
            )}
            <div className="bg-dark_grey rounded-lg px-6 py-3">
              <p className="text-muted text-sm">Available Balance</p>
              <p className="text-white text-xl font-bold">${userBalance.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
            </div>
          </div>
        </div>

        <div className="grid lg:grid-cols-12 gap-6">
          {/* Left Panel - Strategy Pairs */}
          <div className="lg:col-span-3 bg-dark_grey rounded-lg p-4">
            <h3 className="text-white font-semibold mb-4">Strategy Pairs</h3>
            <div className="space-y-3 max-h-[600px] overflow-y-auto">
              {strategyPairs.length === 0 ? (
                <div className="text-center py-8">
                  <Icon icon="tabler:strategy" width="48" height="48" className="text-muted mx-auto mb-3" />
                  <p className="text-muted text-sm">No strategy pairs added yet</p>
                  <p className="text-muted text-xs mt-1">Use the form on the right to add pairs</p>
                </div>
              ) : (
                strategyPairs.map((strategyPair) => (
                  <div
                    key={strategyPair.id}
                    className="p-4 rounded-lg border border-dark_border bg-darkmode"
                  >
                    {/* Strategy Header */}
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <h4 className="text-white font-semibold text-lg">{strategyPair.pair.symbol}</h4>
                        <p className="text-muted text-xs">{strategyPair.pair.base_currency}/{strategyPair.pair.quote_currency}</p>
                      </div>
                      <div className={`px-3 py-1 rounded-full text-xs font-semibold ${
                        strategyPair.type === 'buy' 
                          ? 'bg-success bg-opacity-20 text-success' 
                          : strategyPair.type === 'sell'
                          ? 'bg-error bg-opacity-20 text-error'
                          : 'bg-warning bg-opacity-20 text-warning'
                      }`}>
                        {strategyPair.type.toUpperCase()}
                      </div>
                    </div>

                    {/* Strategy Details */}
                    <div className="space-y-2 mb-3">
                      <div className="flex justify-between">
                        <span className="text-muted text-xs">Entry Price:</span>
                        <span className="text-white font-semibold">${(strategyPair.entryPrice || strategyPair.currentPrice).toFixed(2)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted text-xs">Current Price:</span>
                        <span className="text-white">${strategyPair.currentPrice.toFixed(2)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted text-xs">Target Price:</span>
                        <span className="text-white">${parseFloat(strategyPair.targetPrice).toFixed(2)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted text-xs">Initial Amount:</span>
                        <span className="text-white">{strategyPair.amount}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted text-xs">Remaining:</span>
                        <span className={`font-semibold ${
                          parseFloat(strategyPair.tradeSum || strategyPair.amount) > 0 ? 'text-primary' : 'text-success'
                        }`}>
                          {parseFloat(strategyPair.tradeSum || strategyPair.amount).toFixed(8)}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted text-xs">Leverage:</span>
                        <span className="text-white">{strategyPair.leverage}x</span>
                      </div>
                      <div className="flex justify-between border-t border-dark_border pt-2 mt-2">
                        <span className="text-muted text-xs">P&L:</span>
                        <span className={`font-bold ${
                          (strategyPair.pnl || 0) >= 0 ? 'text-success' : 'text-error'
                        }`}>
                          ${(strategyPair.pnl || 0).toFixed(2)} ({(strategyPair.pnlPercentage || 0).toFixed(2)}%)
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted text-xs">Status:</span>
                        <span className={`text-xs font-semibold ${
                          strategyPair.status === 'active' ? 'text-success' : 
                          strategyPair.status === 'completed' ? 'text-info' : 'text-warning'
                        }`}>
                          {strategyPair.status === 'active' ? '● Trading' : 
                           strategyPair.status === 'completed' ? '✓ Completed' : '⏸ Paused'}
                        </span>
                      </div>
                    </div>

                    {/* Progress Indicator */}
                    <div className="mb-3">
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-muted">Progress</span>
                        <span className={`font-semibold ${
                          strategyPair.type === 'hold' ? 'text-warning' : 'text-primary'
                        }`}>
                          {strategyPair.type === 'hold' 
                            ? 'Monitoring'
                            : `${(strategyPair.progress || 0).toFixed(1)}%`
                          }
                        </span>
                      </div>
                      <div className="w-full bg-darkmode rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full ${
                            strategyPair.type === 'hold' ? 'bg-warning' : 'bg-primary'
                          }`}
                          style={{
                            width: `${Math.min(strategyPair.progress || 0, 100)}%`
                          }}
                        ></div>
                      </div>
                      {strategyPair.lastUpdate && (
                        <div className="text-xs text-muted mt-1">
                          Last update: {new Date(strategyPair.lastUpdate).toLocaleTimeString()}
                        </div>
                      )}
                    </div>

                    {/* Action Buttons */}
                    <div className="grid grid-cols-2 gap-2">
                      <button
                        onClick={() => {
                          setStrategyPairs(prev => prev.map(sp => 
                            sp.id === strategyPair.id 
                              ? { ...sp, status: sp.status === 'active' ? 'paused' : 'active' }
                              : sp
                          ));
                        }}
                        className={`py-2 rounded-lg text-xs font-semibold transition-all ${
                          strategyPair.status === 'active'
                            ? 'bg-warning bg-opacity-20 text-warning hover:bg-warning hover:text-white'
                            : 'bg-success bg-opacity-20 text-success hover:bg-success hover:text-white'
                        }`}
                        disabled={strategyPair.status === 'completed'}
                      >
                        {strategyPair.status === 'active' ? '⏸ Pause' : '▶ Resume'}
                      </button>
                      <button
                        onClick={async () => {
                          if (confirm(`Stop this strategy? Remaining ${strategyPair.tradeSum} will be returned to your balance.`)) {
                            try {
                              const response = await authService.makeAuthenticatedRequest(
                                `http://localhost:8000/api/trading/stop/${strategyPair.id}/`,
                                {
                                  method: 'POST',
                                  headers: {
                                    'Content-Type': 'application/json',
                                  }
                                }
                              );
                              
                              if (response.ok) {
                                const data = await response.json();
                                alert(data.message);
                                setStrategyPairs(prev => prev.filter(sp => sp.id !== strategyPair.id));
                              } else {
                                // If API call fails, just remove from localStorage
                                setStrategyPairs(prev => prev.filter(sp => sp.id !== strategyPair.id));
                              }
                            } catch (error) {
                              console.error('Error stopping trade:', error);
                              setStrategyPairs(prev => prev.filter(sp => sp.id !== strategyPair.id));
                            }
                          }
                        }}
                        className="py-2 rounded-lg text-xs font-semibold bg-error bg-opacity-20 text-error hover:bg-error hover:text-white transition-all"
                      >
                        🛑 Stop
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Center Panel - Chart */}
          <div className="lg:col-span-6 bg-dark_grey rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex-1">
                <h3 className="text-white text-2xl font-bold mb-1">{selectedPair?.symbol}</h3>
                <div className="flex items-center gap-4">
                  <div className={`transition-all duration-300 ${priceFlash ? 'scale-110' : 'scale-100'}`}>
                    <p className={`text-3xl font-bold ${priceFlash ? 'text-primary' : 'text-white'}`}>
                      ${selectedPair?.current_price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </p>
                  </div>
                  {entryPrice && selectedPair && (
                    <div className={`px-4 py-2 rounded-lg ${
                      selectedPair.current_price >= entryPrice 
                        ? 'bg-success/20 border border-success/40' 
                        : 'bg-error/20 border border-error/40'
                    }`}>
                      <p className={`text-2xl font-bold ${
                        selectedPair.current_price >= entryPrice ? 'text-success' : 'text-error'
                      }`}>
                        {selectedPair.current_price >= entryPrice ? '+' : ''}
                        {(((selectedPair.current_price - entryPrice) / entryPrice) * 100).toFixed(2)}%
                      </p>
                      <p className="text-xs text-muted">P/L</p>
                    </div>
                  )}
                </div>
                {lastUpdateTime && (
                  <p className="text-muted text-xs flex items-center gap-1 mt-2">
                    <span className="w-2 h-2 bg-success rounded-full animate-pulse"></span>
                    Last update: {lastUpdateTime}
                  </p>
                )}
              </div>
              <div className="flex items-center gap-4">
                {/* Chart Type Selector */}
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setChartType('candlestick')}
                    className={`px-4 py-2 rounded-lg transition-all ${
                      chartType === 'candlestick'
                        ? 'bg-primary text-white'
                        : 'bg-darkmode text-muted hover:text-white'
                    }`}
                  >
                    <Icon icon="tabler:chart-candle" width="20" height="20" />
                  </button>
                  <button
                    onClick={() => setChartType('line')}
                    className={`px-4 py-2 rounded-lg transition-all ${
                      chartType === 'line'
                        ? 'bg-primary text-white'
                        : 'bg-darkmode text-muted hover:text-white'
                    }`}
                  >
                    <Icon icon="tabler:chart-line" width="20" height="20" />
                  </button>
                </div>
                
                {/* Time Interval Selector */}
                <div className="flex items-center gap-1 bg-darkmode rounded-lg p-1">
                  <button
                    onClick={() => setTimeInterval('seconds')}
                    className={`px-3 py-1.5 rounded text-xs font-semibold transition-all ${
                      timeInterval === 'seconds'
                        ? 'bg-success text-white'
                        : 'text-muted hover:text-white'
                    }`}
                  >
                    S
                  </button>
                  <button
                    onClick={() => setTimeInterval('minutes')}
                    className={`px-3 py-1.5 rounded text-xs font-semibold transition-all ${
                      timeInterval === 'minutes'
                        ? 'bg-success text-white'
                        : 'text-muted hover:text-white'
                    }`}
                  >
                    M
                  </button>
                  <button
                    onClick={() => setTimeInterval('hours')}
                    className={`px-3 py-1.5 rounded text-xs font-semibold transition-all ${
                      timeInterval === 'hours'
                        ? 'bg-success text-white'
                        : 'text-muted hover:text-white'
                    }`}
                  >
                    H
                  </button>
                </div>
              </div>
            </div>
            
            <div className="bg-darkmode rounded-lg p-4 h-[600px] overflow-hidden">
              {chartType === 'candlestick' ? renderCandlestickChart() : renderLineChart()}
            </div>
          </div>

          {/* Right Panel - Trade Pair Strategy */}
          <div className="lg:col-span-3 bg-dark_grey rounded-lg p-6">
            <h3 className="text-white font-semibold mb-4">Trade Pair Strategy</h3>
            
            {/* Strategy Configuration */}
            <div className="space-y-4">
              {/* Trading Pair Selection */}
              <div>
                <label className="text-muted text-sm mb-2 block">Select Trading Pair</label>
                <select
                  value={selectedPair?.id || ''}
                  onChange={(e) => {
                    const pair = tradingPairs.find(p => p.id.toString() === e.target.value);
                    setSelectedPair(pair || null);
                  }}
                  className="w-full bg-darkmode border border-dark_border rounded-lg px-4 py-3 text-white focus:outline-none focus:border-primary"
                >
                  <option value="">Choose a trading pair</option>
                  {tradingPairs.map((pair) => (
                    <option key={pair.id} value={pair.id}>
                      {pair.symbol} - {pair.base_currency}/{pair.quote_currency}
                    </option>
                  ))}
                </select>
              </div>


              {/* Target Price */}
              <div>
                <label className="text-muted text-sm mb-2 block">Target Price (USD)</label>
                <input
                  type="number"
                  value={targetPrice}
                  onChange={(e) => setTargetPrice(e.target.value)}
                  className="w-full bg-darkmode border border-dark_border rounded-lg px-4 py-3 text-white focus:outline-none focus:border-primary"
                  placeholder="Enter target price"
                  step="0.01"
                />
              </div>

              {/* Strategy Parameters */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-muted text-sm mb-2 block">Amount</label>
                  <input
                    type="number"
                    value={strategyAmount}
                    onChange={(e) => setStrategyAmount(e.target.value)}
                    className="w-full bg-darkmode border border-dark_border rounded-lg px-4 py-3 text-white focus:outline-none focus:border-primary"
                    placeholder="0.00"
                    step="0.01"
                  />
                </div>
                <div>
                  <label className="text-muted text-sm mb-2 block">Leverage</label>
                  <select
                    value={strategyLeverage}
                    onChange={(e) => setStrategyLeverage(parseInt(e.target.value))}
                    className="w-full bg-darkmode border border-dark_border rounded-lg px-4 py-3 text-white focus:outline-none focus:border-primary"
                  >
                    <option value={1}>1x</option>
                    <option value={5}>5x</option>
                    <option value={10}>10x</option>
                    <option value={25}>25x</option>
                  </select>
                </div>
              </div>

              {/* Add Strategy Button */}
              <button
                onClick={handleAddStrategy}
                disabled={!selectedPair || !targetPrice || !strategyAmount}
                className="w-full py-3 rounded-lg font-semibold transition-all bg-primary hover:bg-primary/90 text-white disabled:bg-muted disabled:text-darkmode disabled:cursor-not-allowed"
              >
                Add to Strategy List
              </button>
            </div>

            {/* Strategy Summary */}
            <div className="mt-6 p-4 bg-darkmode rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <span className="text-muted text-sm">Active Strategies</span>
                <span className="text-primary font-semibold">{strategyPairs.length}</span>
              </div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-muted text-sm">Selected Pair</span>
                <span className="text-white font-semibold text-sm">
                  {selectedPair?.symbol || 'None'}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-muted text-sm">Total Value</span>
                <span className="text-success font-semibold">
                  ${strategyPairs.reduce((sum, pair) => sum + (parseFloat(pair.amount || '0') * parseFloat(pair.targetPrice || '0')), 0).toFixed(2)}
                </span>
              </div>
            </div>

            {/* Info Notice */}
            <div className="mt-4 p-3 bg-info bg-opacity-10 border border-info border-opacity-30 rounded-lg">
              <div className="flex items-start gap-2">
                <Icon icon="tabler:strategy" width="16" height="16" className="text-info mt-0.5" />
                <div>
                  <p className="text-info text-xs font-semibold mb-1">Strategy Trading Information</p>
                  <p className="text-muted text-xs">
                    Strategy trades are simulated and DO NOT affect your wallet balance. All strategies default to "Hold" mode. The trade_sum decreases as trades execute, and trading stops when it reaches zero. Strategies persist even when you close the browser.
                  </p>
                </div>
              </div>
            </div>
            
            {/* Continuous Trading Status */}
            <div className="mt-3 p-3 bg-success bg-opacity-10 border border-success border-opacity-30 rounded-lg">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-success rounded-full animate-pulse"></div>
                <div>
                  <p className="text-success text-xs font-semibold">Continuous Trading Active</p>
                  <p className="text-muted text-xs">Strategies update every 5 seconds • trade_sum decreases to zero</p>
                </div>
              </div>
            </div>
            
            {/* Important Notice - No Balance Impact */}
            <div className="mt-3 p-3 bg-success bg-opacity-10 border border-success border-opacity-30 rounded-lg">
              <div className="flex items-start gap-2">
                <Icon icon="tabler:shield-check" width="16" height="16" className="text-success mt-0.5" />
                <div>
                  <p className="text-success text-xs font-semibold mb-1">Wallet Protection Active</p>
                  <p className="text-muted text-xs">
                    Strategy trades are 100% simulated and will NOT deduct from or add to your wallet balance. Your USDT balance remains completely safe. The trade_sum decreases as simulated trades execute, stopping automatically when it reaches zero.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Strategy Trades Section */}
      <div className="container mx-auto max-w-7xl px-4 mt-8">
        <div className="bg-dark_grey rounded-lg p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-white text-2xl font-bold">Strategy Trades</h2>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-success rounded-full animate-pulse"></div>
              <span className="text-success text-sm font-semibold">
                {strategyPairs.filter(sp => sp.status === 'active').length} Active
              </span>
            </div>
          </div>
          
          {strategyPairs.length === 0 ? (
            <div className="text-center py-12">
              <Icon icon="tabler:chart-line" width="64" height="64" className="text-muted mx-auto mb-4" />
              <p className="text-muted text-lg mb-2">No Strategy Trades Yet</p>
              <p className="text-muted text-sm">Add strategy pairs above to start trading</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-dark_border">
                    <th className="text-left text-muted text-xs font-semibold pb-3">Pair</th>
                    <th className="text-left text-muted text-xs font-semibold pb-3">Type</th>
                    <th className="text-right text-muted text-xs font-semibold pb-3">Entry</th>
                    <th className="text-right text-muted text-xs font-semibold pb-3">Current</th>
                    <th className="text-right text-muted text-xs font-semibold pb-3">Target</th>
                    <th className="text-right text-muted text-xs font-semibold pb-3">Initial</th>
                    <th className="text-right text-muted text-xs font-semibold pb-3">Remaining</th>
                    <th className="text-right text-muted text-xs font-semibold pb-3">Leverage</th>
                    <th className="text-right text-muted text-xs font-semibold pb-3">P&L</th>
                    <th className="text-center text-muted text-xs font-semibold pb-3">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {strategyPairs.map((strategy) => (
                    <tr key={strategy.id} className="border-b border-dark_border hover:bg-darkmode transition-colors">
                      <td className="py-4">
                        <div>
                          <p className="text-white font-semibold">{strategy.pair.symbol}</p>
                          <p className="text-muted text-xs">{strategy.pair.base_currency}/{strategy.pair.quote_currency}</p>
                        </div>
                      </td>
                      <td className="py-4">
                        <span className={`px-2 py-1 rounded text-xs font-semibold ${
                          strategy.type === 'buy' 
                            ? 'bg-success bg-opacity-20 text-success' 
                            : strategy.type === 'sell'
                            ? 'bg-error bg-opacity-20 text-error'
                            : 'bg-warning bg-opacity-20 text-warning'
                        }`}>
                          {strategy.type.toUpperCase()}
                        </span>
                      </td>
                      <td className="text-right py-4">
                        <span className="text-white text-sm">${(strategy.entryPrice || strategy.currentPrice).toFixed(2)}</span>
                      </td>
                      <td className="text-right py-4">
                        <span className="text-white font-semibold">${strategy.currentPrice.toFixed(2)}</span>
                      </td>
                      <td className="text-right py-4">
                        <span className="text-muted text-sm">${parseFloat(strategy.targetPrice).toFixed(2)}</span>
                      </td>
                      <td className="text-right py-4">
                        <span className="text-white text-sm">{strategy.amount}</span>
                      </td>
                      <td className="text-right py-4">
                        <span className={`text-sm font-semibold ${
                          parseFloat(strategy.tradeSum || strategy.amount) > 0 ? 'text-primary' : 'text-success'
                        }`}>
                          {parseFloat(strategy.tradeSum || strategy.amount).toFixed(8)}
                        </span>
                      </td>
                      <td className="text-right py-4">
                        <span className="text-primary text-sm font-semibold">{strategy.leverage}x</span>
                      </td>
                      <td className="text-right py-4">
                        <div>
                          <p className={`font-bold ${
                            (strategy.pnl || 0) >= 0 ? 'text-success' : 'text-error'
                          }`}>
                            ${(strategy.pnl || 0).toFixed(2)}
                          </p>
                          <p className={`text-xs ${
                            (strategy.pnlPercentage || 0) >= 0 ? 'text-success' : 'text-error'
                          }`}>
                            {(strategy.pnlPercentage || 0) >= 0 ? '+' : ''}{(strategy.pnlPercentage || 0).toFixed(2)}%
                          </p>
                        </div>
                      </td>
                      <td className="text-center py-4">
                        <span className={`px-2 py-1 rounded text-xs font-semibold ${
                          strategy.status === 'active' 
                            ? 'bg-success bg-opacity-20 text-success' 
                            : strategy.status === 'completed'
                            ? 'bg-info bg-opacity-20 text-info'
                            : 'bg-warning bg-opacity-20 text-warning'
                        }`}>
                          {strategy.status === 'active' ? '● Trading' : 
                           strategy.status === 'completed' ? '✓ Completed' : '⏸ Paused'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              
              {/* Summary */}
              <div className="mt-6 pt-6 border-t border-dark_border">
                <div className="grid grid-cols-4 gap-4">
                  <div className="bg-darkmode rounded-lg p-4">
                    <p className="text-muted text-xs mb-1">Total Strategies</p>
                    <p className="text-white text-2xl font-bold">{strategyPairs.length}</p>
                  </div>
                  <div className="bg-darkmode rounded-lg p-4">
                    <p className="text-muted text-xs mb-1">Active Trading</p>
                    <p className="text-success text-2xl font-bold">
                      {strategyPairs.filter(sp => sp.status === 'active').length}
                    </p>
                  </div>
                  <div className="bg-darkmode rounded-lg p-4">
                    <p className="text-muted text-xs mb-1">Total P&L</p>
                    <p className={`text-2xl font-bold ${
                      strategyPairs.reduce((sum, sp) => sum + (sp.pnl || 0), 0) >= 0 ? 'text-success' : 'text-error'
                    }`}>
                      ${strategyPairs.reduce((sum, sp) => sum + (sp.pnl || 0), 0).toFixed(2)}
                    </p>
                  </div>
                  <div className="bg-darkmode rounded-lg p-4">
                    <p className="text-muted text-xs mb-1">Total Volume</p>
                    <p className="text-primary text-2xl font-bold">
                      ${strategyPairs.reduce((sum, sp) => sum + (parseFloat(sp.amount) * sp.currentPrice), 0).toFixed(2)}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
      
      {/* Wallet Trades Section (All Trades History) */}
      <div className="container mx-auto max-w-7xl px-4 mt-8">
        <div className="mb-4 p-3 bg-info bg-opacity-10 border border-info border-opacity-30 rounded-lg">
          <div className="flex items-start gap-2">
            <Icon icon="tabler:wallet" width="16" height="16" className="text-info mt-0.5" />
            <div>
              <p className="text-info text-xs font-semibold mb-1">Trade History</p>
              <p className="text-muted text-xs">
                This section shows your trade history. Strategy Trades (above) are simulated and don't affect your wallet balance. Only actual wallet trades impact your USDT balance.
              </p>
            </div>
          </div>
        </div>
        <OngoingTrades />
      </div>
    </div>
  );
}
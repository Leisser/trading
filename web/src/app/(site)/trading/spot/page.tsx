"use client";

import React, { useState, useEffect } from 'react';
import { Icon } from "@iconify/react";

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

interface OrderBookEntry {
  price: number;
  amount: number;
  total: number;
}

interface Trade {
  id: number;
  price: number;
  amount: number;
  side: 'buy' | 'sell';
  timestamp: string;
}

export default function SpotTradingPage() {
  const [selectedPair, setSelectedPair] = useState<TradingPair | null>(null);
  const [tradingPairs, setTradingPairs] = useState<TradingPair[]>([]);
  const [orderBook, setOrderBook] = useState<{
    bids: OrderBookEntry[];
    asks: OrderBookEntry[];
  }>({ bids: [], asks: [] });
  const [recentTrades, setRecentTrades] = useState<Trade[]>([]);
  const [userBalance, setUserBalance] = useState(0);
  const [loading, setLoading] = useState(true);
  
  // Order form states
  const [orderType, setOrderType] = useState<'market' | 'limit'>('limit');
  const [orderSide, setOrderSide] = useState<'buy' | 'sell'>('buy');
  const [orderAmount, setOrderAmount] = useState('');
  const [orderPrice, setOrderPrice] = useState('');

  useEffect(() => {
    loadTradingData();
    loadUserBalance();
    
    // Set up real-time updates (mock for now)
    const interval = setInterval(() => {
      updateMarketData();
    }, 5000);
    
    return () => clearInterval(interval);
  }, [selectedPair]);

  const loadTradingData = async () => {
    try {
      // Load trading pairs from API
      const response = await fetch('http://localhost:8000/api/trading/pairs/');
      if (response.ok) {
        const pairs = await response.json();
        setTradingPairs(pairs);
        if (!selectedPair && pairs.length > 0) {
          setSelectedPair(pairs[0]);
        }
      } else {
        // Fallback to mock data
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
          },
          {
            id: 'ADA-USD',
            symbol: 'ADA/USD',
            base_currency: 'ADA',
            quote_currency: 'USD',
            current_price: 0.485,
            price_change_24h: 5.67,
            volume_24h: 125000,
            is_active: true
          }
        ];

        setTradingPairs(mockPairs);
        if (!selectedPair && mockPairs.length > 0) {
          setSelectedPair(mockPairs[0]);
        }
      }
      
      // Mock order book data
      setOrderBook({
        bids: [
          { price: 43245.50, amount: 0.5, total: 21622.75 },
          { price: 43240.25, amount: 1.2, total: 51888.30 },
          { price: 43235.00, amount: 0.8, total: 34588.00 },
          { price: 43230.75, amount: 2.1, total: 90784.58 },
          { price: 43225.50, amount: 0.3, total: 12967.65 }
        ],
        asks: [
          { price: 43255.75, amount: 0.7, total: 30279.03 },
          { price: 43260.00, amount: 1.5, total: 64890.00 },
          { price: 43265.25, amount: 0.9, total: 38938.73 },
          { price: 43270.50, amount: 1.8, total: 77886.90 },
          { price: 43275.75, amount: 0.4, total: 17310.30 }
        ]
      });
      
      // Mock recent trades
      setRecentTrades([
        { id: 1, price: 43250.50, amount: 0.25, side: 'buy', timestamp: new Date().toISOString() },
        { id: 2, price: 43248.75, amount: 0.15, side: 'sell', timestamp: new Date().toISOString() },
        { id: 3, price: 43252.00, amount: 0.35, side: 'buy', timestamp: new Date().toISOString() },
        { id: 4, price: 43247.25, amount: 0.20, side: 'sell', timestamp: new Date().toISOString() },
        { id: 5, price: 43251.50, amount: 0.45, side: 'buy', timestamp: new Date().toISOString() }
      ]);
      
    } catch (error) {
      console.error('Failed to load trading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadUserBalance = async () => {
    try {
      const token = localStorage.getItem('token') || localStorage.getItem('auth_token');
      const response = await fetch('http://localhost:8000/api/balance/', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        setUserBalance(data.balance);
      }
    } catch (error) {
      console.error('Failed to load user balance:', error);
    }
  };

  const updateMarketData = () => {
    // Mock real-time price updates
    if (selectedPair) {
      const priceChange = (Math.random() - 0.5) * 10; // Random price change
      setSelectedPair(prev => prev ? {
        ...prev,
        current_price: prev.current_price + priceChange
      } : null);
    }
  };

  const handlePlaceOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedPair) {
      alert('Please select a trading pair');
      return;
    }
    
    try {
      const token = localStorage.getItem('token') || localStorage.getItem('auth_token');
      const orderData = {
        trading_pair: selectedPair.id,
        order_type: orderType,
        side: orderSide,
        amount: parseFloat(orderAmount),
        price: orderType === 'limit' ? parseFloat(orderPrice) : selectedPair.current_price
      };
      
      const response = await fetch('http://localhost:8000/api/trades/trading/orders/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(orderData),
      });
      
      if (response.ok) {
        alert('Order placed successfully!');
        setOrderAmount('');
        setOrderPrice('');
        loadUserBalance();
      } else {
        const error = await response.json();
        alert(`Error: ${error.error || 'Failed to place order'}`);
      }
    } catch (error) {
      console.error('Order placement error:', error);
      alert('Failed to place order');
    }
  };

  const formatCurrency = (amount: number, decimals: number = 2) => {
    return new Intl.NumberFormat('en-US', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    }).format(amount);
  };

  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-darkmode pt-32 pb-16">
        <div className="container mx-auto max-w-7xl px-4">
          <div className="text-center">
            <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary mx-auto"></div>
            <p className="text-white mt-4">Loading trading data...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-darkmode pt-32 pb-16">
      <div className="container mx-auto max-w-7xl px-4">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-4 mb-6">
            <div className="w-16 h-16 bg-primary bg-opacity-20 rounded-full flex items-center justify-center">
              <Icon icon="tabler:chart-candle" width="32" height="32" className="text-primary" />
            </div>
            <div>
              <h1 className="text-white text-4xl font-bold mb-2">Spot Trading</h1>
              <p className="text-muted text-lg">Trade cryptocurrencies with real-time market data</p>
            </div>
          </div>
          
          {/* Trading Status Indicator */}
          <div className="flex items-center gap-2 mb-4">
            <div className="w-3 h-3 bg-success rounded-full animate-pulse"></div>
            <span className="text-success text-sm font-medium">Live Trading Active</span>
            <span className="text-muted text-sm">•</span>
            <span className="text-muted text-sm">Real-time data feed connected</span>
          </div>
        </div>

        {/* Trading Pairs Selector */}
        <div className="bg-dark_grey rounded-lg p-6 mb-6">
          <h2 className="text-white text-xl font-semibold mb-4">Trading Pairs</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {tradingPairs.map((pair) => (
              <button
                key={pair.id}
                onClick={() => setSelectedPair(pair)}
                className={`p-4 rounded-lg border transition-all ${
                  selectedPair?.id === pair.id
                    ? 'border-primary bg-primary bg-opacity-10'
                    : 'border-dark_border hover:border-primary'
                }`}
              >
                <div className="text-left">
                  <p className="text-white font-semibold">{pair.symbol}</p>
                  <p className="text-primary text-lg font-bold">
                    ${formatCurrency(pair.current_price, 2)}
                  </p>
                  <p className={`text-sm ${
                    pair.price_change_24h >= 0 ? 'text-success' : 'text-error'
                  }`}>
                    {pair.price_change_24h >= 0 ? '+' : ''}{pair.price_change_24h.toFixed(2)}%
                  </p>
                </div>
              </button>
            ))}
          </div>
        </div>

        {selectedPair && (
          <div className="grid lg:grid-cols-3 gap-6">
            {/* Order Book & Recent Trades */}
            <div className="lg:col-span-1 space-y-6">
              {/* Order Book */}
              <div className="bg-dark_grey rounded-lg p-6">
                <h3 className="text-white text-lg font-semibold mb-4">Order Book</h3>
                
                {/* Asks (Sell Orders) */}
                <div className="mb-4">
                  <div className="grid grid-cols-3 gap-2 text-muted text-sm mb-2">
                    <span>Price (USD)</span>
                    <span>Amount ({selectedPair.base_currency})</span>
                    <span>Total (USD)</span>
                  </div>
                  {orderBook.asks.reverse().map((ask, index) => (
                    <div key={`ask-${index}`} className="grid grid-cols-3 gap-2 text-sm py-1">
                      <span className="text-error">${formatCurrency(ask.price, 2)}</span>
                      <span className="text-white">{ask.amount}</span>
                      <span className="text-muted">${formatCurrency(ask.total, 2)}</span>
                    </div>
                  ))}
                </div>
                
                {/* Current Price */}
                <div className="text-center py-2 border-t border-b border-dark_border mb-4">
                  <span className="text-primary text-lg font-bold">
                    ${formatCurrency(selectedPair.current_price, 2)}
                  </span>
                </div>
                
                {/* Bids (Buy Orders) */}
                <div>
                  {orderBook.bids.map((bid, index) => (
                    <div key={`bid-${index}`} className="grid grid-cols-3 gap-2 text-sm py-1">
                      <span className="text-success">${formatCurrency(bid.price, 2)}</span>
                      <span className="text-white">{bid.amount}</span>
                      <span className="text-muted">${formatCurrency(bid.total, 2)}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recent Trades */}
              <div className="bg-dark_grey rounded-lg p-6">
                <h3 className="text-white text-lg font-semibold mb-4">Recent Trades</h3>
                <div className="space-y-2">
                  <div className="grid grid-cols-3 gap-2 text-muted text-sm">
                    <span>Price</span>
                    <span>Amount</span>
                    <span>Time</span>
                  </div>
                  {recentTrades.map((trade) => (
                    <div key={trade.id} className="grid grid-cols-3 gap-2 text-sm">
                      <span className={trade.side === 'buy' ? 'text-success' : 'text-error'}>
                        ${formatCurrency(trade.price, 2)}
                      </span>
                      <span className="text-white">{trade.amount}</span>
                      <span className="text-muted">{formatTime(trade.timestamp)}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Trading Interface */}
            <div className="lg:col-span-2">
              {/* Price Chart Placeholder */}
              <div className="bg-dark_grey rounded-lg p-6 mb-6">
                <h3 className="text-white text-lg font-semibold mb-4">
                  {selectedPair.symbol} Price Chart
                </h3>
                <div className="h-64 bg-darkmode rounded-lg flex items-center justify-center">
                  <div className="text-center">
                    <Icon icon="tabler:chart-line" width="64" height="64" className="text-muted mx-auto mb-4" />
                    <p className="text-muted">Advanced charting coming soon</p>
                    <p className="text-primary text-2xl font-bold mt-4">
                      ${formatCurrency(selectedPair.current_price, 2)}
                    </p>
                  </div>
                </div>
              </div>

              {/* Order Form */}
              <div className="bg-dark_grey rounded-lg p-6">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-white text-lg font-semibold">Place Order</h3>
                  <div className="text-muted text-sm">
                    Balance: ${formatCurrency(userBalance, 2)}
                  </div>
                </div>

                <form onSubmit={handlePlaceOrder} className="space-y-6">
                  {/* Order Type & Side */}
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-white text-sm font-medium mb-2">
                        Order Type
                      </label>
                      <select
                        value={orderType}
                        onChange={(e) => setOrderType(e.target.value as 'market' | 'limit')}
                        className="w-full px-4 py-3 bg-darkmode border border-dark_border rounded-lg text-white focus:outline-none focus:border-primary"
                      >
                        <option value="limit">Limit Order</option>
                        <option value="market">Market Order</option>
                      </select>
                    </div>
                    
                    <div>
                      <label className="block text-white text-sm font-medium mb-2">
                        Side
                      </label>
                      <div className="grid grid-cols-2 gap-2">
                        <button
                          type="button"
                          onClick={() => setOrderSide('buy')}
                          className={`py-3 px-4 rounded-lg font-medium transition-all ${
                            orderSide === 'buy'
                              ? 'bg-success text-white'
                              : 'bg-darkmode text-muted border border-dark_border hover:border-success'
                          }`}
                        >
                          Buy
                        </button>
                        <button
                          type="button"
                          onClick={() => setOrderSide('sell')}
                          className={`py-3 px-4 rounded-lg font-medium transition-all ${
                            orderSide === 'sell'
                              ? 'bg-error text-white'
                              : 'bg-darkmode text-muted border border-dark_border hover:border-error'
                          }`}
                        >
                          Sell
                        </button>
                      </div>
                    </div>
                  </div>

                  {/* Price (for limit orders) */}
                  {orderType === 'limit' && (
                    <div>
                      <label className="block text-white text-sm font-medium mb-2">
                        Price (USD)
                      </label>
                      <input
                        type="number"
                        step="0.01"
                        value={orderPrice}
                        onChange={(e) => setOrderPrice(e.target.value)}
                        placeholder={`${selectedPair.current_price}`}
                        className="w-full px-4 py-3 bg-darkmode border border-dark_border rounded-lg text-white focus:outline-none focus:border-primary"
                        required
                      />
                    </div>
                  )}

                  {/* Amount */}
                  <div>
                    <label className="block text-white text-sm font-medium mb-2">
                      Amount ({selectedPair.base_currency})
                    </label>
                    <input
                      type="number"
                      step="0.00000001"
                      value={orderAmount}
                      onChange={(e) => setOrderAmount(e.target.value)}
                      placeholder="0.00000000"
                      className="w-full px-4 py-3 bg-darkmode border border-dark_border rounded-lg text-white focus:outline-none focus:border-primary"
                      required
                    />
                  </div>

                  {/* Total */}
                  {orderAmount && (orderPrice || orderType === 'market') && (
                    <div className="bg-darkmode p-4 rounded-lg">
                      <div className="flex justify-between text-sm">
                        <span className="text-muted">Total:</span>
                        <span className="text-white font-medium">
                          ${formatCurrency(
                            parseFloat(orderAmount) * 
                            (orderType === 'limit' ? parseFloat(orderPrice || '0') : selectedPair.current_price),
                            2
                          )}
                        </span>
                      </div>
                    </div>
                  )}

                  {/* Submit Button */}
                  <button
                    type="submit"
                    className={`w-full py-3 px-6 rounded-lg font-semibold transition-all ${
                      orderSide === 'buy'
                        ? 'bg-success hover:bg-opacity-90 text-white'
                        : 'bg-error hover:bg-opacity-90 text-white'
                    }`}
                  >
                    {orderSide === 'buy' ? 'Buy' : 'Sell'} {selectedPair.base_currency}
                  </button>
                </form>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

"use client";

import React, { useState, useEffect } from 'react';
import { Icon } from "@iconify/react";
import { authService } from '@/services/authService';

interface Trade {
  id: number;
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
}

interface OngoingTradesProps {
  refreshTrigger?: number;
}

export default function OngoingTrades({ refreshTrigger = 0 }: OngoingTradesProps) {
  const [trades, setTrades] = useState<Trade[]>([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState(true);

  useEffect(() => {
    loadOngoingTrades();
    
    // Auto-refresh every 5 seconds
    const interval = setInterval(() => {
      loadOngoingTrades();
    }, 5000);
    
    return () => clearInterval(interval);
  }, [refreshTrigger]);

  const loadOngoingTrades = async () => {
    try {
      const response = await authService.makeAuthenticatedRequest(
        'http://localhost:8000/api/trading/history/'
      );
      
      if (response.ok) {
        const data = await response.json();
        // Get only recent trades (last 10)
        const recentTrades = (data.results || data).slice(0, 10);
        setTrades(recentTrades);
      }
    } catch (error) {
      console.error('Failed to load trades:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    
    if (seconds < 60) return `${seconds}s ago`;
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    return date.toLocaleDateString();
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'executed': return 'text-success';
      case 'pending': return 'text-warning';
      case 'cancelled': return 'text-muted';
      case 'failed': return 'text-error';
      default: return 'text-white';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'executed': return 'tabler:check-circle';
      case 'pending': return 'tabler:clock';
      case 'cancelled': return 'tabler:x-circle';
      case 'failed': return 'tabler:alert-circle';
      default: return 'tabler:circle';
    }
  };

  const getPnLColor = (pnl: number) => {
    if (pnl > 0) return 'text-success';
    if (pnl < 0) return 'text-error';
    return 'text-muted';
  };

  return (
    <div className="bg-dark_grey rounded-lg overflow-hidden">
      {/* Header */}
      <div 
        className="flex items-center justify-between p-4 border-b border-dark_border cursor-pointer hover:bg-darkmode transition-colors"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-primary bg-opacity-20 rounded-lg flex items-center justify-center">
            <Icon icon="tabler:chart-line" width="20" height="20" className="text-primary" />
          </div>
          <div>
            <h3 className="text-white font-semibold text-lg">Ongoing Trades</h3>
            <p className="text-muted text-sm">{trades.length} active positions</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-success rounded-full animate-pulse"></div>
            <span className="text-success text-xs">Live</span>
          </div>
          <Icon 
            icon={expanded ? "tabler:chevron-up" : "tabler:chevron-down"} 
            width="24" 
            height="24" 
            className="text-muted"
          />
        </div>
      </div>

      {/* Trades List */}
      {expanded && (
        <div className="max-h-96 overflow-y-auto">
          {loading ? (
            <div className="p-8 text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-2"></div>
              <p className="text-muted text-sm">Loading trades...</p>
            </div>
          ) : trades.length === 0 ? (
            <div className="p-8 text-center">
              <Icon icon="tabler:inbox" width="48" height="48" className="text-muted mx-auto mb-3" />
              <p className="text-muted">No active trades</p>
              <p className="text-muted text-sm mt-1">Your trades will appear here</p>
            </div>
          ) : (
            <div className="divide-y divide-dark_border">
              {trades.map((trade) => (
                <div 
                  key={trade.id} 
                  className="p-4 hover:bg-darkmode transition-colors"
                >
                  <div className="flex items-start justify-between mb-2">
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
                      
                      {/* Cryptocurrency */}
                      <div>
                        <p className="text-white font-semibold">{trade.cryptocurrency_symbol}</p>
                        <p className="text-muted text-xs">{formatTime(trade.created_at)}</p>
                      </div>
                    </div>
                    
                    {/* Status */}
                    <div className="flex items-center gap-2">
                      <Icon 
                        icon={getStatusIcon(trade.status)} 
                        width="16" 
                        height="16" 
                        className={getStatusColor(trade.status)}
                      />
                      <span className={`text-xs font-medium ${getStatusColor(trade.status)}`}>
                        {trade.status}
                      </span>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-3">
                    {/* Amount */}
                    <div>
                      <p className="text-muted text-xs mb-1">Amount</p>
                      <p className="text-white text-sm font-medium">
                        {trade.amount.toFixed(8)}
                      </p>
                    </div>
                    
                    {/* Price */}
                    <div>
                      <p className="text-muted text-xs mb-1">Price</p>
                      <p className="text-white text-sm font-medium">
                        ${trade.price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                      </p>
                    </div>
                    
                    {/* Leverage */}
                    {trade.leverage > 1 && (
                      <div>
                        <p className="text-muted text-xs mb-1">Leverage</p>
                        <p className="text-primary text-sm font-medium">
                          {trade.leverage}x
                        </p>
                      </div>
                    )}
                    
                    {/* P&L */}
                    <div>
                      <p className="text-muted text-xs mb-1">P&L</p>
                      <p className={`text-sm font-semibold ${getPnLColor(trade.pnl)}`}>
                        {trade.pnl >= 0 ? '+' : ''}${trade.pnl.toFixed(2)}
                      </p>
                    </div>
                    
                    {/* Total Value */}
                    <div>
                      <p className="text-muted text-xs mb-1">Total</p>
                      <p className="text-white text-sm font-medium">
                        ${trade.total_value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                      </p>
                    </div>
                  </div>
                  
                  {/* Fees */}
                  {trade.fees > 0 && (
                    <div className="mt-2 text-xs text-muted">
                      Fee: ${trade.fees.toFixed(4)}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}


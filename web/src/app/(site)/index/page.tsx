"use client";

import { Icon } from "@iconify/react";
import Link from "next/link";
import { useRouter } from 'next/navigation';
import { useState, useEffect } from 'react';
import { authService } from '@/services/authService';

export default function IndexPage() {
  const router = useRouter();
  const [userBalance, setUserBalance] = useState(0);
  
  useEffect(() => {
    loadUserBalance();
  }, []);

  const loadUserBalance = async () => {
    try {
      const token = authService.getAccessToken();
      if (!token) {
        // Don't redirect immediately, just set balance to 0
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
      // If authService throws an error, it means refresh failed too
      setUserBalance(0);
    }
  };

  return (
    <div className="min-h-screen bg-darkmode pt-32 pb-16">
      <div className="container mx-auto lg:max-w-screen-2xl px-4">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <div className="w-24 h-24 bg-gradient-to-r from-primary via-purple-500 to-warning rounded-full flex items-center justify-center mx-auto mb-6 animate-pulse">
              <Icon icon="tabler:chart-dots" width="48" height="48" className="text-white" />
            </div>
            <h1 className="text-white text-5xl font-bold mb-4">High-Risk Trading Index</h1>
            <p className="text-muted text-xl">
              Advanced strategies for experienced traders seeking maximum profit potential
            </p>
            <div className="mt-6 inline-block bg-dark_grey rounded-lg px-8 py-4">
              <p className="text-muted text-sm mb-1">Your Available Balance</p>
              <p className="text-white text-3xl font-bold">${userBalance.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
            </div>
          </div>

          {/* Risk Warning */}
          <div className="bg-gradient-to-r from-error/10 via-warning/10 to-error/10 border-2 border-error/40 rounded-xl p-6 mb-12 animate-pulse">
            <div className="flex items-center justify-center gap-4">
              <Icon icon="tabler:alert-triangle" width="32" height="32" className="text-error" />
              <div className="text-center">
                <h3 className="text-error font-bold text-xl mb-2">⚠️ EXTREME RISK WARNING ⚠️</h3>
                <p className="text-muted">
                  These trading strategies can result in significant losses. Only trade with capital you can afford to lose.
                </p>
              </div>
              <Icon icon="tabler:alert-triangle" width="32" height="32" className="text-error" />
            </div>
          </div>

          {/* Trading Strategy Cards */}
          <div className="grid md:grid-cols-3 gap-8 mb-12">
            {/* Advanced Orders Card */}
            <Link href="/index/advanced-orders" className="group">
              <div className="relative bg-gradient-to-br from-error/20 via-dark_grey to-darkmode rounded-xl p-8 border-2 border-error/30 hover:border-error/60 transition-all duration-300 group-hover:scale-105 h-full">
                <div className="absolute top-4 right-4">
                  <span className="bg-error text-white text-xs font-bold px-3 py-1 rounded-full">HIGHEST RISK</span>
                </div>
                
                <div className="w-16 h-16 bg-error bg-opacity-20 rounded-full flex items-center justify-center mb-6">
                  <Icon icon="tabler:alert-triangle" width="32" height="32" className="text-error" />
                </div>
                
                <h2 className="text-white text-2xl font-bold mb-4">Advanced Orders</h2>
                
                <div className="space-y-3 mb-6">
                  <div className="flex items-center gap-2 text-sm">
                    <Icon icon="tabler:check" width="16" height="16" className="text-error" />
                    <span className="text-muted">Stop Loss Orders</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <Icon icon="tabler:check" width="16" height="16" className="text-error" />
                    <span className="text-muted">Trailing Stop</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <Icon icon="tabler:check" width="16" height="16" className="text-error" />
                    <span className="text-muted">Stop Limit</span>
                  </div>
                </div>
                
                <div className="bg-error/10 border border-error/20 rounded-lg p-4 mb-6">
                  <p className="text-error text-xs font-semibold">Auto-executes during volatility</p>
                </div>
                
                <div className="flex items-center justify-between text-primary group-hover:text-primary/80 transition-colors">
                  <span className="font-semibold">Start Trading</span>
                  <Icon icon="tabler:arrow-right" width="20" height="20" />
                </div>
              </div>
            </Link>

            {/* Automated Strategies Card */}
            <Link href="/index/automated-strategies" className="group">
              <div className="relative bg-gradient-to-br from-warning/20 via-dark_grey to-darkmode rounded-xl p-8 border-2 border-warning/30 hover:border-warning/60 transition-all duration-300 group-hover:scale-105 h-full">
                <div className="absolute top-4 right-4">
                  <span className="bg-warning text-white text-xs font-bold px-3 py-1 rounded-full">HIGH RISK</span>
                </div>
                
                <div className="w-16 h-16 bg-warning bg-opacity-20 rounded-full flex items-center justify-center mb-6">
                  <Icon icon="tabler:robot" width="32" height="32" className="text-warning" />
                </div>
                
                <h2 className="text-white text-2xl font-bold mb-4">Automated Strategies</h2>
                
                <div className="space-y-3 mb-6">
                  <div className="flex items-center gap-2 text-sm">
                    <Icon icon="tabler:check" width="16" height="16" className="text-warning" />
                    <span className="text-muted">Arbitrage Trading</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <Icon icon="tabler:check" width="16" height="16" className="text-warning" />
                    <span className="text-muted">Momentum Strategy</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <Icon icon="tabler:check" width="16" height="16" className="text-warning" />
                    <span className="text-muted">Grid Trading</span>
                  </div>
                </div>
                
                <div className="bg-warning/10 border border-warning/20 rounded-lg p-4 mb-6">
                  <p className="text-warning text-xs font-semibold">24/7 AI-powered execution</p>
                </div>
                
                <div className="flex items-center justify-between text-primary group-hover:text-primary/80 transition-colors">
                  <span className="font-semibold">Start Trading</span>
                  <Icon icon="tabler:arrow-right" width="20" height="20" />
                </div>
              </div>
            </Link>

            {/* Leverage Trading Card */}
            <Link href="/index/leverage-trading" className="group">
              <div className="relative bg-gradient-to-br from-success/20 via-dark_grey to-darkmode rounded-xl p-8 border-2 border-success/30 hover:border-success/60 transition-all duration-300 group-hover:scale-105 h-full">
                <div className="absolute top-4 right-4">
                  <span className="bg-gradient-to-r from-success to-primary text-white text-xs font-bold px-3 py-1 rounded-full">UP TO 100x</span>
                </div>
                
                <div className="w-16 h-16 bg-success bg-opacity-20 rounded-full flex items-center justify-center mb-6">
                  <Icon icon="tabler:trending-up" width="32" height="32" className="text-success" />
                </div>
                
                <h2 className="text-white text-2xl font-bold mb-4">Leverage Trading</h2>
                
                <div className="space-y-3 mb-6">
                  <div className="flex items-center gap-2 text-sm">
                    <Icon icon="tabler:check" width="16" height="16" className="text-success" />
                    <span className="text-muted">1x - 100x Leverage</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <Icon icon="tabler:check" width="16" height="16" className="text-success" />
                    <span className="text-muted">Long & Short Positions</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <Icon icon="tabler:check" width="16" height="16" className="text-success" />
                    <span className="text-muted">Margin Trading</span>
                  </div>
                </div>
                
                <div className="bg-success/10 border border-success/20 rounded-lg p-4 mb-6">
                  <p className="text-success text-xs font-semibold">Amplify profits & losses</p>
                </div>
                
                <div className="flex items-center justify-between text-primary group-hover:text-primary/80 transition-colors">
                  <span className="font-semibold">Start Trading</span>
                  <Icon icon="tabler:arrow-right" width="20" height="20" />
                </div>
              </div>
            </Link>
          </div>

          {/* Quick Stats */}
          <div className="grid md:grid-cols-4 gap-6 mb-12">
            <div className="bg-dark_grey rounded-lg p-6 text-center">
              <Icon icon="tabler:chart-line" width="32" height="32" className="text-primary mx-auto mb-3" />
              <p className="text-white text-2xl font-bold mb-1">30-50%</p>
              <p className="text-muted text-sm">Potential Monthly ROI</p>
            </div>
            <div className="bg-dark_grey rounded-lg p-6 text-center">
              <Icon icon="tabler:clock" width="32" height="32" className="text-warning mx-auto mb-3" />
              <p className="text-white text-2xl font-bold mb-1">24/7</p>
              <p className="text-muted text-sm">Market Access</p>
            </div>
            <div className="bg-dark_grey rounded-lg p-6 text-center">
              <Icon icon="tabler:bolt" width="32" height="32" className="text-success mx-auto mb-3" />
              <p className="text-white text-2xl font-bold mb-1">&lt;1ms</p>
              <p className="text-muted text-sm">Execution Speed</p>
            </div>
            <div className="bg-dark_grey rounded-lg p-6 text-center">
              <Icon icon="tabler:shield-check" width="32" height="32" className="text-primary mx-auto mb-3" />
              <p className="text-white text-2xl font-bold mb-1">100%</p>
              <p className="text-muted text-sm">Secure Platform</p>
            </div>
          </div>

          {/* Bottom CTA */}
          <div className="bg-gradient-to-r from-primary via-purple-600 to-warning rounded-xl p-8 text-center">
            <h3 className="text-white text-3xl font-bold mb-4">Ready to Maximize Your Profits?</h3>
            <p className="text-white/80 text-lg mb-6">
              Choose your trading strategy and start trading with advanced features
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                href="/index/advanced-orders" 
                className="bg-white text-primary px-8 py-4 rounded-lg font-bold hover:bg-opacity-90 transition-all flex items-center justify-center gap-2"
              >
                <Icon icon="tabler:alert-triangle" width="20" height="20" />
                Advanced Orders
              </Link>
              <Link 
                href="/index/automated-strategies" 
                className="bg-white text-primary px-8 py-4 rounded-lg font-bold hover:bg-opacity-90 transition-all flex items-center justify-center gap-2"
              >
                <Icon icon="tabler:robot" width="20" height="20" />
                Automated Strategies
              </Link>
              <Link 
                href="/index/leverage-trading" 
                className="bg-white text-primary px-8 py-4 rounded-lg font-bold hover:bg-opacity-90 transition-all flex items-center justify-center gap-2"
              >
                <Icon icon="tabler:trending-up" width="20" height="20" />
                Leverage Trading
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
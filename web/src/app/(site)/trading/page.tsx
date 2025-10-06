import { Metadata } from "next";
import { Icon } from "@iconify/react";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Spot Trading | Fluxor",
  description: "Trade cryptocurrencies instantly with Fluxor's advanced spot trading platform",
};

export default function SpotTradingPage() {
  return (
    <div className="min-h-screen bg-darkmode pt-32 pb-16">
      <div className="container mx-auto lg:max-w-screen-xl px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-white text-4xl font-bold mb-8">Spot Trading</h1>
          
          <div className="prose prose-invert max-w-none">
            <p className="text-muted text-lg mb-8">
              Trade cryptocurrencies instantly with Fluxor's advanced spot trading platform. Buy and sell digital assets at current market prices with institutional-grade security and lightning-fast execution.
            </p>

            <div className="grid md:grid-cols-2 gap-8 mb-12">
              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:chart-candle" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Advanced Charts</h3>
                </div>
                <p className="text-muted">
                  Professional trading charts with technical indicators, drawing tools, and real-time market data to help you make informed trading decisions.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:zap" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Lightning Fast</h3>
                </div>
                <p className="text-muted">
                  Execute trades in milliseconds with our high-performance trading engine and low-latency infrastructure.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:shield-check" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Bank-Level Security</h3>
                </div>
                <p className="text-muted">
                  Your funds are protected with institutional-grade security measures including cold storage and multi-signature wallets.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:coins" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Wide Selection</h3>
                </div>
                <p className="text-muted">
                  Trade over 200+ cryptocurrencies including Bitcoin, Ethereum, and emerging altcoins with competitive spreads.
                </p>
              </div>
            </div>

            <div className="bg-gradient-to-r from-primary to-charcoalGray rounded-lg p-8 text-center mb-12">
              <h3 className="text-white text-2xl font-semibold mb-4">Start Trading Today</h3>
              <p className="text-muted mb-6">
                Join thousands of traders who trust Fluxor for their cryptocurrency trading needs.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link 
                  href="/signup" 
                  className="bg-white text-primary px-6 py-3 rounded-lg font-semibold hover:bg-opacity-90 transition-all"
                >
                  Create Account
                </Link>
                <Link 
                  href="/signin" 
                  className="border border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white hover:text-primary transition-all"
                >
                  Sign In
                </Link>
              </div>
            </div>

            <div className="space-y-8">
              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">Trading Features</h2>
                <ul className="text-muted list-disc list-inside space-y-2">
                  <li>Real-time market data and price feeds</li>
                  <li>Advanced order types (Market, Limit, Stop-Loss)</li>
                  <li>Professional trading interface</li>
                  <li>Mobile and desktop trading platforms</li>
                  <li>24/7 customer support</li>
                  <li>Low trading fees starting from 0.1%</li>
                </ul>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">Supported Cryptocurrencies</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {['Bitcoin (BTC)', 'Ethereum (ETH)', 'Binance Coin (BNB)', 'Cardano (ADA)', 'Solana (SOL)', 'XRP (XRP)', 'Polkadot (DOT)', 'Dogecoin (DOGE)'].map((coin) => (
                    <div key={coin} className="bg-dark_grey bg-opacity-30 rounded-lg p-3 text-center">
                      <span className="text-white text-sm">{coin}</span>
                    </div>
                  ))}
                </div>
              </section>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

import { Metadata } from "next";
import { Icon } from "@iconify/react";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Futures Trading | Fluxor",
  description: "Trade cryptocurrency futures with up to 100x leverage on Fluxor's advanced derivatives platform",
};

export default function FuturesTradingPage() {
  return (
    <div className="min-h-screen bg-darkmode pt-32 pb-16">
      <div className="container mx-auto lg:max-w-screen-xl px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-white text-4xl font-bold mb-8">Futures Trading</h1>
          
          <div className="prose prose-invert max-w-none">
            <p className="text-muted text-lg mb-8">
              Trade cryptocurrency futures with up to 100x leverage on Fluxor's advanced derivatives platform. Profit from both rising and falling markets with sophisticated risk management tools.
            </p>

            <div className="grid md:grid-cols-2 gap-8 mb-12">
              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:trending-up" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">High Leverage</h3>
                </div>
                <p className="text-muted">
                  Trade with up to 100x leverage to maximize your potential profits while maintaining strict risk controls.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:arrows-sort" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Long & Short</h3>
                </div>
                <p className="text-muted">
                  Profit from both rising and falling markets. Go long to profit from price increases or short to profit from price decreases.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:shield-check" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Risk Management</h3>
                </div>
                <p className="text-muted">
                  Advanced risk management tools including stop-loss, take-profit, and position sizing to protect your capital.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:chart-line" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Advanced Analytics</h3>
                </div>
                <p className="text-muted">
                  Comprehensive analytics and performance metrics to track your trading performance and optimize strategies.
                </p>
              </div>
            </div>

            <div className="bg-gradient-to-r from-primary to-charcoalGray rounded-lg p-8 text-center mb-12">
              <h3 className="text-white text-2xl font-semibold mb-4">Start Futures Trading</h3>
              <p className="text-muted mb-6">
                Access professional-grade futures trading tools with institutional-level security.
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
                <h2 className="text-white text-2xl font-semibold mb-4">Futures Features</h2>
                <ul className="text-muted list-disc list-inside space-y-2">
                  <li>Up to 100x leverage on major cryptocurrencies</li>
                  <li>Perpetual futures contracts with no expiration</li>
                  <li>Advanced order types and execution algorithms</li>
                  <li>Real-time P&L tracking and risk monitoring</li>
                  <li>Cross-collateral support for multiple assets</li>
                  <li>Professional trading interface with custom layouts</li>
                </ul>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">Risk Warning</h2>
                <div className="bg-red-900 bg-opacity-20 border border-red-500 rounded-lg p-6">
                  <p className="text-red-300">
                    <strong>High Risk:</strong> Futures trading involves significant risk and may not be suitable for all investors. 
                    Leverage can amplify both gains and losses. Please ensure you understand the risks involved and only trade 
                    with capital you can afford to lose.
                  </p>
                </div>
              </section>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

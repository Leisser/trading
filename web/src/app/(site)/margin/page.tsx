import { Metadata } from "next";
import { Icon } from "@iconify/react";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Margin Trading | Fluxor",
  description: "Trade cryptocurrencies with borrowed funds using Fluxor's margin trading platform",
};

export default function MarginTradingPage() {
  return (
    <div className="min-h-screen bg-darkmode pt-32 pb-16">
      <div className="container mx-auto lg:max-w-screen-xl px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-white text-4xl font-bold mb-8">Margin Trading</h1>
          
          <div className="prose prose-invert max-w-none">
            <p className="text-muted text-lg mb-8">
              Trade cryptocurrencies with borrowed funds using Fluxor's margin trading platform. Increase your buying power and potential profits with flexible leverage options.
            </p>

            <div className="grid md:grid-cols-2 gap-8 mb-12">
              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:scale" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Flexible Leverage</h3>
                </div>
                <p className="text-muted">
                  Choose from 2x to 10x leverage depending on your risk tolerance and trading strategy.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:calculator" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Interest Calculator</h3>
                </div>
                <p className="text-muted">
                  Transparent interest rates with real-time calculation tools to help you manage borrowing costs.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:alert-triangle" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Liquidation Protection</h3>
                </div>
                <p className="text-muted">
                  Advanced risk management with automatic liquidation protection and margin call alerts.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:wallet" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Cross-Collateral</h3>
                </div>
                <p className="text-muted">
                  Use multiple cryptocurrencies as collateral to maximize your borrowing power and flexibility.
                </p>
              </div>
            </div>

            <div className="bg-gradient-to-r from-primary to-charcoalGray rounded-lg p-8 text-center mb-12">
              <h3 className="text-white text-2xl font-semibold mb-4">Start Margin Trading</h3>
              <p className="text-muted mb-6">
                Access professional margin trading tools with competitive interest rates and flexible terms.
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
                <h2 className="text-white text-2xl font-semibold mb-4">Margin Trading Features</h2>
                <ul className="text-muted list-disc list-inside space-y-2">
                  <li>2x to 10x leverage on major cryptocurrencies</li>
                  <li>Competitive interest rates starting from 0.02% daily</li>
                  <li>Cross-collateral support for multiple assets</li>
                  <li>Real-time margin ratio monitoring</li>
                  <li>Automatic liquidation protection</li>
                  <li>Flexible repayment options</li>
                </ul>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">How It Works</h2>
                <div className="grid md:grid-cols-3 gap-6">
                  <div className="text-center">
                    <div className="bg-primary bg-opacity-20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                      <span className="text-primary text-2xl font-bold">1</span>
                    </div>
                    <h3 className="text-white font-semibold mb-2">Deposit Collateral</h3>
                    <p className="text-muted text-sm">Deposit cryptocurrency as collateral to secure your margin loan.</p>
                  </div>
                  <div className="text-center">
                    <div className="bg-primary bg-opacity-20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                      <span className="text-primary text-2xl font-bold">2</span>
                    </div>
                    <h3 className="text-white font-semibold mb-2">Borrow Funds</h3>
                    <p className="text-muted text-sm">Borrow additional funds based on your collateral value and chosen leverage.</p>
                  </div>
                  <div className="text-center">
                    <div className="bg-primary bg-opacity-20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                      <span className="text-primary text-2xl font-bold">3</span>
                    </div>
                    <h3 className="text-white font-semibold mb-2">Trade & Repay</h3>
                    <p className="text-muted text-sm">Execute trades and repay the loan with interest when ready.</p>
                  </div>
                </div>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">Risk Warning</h2>
                <div className="bg-red-900 bg-opacity-20 border border-red-500 rounded-lg p-6">
                  <p className="text-red-300">
                    <strong>High Risk:</strong> Margin trading involves significant risk including the potential loss of your entire investment. 
                    Leverage amplifies both gains and losses. Please ensure you understand the risks and only trade with capital you can afford to lose.
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

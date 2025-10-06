import { Metadata } from "next";
import { Icon } from "@iconify/react";
import Link from "next/link";

export const metadata: Metadata = {
  title: "API Access | Fluxor",
  description: "Access Fluxor's powerful trading API for automated trading and integration",
};

export default function APIPage() {
  return (
    <div className="min-h-screen bg-darkmode pt-32 pb-16">
      <div className="container mx-auto lg:max-w-screen-xl px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-white text-4xl font-bold mb-8">API Access</h1>
          
          <div className="prose prose-invert max-w-none">
            <p className="text-muted text-lg mb-8">
              Access Fluxor's powerful trading API for automated trading, portfolio management, and seamless integration with your applications. Build sophisticated trading bots and applications with our comprehensive API.
            </p>

            <div className="grid md:grid-cols-2 gap-8 mb-12">
              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:code" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">REST API</h3>
                </div>
                <p className="text-muted">
                  Comprehensive REST API with full trading functionality, account management, and market data access.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:bolt" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">WebSocket API</h3>
                </div>
                <p className="text-muted">
                  Real-time data streams for market prices, order updates, and account changes with low latency.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:shield-check" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Secure Access</h3>
                </div>
                <p className="text-muted">
                  Industry-standard authentication with API keys, IP whitelisting, and rate limiting for security.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:book" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Documentation</h3>
                </div>
                <p className="text-muted">
                  Comprehensive documentation with code examples, SDKs, and interactive API explorer.
                </p>
              </div>
            </div>

            <div className="bg-gradient-to-r from-primary to-charcoalGray rounded-lg p-8 text-center mb-12">
              <h3 className="text-white text-2xl font-semibold mb-4">Get API Access</h3>
              <p className="text-muted mb-6">
                Start building with our powerful API and create sophisticated trading applications.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link 
                  href="/signup" 
                  className="bg-white text-primary px-6 py-3 rounded-lg font-semibold hover:bg-opacity-90 transition-all"
                >
                  Create Account
                </Link>
                <Link 
                  href="/documentation" 
                  className="border border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white hover:text-primary transition-all"
                >
                  View Documentation
                </Link>
              </div>
            </div>

            <div className="space-y-8">
              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">API Features</h2>
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="text-white text-lg font-semibold mb-3">Trading Operations</h3>
                    <ul className="text-muted list-disc list-inside space-y-1">
                      <li>Place and cancel orders</li>
                      <li>Manage positions and portfolios</li>
                      <li>Access order history and fills</li>
                      <li>Real-time balance updates</li>
                    </ul>
                  </div>
                  <div>
                    <h3 className="text-white text-lg font-semibold mb-3">Market Data</h3>
                    <ul className="text-muted list-disc list-inside space-y-1">
                      <li>Real-time price feeds</li>
                      <li>Order book data</li>
                      <li>Historical price data</li>
                      <li>Market statistics</li>
                    </ul>
                  </div>
                </div>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">Rate Limits</h2>
                <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                  <div className="grid md:grid-cols-3 gap-6 text-center">
                    <div>
                      <h3 className="text-white font-semibold mb-2">Public Endpoints</h3>
                      <p className="text-primary text-2xl font-bold">1000/min</p>
                      <p className="text-muted text-sm">Market data and public information</p>
                    </div>
                    <div>
                      <h3 className="text-white font-semibold mb-2">Private Endpoints</h3>
                      <p className="text-primary text-2xl font-bold">500/min</p>
                      <p className="text-muted text-sm">Account and trading operations</p>
                    </div>
                    <div>
                      <h3 className="text-white font-semibold mb-2">WebSocket</h3>
                      <p className="text-primary text-2xl font-bold">Unlimited</p>
                      <p className="text-muted text-sm">Real-time data streams</p>
                    </div>
                  </div>
                </div>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">SDKs & Libraries</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {['Python', 'JavaScript', 'Java', 'C#', 'Go', 'PHP', 'Ruby', 'Swift'].map((lang) => (
                    <div key={lang} className="bg-dark_grey bg-opacity-30 rounded-lg p-4 text-center">
                      <span className="text-white font-semibold">{lang}</span>
                    </div>
                  ))}
                </div>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">Getting Started</h2>
                <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                  <h3 className="text-white font-semibold mb-4">Quick Start Example</h3>
                  <pre className="bg-slate-900 rounded-lg p-4 text-sm overflow-x-auto">
                    <code className="text-green-400">
{`# Python Example
import requests

# Set your API credentials
api_key = "your_api_key"
api_secret = "your_api_secret"

# Get account balance
headers = {
    "X-API-Key": api_key,
    "X-API-Secret": api_secret
}

response = requests.get(
    "https://api.fluxor.pro/v1/account/balance",
    headers=headers
)

print(response.json())`}
                    </code>
                  </pre>
                </div>
              </section>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

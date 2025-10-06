import { Metadata } from "next";
import { Icon } from "@iconify/react";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Staking Rewards | Fluxor",
  description: "Earn passive income by staking your cryptocurrencies on Fluxor's secure staking platform",
};

export default function StakingPage() {
  return (
    <div className="min-h-screen bg-darkmode pt-32 pb-16">
      <div className="container mx-auto lg:max-w-screen-xl px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-white text-4xl font-bold mb-8">Staking Rewards</h1>
          
          <div className="prose prose-invert max-w-none">
            <p className="text-muted text-lg mb-8">
              Earn passive income by staking your cryptocurrencies on Fluxor's secure staking platform. Support blockchain networks while earning attractive rewards on your holdings.
            </p>

            <div className="grid md:grid-cols-2 gap-8 mb-12">
              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:coins" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">High APY</h3>
                </div>
                <p className="text-muted">
                  Earn up to 12% APY on supported cryptocurrencies with competitive staking rewards.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:shield-check" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Secure Staking</h3>
                </div>
                <p className="text-muted">
                  Your staked assets are protected with institutional-grade security and insurance coverage.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:clock" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Flexible Terms</h3>
                </div>
                <p className="text-muted">
                  Choose from flexible staking terms ranging from 7 days to 1 year with different reward rates.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:chart-line" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Auto-Compound</h3>
                </div>
                <p className="text-muted">
                  Automatically compound your staking rewards to maximize your earning potential over time.
                </p>
              </div>
            </div>

            <div className="bg-gradient-to-r from-primary to-charcoalGray rounded-lg p-8 text-center mb-12">
              <h3 className="text-white text-2xl font-semibold mb-4">Start Staking Today</h3>
              <p className="text-muted mb-6">
                Begin earning passive income on your cryptocurrency holdings with our secure staking platform.
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
                <h2 className="text-white text-2xl font-semibold mb-4">Supported Staking Assets</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {[
                    { coin: 'Ethereum (ETH)', apy: '5.2%', term: 'Flexible' },
                    { coin: 'Cardano (ADA)', apy: '4.8%', term: '30 days' },
                    { coin: 'Solana (SOL)', apy: '7.2%', term: '7 days' },
                    { coin: 'Polkadot (DOT)', apy: '12.0%', term: '90 days' },
                    { coin: 'Cosmos (ATOM)', apy: '8.5%', term: '21 days' },
                    { coin: 'Tezos (XTZ)', apy: '6.1%', term: '14 days' }
                  ].map((asset) => (
                    <div key={asset.coin} className="bg-dark_grey bg-opacity-50 rounded-lg p-4">
                      <div className="flex justify-between items-center mb-2">
                        <h3 className="text-white font-semibold">{asset.coin}</h3>
                        <span className="text-primary font-bold">{asset.apy}</span>
                      </div>
                      <p className="text-muted text-sm">Minimum term: {asset.term}</p>
                    </div>
                  ))}
                </div>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">How Staking Works</h2>
                <div className="grid md:grid-cols-3 gap-6">
                  <div className="text-center">
                    <div className="bg-primary bg-opacity-20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                      <span className="text-primary text-2xl font-bold">1</span>
                    </div>
                    <h3 className="text-white font-semibold mb-2">Choose Asset</h3>
                    <p className="text-muted text-sm">Select from supported cryptocurrencies and choose your staking term.</p>
                  </div>
                  <div className="text-center">
                    <div className="bg-primary bg-opacity-20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                      <span className="text-primary text-2xl font-bold">2</span>
                    </div>
                    <h3 className="text-white font-semibold mb-2">Stake & Lock</h3>
                    <p className="text-muted text-sm">Lock your assets for the chosen term and start earning rewards.</p>
                  </div>
                  <div className="text-center">
                    <div className="bg-primary bg-opacity-20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                      <span className="text-primary text-2xl font-bold">3</span>
                    </div>
                    <h3 className="text-white font-semibold mb-2">Earn Rewards</h3>
                    <p className="text-muted text-sm">Receive regular rewards based on your staked amount and chosen APY.</p>
                  </div>
                </div>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">Staking Benefits</h2>
                <ul className="text-muted list-disc list-inside space-y-2">
                  <li>Earn passive income on your cryptocurrency holdings</li>
                  <li>Support blockchain network security and decentralization</li>
                  <li>Competitive APY rates with flexible terms</li>
                  <li>Automatic reward distribution and compounding</li>
                  <li>Professional validator infrastructure</li>
                  <li>24/7 monitoring and support</li>
                </ul>
              </section>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

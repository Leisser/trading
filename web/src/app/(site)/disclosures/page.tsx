import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Disclosures | Fluxor",
  description: "Important disclosures and risk information for Fluxor cryptocurrency trading platform",
};

export default function DisclosuresPage() {
  return (
    <div className="min-h-screen bg-darkmode pt-32 pb-16">
      <div className="container mx-auto lg:max-w-screen-xl px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-white text-4xl font-bold mb-8">Disclosures</h1>
          
          <div className="prose prose-invert max-w-none">
            <div className="bg-dark_grey bg-opacity-50 p-8 rounded-lg">
              <h2 className="text-white text-2xl font-semibold mb-6">Risk Disclosure</h2>
              <p className="text-muted text-opacity-80 mb-6">
                Trading cryptocurrencies involves substantial risk of loss and is not suitable for all investors. The high degree of leverage can work against you as well as for you. Before deciding to trade cryptocurrencies, you should carefully consider your investment objectives, level of experience, and risk appetite.
              </p>

              <h2 className="text-white text-2xl font-semibold mb-6">Regulatory Information</h2>
              <p className="text-muted text-opacity-80 mb-6">
                Fluxor operates as a cryptocurrency trading platform. Please note that cryptocurrency regulations vary by jurisdiction and may change over time. Users are responsible for ensuring compliance with applicable laws and regulations in their jurisdiction.
              </p>

              <h2 className="text-white text-2xl font-semibold mb-6">Investment Risks</h2>
              <div className="mb-6">
                <h3 className="text-white text-xl font-semibold mb-4">Market Risk</h3>
                <p className="text-muted text-opacity-80 mb-4">
                  Cryptocurrency prices are highly volatile and can fluctuate dramatically in short periods. Market conditions can change rapidly, and past performance does not guarantee future results.
                </p>

                <h3 className="text-white text-xl font-semibold mb-4">Liquidity Risk</h3>
                <p className="text-muted text-opacity-80 mb-4">
                  Some cryptocurrencies may have limited liquidity, which can make it difficult to buy or sell large amounts without significantly affecting the price.
                </p>

                <h3 className="text-white text-xl font-semibold mb-4">Technology Risk</h3>
                <p className="text-muted text-opacity-80 mb-4">
                  Cryptocurrency trading relies on technology infrastructure. Technical failures, cyber attacks, or other technological issues could result in losses.
                </p>

                <h3 className="text-white text-xl font-semibold mb-4">Regulatory Risk</h3>
                <p className="text-muted text-opacity-80 mb-4">
                  Changes in government regulations or policies could adversely affect the value of cryptocurrencies and the ability to trade them.
                </p>
              </div>

              <h2 className="text-white text-2xl font-semibold mb-6">Platform Disclosures</h2>
              <p className="text-muted text-opacity-80 mb-6">
                Fluxor provides a trading platform for cryptocurrencies. We do not provide investment advice, and all trading decisions are made by the user. Users should conduct their own research and consider consulting with a qualified financial advisor before making investment decisions.
              </p>

              <h2 className="text-white text-2xl font-semibold mb-6">Fee Structure</h2>
              <p className="text-muted text-opacity-80 mb-6">
                Trading fees and other charges may apply to transactions conducted on our platform. Please review our fee schedule carefully before trading. Fees are subject to change with notice.
              </p>

              <h2 className="text-white text-2xl font-semibold mb-6">Security Measures</h2>
              <p className="text-muted text-opacity-80 mb-6">
                While we implement industry-standard security measures to protect user funds and data, no system is completely secure. Users should take appropriate precautions to protect their accounts and personal information.
              </p>

              <h2 className="text-white text-2xl font-semibold mb-6">No Guarantee of Performance</h2>
              <p className="text-muted text-opacity-80 mb-6">
                Fluxor makes no representations or warranties regarding the performance of any cryptocurrency or the success of any trading strategy. All investments carry risk, and users may lose some or all of their invested capital.
              </p>

              <h2 className="text-white text-2xl font-semibold mb-6">Third-Party Services</h2>
              <p className="text-muted text-opacity-80 mb-6">
                Our platform may integrate with third-party services and data providers. We are not responsible for the accuracy, completeness, or timeliness of information provided by third parties.
              </p>

              <div className="mt-8 p-6 bg-red-500 bg-opacity-10 border border-red-500 border-opacity-30 rounded-lg">
                <h3 className="text-red-400 text-xl font-semibold mb-4">Important Notice</h3>
                <p className="text-muted text-opacity-80">
                  This disclosure is not intended to be comprehensive. Users should carefully consider all risks before trading cryptocurrencies. If you are unsure about any aspect of cryptocurrency trading, please consult with a qualified financial advisor.
                </p>
              </div>

              <div className="mt-6 p-6 bg-primary bg-opacity-10 rounded-lg">
                <p className="text-muted text-opacity-80">
                  <strong>Last updated:</strong> {new Date().toLocaleDateString()}
                </p>
                <p className="text-muted text-opacity-80 mt-2">
                  For questions about these disclosures, please contact our support team.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

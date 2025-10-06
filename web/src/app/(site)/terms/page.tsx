import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Terms of Service | Fluxor",
  description: "Terms of Service for Fluxor cryptocurrency trading platform",
};

export default function TermsPage() {
  return (
    <div className="min-h-screen bg-darkmode pt-32 pb-16">
      <div className="container mx-auto lg:max-w-screen-xl px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-white text-4xl font-bold mb-8">Terms of Service</h1>
          
          <div className="prose prose-invert max-w-none">
            <div className="bg-dark_grey bg-opacity-50 p-8 rounded-lg">
              <h2 className="text-white text-2xl font-semibold mb-6">1. Acceptance of Terms</h2>
              <p className="text-muted text-opacity-80 mb-6">
                By accessing and using Fluxor's cryptocurrency trading platform, you accept and agree to be bound by the terms and provision of this agreement.
              </p>

              <h2 className="text-white text-2xl font-semibold mb-6">2. Use License</h2>
              <p className="text-muted text-opacity-80 mb-6">
                Permission is granted to temporarily download one copy of Fluxor's materials for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title, and under this license you may not:
              </p>
              <ul className="text-muted text-opacity-80 mb-6 list-disc pl-6">
                <li>Modify or copy the materials</li>
                <li>Use the materials for any commercial purpose or for any public display</li>
                <li>Attempt to reverse engineer any software contained on the website</li>
                <li>Remove any copyright or other proprietary notations from the materials</li>
              </ul>

              <h2 className="text-white text-2xl font-semibold mb-6">3. Trading Risks</h2>
              <p className="text-muted text-opacity-80 mb-6">
                Cryptocurrency trading involves substantial risk of loss and is not suitable for all investors. The high degree of leverage can work against you as well as for you. Before deciding to trade cryptocurrency, you should carefully consider your investment objectives, level of experience, and risk appetite.
              </p>

              <h2 className="text-white text-2xl font-semibold mb-6">4. User Responsibilities</h2>
              <p className="text-muted text-opacity-80 mb-6">
                You are responsible for maintaining the confidentiality of your account and password. You agree to accept responsibility for all activities that occur under your account or password.
              </p>

              <h2 className="text-white text-2xl font-semibold mb-6">5. Prohibited Uses</h2>
              <p className="text-muted text-opacity-80 mb-6">
                You may not use our service for any unlawful purpose or to solicit others to perform or participate in any unlawful acts. You may not violate any international, federal, provincial, or state regulations, rules, laws, or local ordinances.
              </p>

              <h2 className="text-white text-2xl font-semibold mb-6">6. Disclaimer</h2>
              <p className="text-muted text-opacity-80 mb-6">
                The materials on Fluxor's website are provided on an 'as is' basis. Fluxor makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties including without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.
              </p>

              <h2 className="text-white text-2xl font-semibold mb-6">7. Limitations</h2>
              <p className="text-muted text-opacity-80 mb-6">
                In no event shall Fluxor or its suppliers be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption) arising out of the use or inability to use the materials on Fluxor's website, even if Fluxor or a Fluxor authorized representative has been notified orally or in writing of the possibility of such damage.
              </p>

              <h2 className="text-white text-2xl font-semibold mb-6">8. Revisions</h2>
              <p className="text-muted text-opacity-80 mb-6">
                Fluxor may revise these terms of service for its website at any time without notice. By using this website you are agreeing to be bound by the then current version of these terms of service.
              </p>

              <h2 className="text-white text-2xl font-semibold mb-6">9. Governing Law</h2>
              <p className="text-muted text-opacity-80 mb-6">
                These terms and conditions are governed by and construed in accordance with the laws of the jurisdiction in which Fluxor operates and you irrevocably submit to the exclusive jurisdiction of the courts in that state or location.
              </p>

              <div className="mt-8 p-6 bg-primary bg-opacity-10 rounded-lg">
                <p className="text-muted text-opacity-80">
                  <strong>Last updated:</strong> {new Date().toLocaleDateString()}
                </p>
                <p className="text-muted text-opacity-80 mt-2">
                  If you have any questions about these Terms of Service, please contact us.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

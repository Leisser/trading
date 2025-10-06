import { Metadata } from "next";
import { Icon } from "@iconify/react";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Security | Fluxor",
  description: "Learn about Fluxor's comprehensive security measures and how we protect your funds and data",
};

export default function SecurityPage() {
  return (
    <div className="min-h-screen bg-darkmode pt-32 pb-16">
      <div className="container mx-auto lg:max-w-screen-xl px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-white text-4xl font-bold mb-8">Security</h1>
          
          <div className="prose prose-invert max-w-none">
            <p className="text-muted text-lg mb-8">
              At Fluxor, security is our top priority. We employ industry-leading security measures and best practices to protect your funds, data, and trading activities. Learn about our comprehensive security framework and how we keep your assets safe.
            </p>

            <div className="grid md:grid-cols-2 gap-8 mb-12">
              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:shield-check" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Cold Storage</h3>
                </div>
                <p className="text-muted">
                  95% of user funds are stored in offline cold storage wallets, completely isolated from internet access and potential cyber threats.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:key" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Multi-Signature</h3>
                </div>
                <p className="text-muted">
                  All hot wallets use multi-signature technology requiring multiple authorized signatures for any transaction approval.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:lock" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">2FA Protection</h3>
                </div>
                <p className="text-muted">
                  Two-factor authentication is mandatory for all accounts, providing an additional layer of security for your login and transactions.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:eye" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Real-time Monitoring</h3>
                </div>
                <p className="text-muted">
                  24/7 security monitoring with advanced threat detection systems and immediate response protocols for any suspicious activity.
                </p>
              </div>
            </div>

            <div className="bg-gradient-to-r from-primary to-charcoalGray rounded-lg p-8 text-center mb-12">
              <h3 className="text-white text-2xl font-semibold mb-4">Security First</h3>
              <p className="text-muted mb-6">
                Your security is our commitment. We continuously invest in the latest security technologies and practices.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link 
                  href="/signup" 
                  className="bg-white text-primary px-6 py-3 rounded-lg font-semibold hover:bg-opacity-90 transition-all"
                >
                  Create Secure Account
                </Link>
                <Link 
                  href="/support" 
                  className="border border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white hover:text-primary transition-all"
                >
                  Security Questions
                </Link>
              </div>
            </div>

            <div className="space-y-8">
              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">Security Measures</h2>
                <div className="space-y-6">
                  <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                    <h3 className="text-white font-semibold text-lg mb-3">Fund Protection</h3>
                    <ul className="text-muted list-disc list-inside space-y-2">
                      <li>95% of funds in cold storage with air-gapped systems</li>
                      <li>Multi-signature wallets for all hot wallet operations</li>
                      <li>Distributed key management across multiple secure locations</li>
                      <li>Regular security audits by third-party firms</li>
                      <li>Insurance coverage for digital assets</li>
                    </ul>
                  </div>

                  <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                    <h3 className="text-white font-semibold text-lg mb-3">Account Security</h3>
                    <ul className="text-muted list-disc list-inside space-y-2">
                      <li>Mandatory two-factor authentication (2FA)</li>
                      <li>Advanced password requirements and encryption</li>
                      <li>IP whitelisting and device management</li>
                      <li>Email and SMS verification for sensitive operations</li>
                      <li>Automatic logout for inactive sessions</li>
                    </ul>
                  </div>

                  <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                    <h3 className="text-white font-semibold text-lg mb-3">Infrastructure Security</h3>
                    <ul className="text-muted list-disc list-inside space-y-2">
                      <li>Enterprise-grade data centers with physical security</li>
                      <li>DDoS protection and traffic filtering</li>
                      <li>Regular penetration testing and vulnerability assessments</li>
                      <li>Encrypted data transmission (TLS 1.3)</li>
                      <li>Secure API endpoints with rate limiting</li>
                    </ul>
                  </div>
                </div>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">Compliance & Certifications</h2>
                <div className="grid md:grid-cols-2 gap-6">
                  <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                    <h3 className="text-white font-semibold mb-3">Regulatory Compliance</h3>
                    <ul className="text-muted space-y-2">
                      <li>• Licensed in multiple jurisdictions</li>
                      <li>• KYC/AML compliance programs</li>
                      <li>• Regular regulatory reporting</li>
                      <li>• Anti-money laundering measures</li>
                      <li>• Know Your Customer verification</li>
                    </ul>
                  </div>
                  <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                    <h3 className="text-white font-semibold mb-3">Security Certifications</h3>
                    <ul className="text-muted space-y-2">
                      <li>• SOC 2 Type II certified</li>
                      <li>• ISO 27001 compliance</li>
                      <li>• PCI DSS Level 1 certified</li>
                      <li>• Regular third-party audits</li>
                      <li>• Bug bounty program</li>
                    </ul>
                  </div>
                </div>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">Security Best Practices</h2>
                <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                  <h3 className="text-white font-semibold mb-4">For Users</h3>
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <h4 className="text-white font-medium mb-2">Account Security</h4>
                      <ul className="text-muted text-sm space-y-1">
                        <li>• Enable 2FA on your account</li>
                        <li>• Use a strong, unique password</li>
                        <li>• Regularly update your password</li>
                        <li>• Monitor your account activity</li>
                        <li>• Log out from shared devices</li>
                      </ul>
                    </div>
                    <div>
                      <h4 className="text-white font-medium mb-2">Trading Security</h4>
                      <ul className="text-muted text-sm space-y-1">
                        <li>• Verify withdrawal addresses</li>
                        <li>• Use whitelisted addresses</li>
                        <li>• Enable withdrawal confirmations</li>
                        <li>• Keep your API keys secure</li>
                        <li>• Monitor your trading activity</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">Incident Response</h2>
                <div className="grid md:grid-cols-3 gap-6">
                  <div className="text-center">
                    <div className="bg-primary bg-opacity-20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                      <span className="text-primary text-2xl font-bold">1</span>
                    </div>
                    <h3 className="text-white font-semibold mb-2">Detection</h3>
                    <p className="text-muted text-sm">Advanced monitoring systems detect potential security threats in real-time.</p>
                  </div>
                  <div className="text-center">
                    <div className="bg-primary bg-opacity-20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                      <span className="text-primary text-2xl font-bold">2</span>
                    </div>
                    <h3 className="text-white font-semibold mb-2">Response</h3>
                    <p className="text-muted text-sm">Immediate response protocols are activated to contain and mitigate threats.</p>
                  </div>
                  <div className="text-center">
                    <div className="bg-primary bg-opacity-20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                      <span className="text-primary text-2xl font-bold">3</span>
                    </div>
                    <h3 className="text-white font-semibold mb-2">Recovery</h3>
                    <p className="text-muted text-sm">Systems are restored and security measures are strengthened.</p>
                  </div>
                </div>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">Security Contact</h2>
                <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                  <p className="text-muted mb-4">
                    If you discover a security vulnerability or have security concerns, please contact our security team immediately.
                  </p>
                  <div className="flex flex-col sm:flex-row gap-4">
                    <Link 
                      href="mailto:security@fluxor.pro" 
                      className="bg-primary text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary/90 transition-all text-center"
                    >
                      Report Security Issue
                    </Link>
                    <Link 
                      href="mailto:security@fluxor.pro" 
                      className="border border-primary text-primary px-6 py-3 rounded-lg font-semibold hover:bg-primary hover:text-white transition-all text-center"
                    >
                      Security Questions
                    </Link>
                  </div>
                </div>
              </section>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

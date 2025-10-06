import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Privacy Policy | Fluxor",
  description: "Learn how Fluxor protects your privacy and handles your personal information",
};

export default function PrivacyPage() {
  return (
    <div className="min-h-screen bg-darkmode pt-32 pb-16">
      <div className="container mx-auto lg:max-w-screen-xl px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-white text-4xl font-bold mb-8">Privacy Policy</h1>
          
          <div className="prose prose-invert max-w-none">
            <p className="text-muted text-lg mb-8">
              <strong>Last Updated:</strong> December 2024
            </p>

            <div className="space-y-8">
              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">1. Introduction</h2>
                <p className="text-muted leading-relaxed">
                  Fluxor ("we," "our," or "us") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our cryptocurrency trading platform and related services (the "Service").
                </p>
                <p className="text-muted leading-relaxed mt-4">
                  By using our Service, you agree to the collection and use of information in accordance with this Privacy Policy.
                </p>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">2. Information We Collect</h2>
                
                <h3 className="text-white text-xl font-medium mb-3">2.1 Personal Information</h3>
                <p className="text-muted leading-relaxed mb-4">
                  We may collect personal information that you provide directly to us, including:
                </p>
                <ul className="text-muted list-disc list-inside space-y-2 ml-4">
                  <li>Name, email address, and contact information</li>
                  <li>Account credentials and authentication information</li>
                  <li>Financial information for trading and payment processing</li>
                  <li>Identity verification documents (KYC/AML compliance)</li>
                  <li>Communication preferences and support interactions</li>
                </ul>

                <h3 className="text-white text-xl font-medium mb-3 mt-6">2.2 Technical Information</h3>
                <p className="text-muted leading-relaxed mb-4">
                  We automatically collect certain technical information, including:
                </p>
                <ul className="text-muted list-disc list-inside space-y-2 ml-4">
                  <li>IP address, browser type, and device information</li>
                  <li>Usage patterns and platform interactions</li>
                  <li>Cookies and similar tracking technologies</li>
                  <li>Log files and system performance data</li>
                </ul>

                <h3 className="text-white text-xl font-medium mb-3 mt-6">2.3 Trading Information</h3>
                <p className="text-muted leading-relaxed mb-4">
                  We collect trading-related data to provide our services:
                </p>
                <ul className="text-muted list-disc list-inside space-y-2 ml-4">
                  <li>Trading history and transaction records</li>
                  <li>Portfolio holdings and performance data</li>
                  <li>Market analysis and research preferences</li>
                  <li>Risk assessment and compliance data</li>
                </ul>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">3. How We Use Your Information</h2>
                <p className="text-muted leading-relaxed mb-4">
                  We use the collected information for the following purposes:
                </p>
                <ul className="text-muted list-disc list-inside space-y-2 ml-4">
                  <li><strong>Service Provision:</strong> To provide, maintain, and improve our trading platform</li>
                  <li><strong>Account Management:</strong> To create and manage your account and verify your identity</li>
                  <li><strong>Transaction Processing:</strong> To process trades, deposits, and withdrawals</li>
                  <li><strong>Security:</strong> To protect against fraud, unauthorized access, and security threats</li>
                  <li><strong>Compliance:</strong> To meet regulatory requirements and legal obligations</li>
                  <li><strong>Communication:</strong> To send important updates, notifications, and support</li>
                  <li><strong>Analytics:</strong> To analyze usage patterns and improve our services</li>
                  <li><strong>Marketing:</strong> To provide relevant information about our services (with your consent)</li>
                </ul>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">4. Information Sharing and Disclosure</h2>
                <p className="text-muted leading-relaxed mb-4">
                  We do not sell, trade, or rent your personal information to third parties. We may share your information in the following circumstances:
                </p>
                <ul className="text-muted list-disc list-inside space-y-2 ml-4">
                  <li><strong>Service Providers:</strong> With trusted third-party vendors who assist in platform operations</li>
                  <li><strong>Legal Requirements:</strong> When required by law, court order, or regulatory authority</li>
                  <li><strong>Business Transfers:</strong> In connection with mergers, acquisitions, or asset sales</li>
                  <li><strong>Consent:</strong> When you explicitly consent to sharing your information</li>
                  <li><strong>Security:</strong> To protect our rights, property, or safety, or that of our users</li>
                </ul>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">5. Data Security</h2>
                <p className="text-muted leading-relaxed mb-4">
                  We implement comprehensive security measures to protect your information:
                </p>
                <ul className="text-muted list-disc list-inside space-y-2 ml-4">
                  <li>End-to-end encryption for all data transmission</li>
                  <li>Multi-factor authentication and secure login systems</li>
                  <li>Regular security audits and vulnerability assessments</li>
                  <li>Secure data centers with physical and digital access controls</li>
                  <li>Employee training on data protection and privacy practices</li>
                  <li>Incident response procedures for potential security breaches</li>
                </ul>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">6. Data Retention</h2>
                <p className="text-muted leading-relaxed">
                  We retain your personal information for as long as necessary to provide our services and comply with legal obligations. Trading records and financial data are retained for regulatory compliance periods, typically 5-7 years. You may request deletion of your account and associated data, subject to legal and regulatory requirements.
                </p>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">7. Your Rights and Choices</h2>
                <p className="text-muted leading-relaxed mb-4">
                  You have the following rights regarding your personal information:
                </p>
                <ul className="text-muted list-disc list-inside space-y-2 ml-4">
                  <li><strong>Access:</strong> Request access to your personal information</li>
                  <li><strong>Correction:</strong> Request correction of inaccurate or incomplete data</li>
                  <li><strong>Deletion:</strong> Request deletion of your personal information (subject to legal requirements)</li>
                  <li><strong>Portability:</strong> Request a copy of your data in a portable format</li>
                  <li><strong>Opt-out:</strong> Unsubscribe from marketing communications</li>
                  <li><strong>Restriction:</strong> Request restriction of processing in certain circumstances</li>
                </ul>
                <p className="text-muted leading-relaxed mt-4">
                  To exercise these rights, please contact us at <a href="mailto:privacy@fluxor.pro" className="text-primary hover:text-white transition-colors">privacy@fluxor.pro</a>
                </p>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">8. Cookies and Tracking Technologies</h2>
                <p className="text-muted leading-relaxed mb-4">
                  We use cookies and similar technologies to enhance your experience:
                </p>
                <ul className="text-muted list-disc list-inside space-y-2 ml-4">
                  <li><strong>Essential Cookies:</strong> Required for platform functionality and security</li>
                  <li><strong>Analytics Cookies:</strong> Help us understand usage patterns and improve services</li>
                  <li><strong>Preference Cookies:</strong> Remember your settings and preferences</li>
                  <li><strong>Marketing Cookies:</strong> Used for targeted advertising (with your consent)</li>
                </ul>
                <p className="text-muted leading-relaxed mt-4">
                  You can manage cookie preferences through your browser settings or our cookie consent manager.
                </p>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">9. International Data Transfers</h2>
                <p className="text-muted leading-relaxed">
                  Your information may be transferred to and processed in countries other than your country of residence. We ensure appropriate safeguards are in place to protect your information in accordance with applicable data protection laws, including standard contractual clauses and adequacy decisions.
                </p>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">10. Children's Privacy</h2>
                <p className="text-muted leading-relaxed">
                  Our Service is not intended for individuals under the age of 18. We do not knowingly collect personal information from children under 18. If we become aware that we have collected personal information from a child under 18, we will take steps to delete such information promptly.
                </p>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">11. Changes to This Privacy Policy</h2>
                <p className="text-muted leading-relaxed">
                  We may update this Privacy Policy from time to time. We will notify you of any material changes by posting the new Privacy Policy on this page and updating the "Last Updated" date. We encourage you to review this Privacy Policy periodically for any changes.
                </p>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">12. Contact Information</h2>
                <p className="text-muted leading-relaxed mb-4">
                  If you have any questions about this Privacy Policy or our privacy practices, please contact us:
                </p>
                <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                  <div className="space-y-3">
                    <div>
                      <strong className="text-white">Email:</strong> 
                      <a href="mailto:privacy@fluxor.pro" className="text-primary hover:text-white transition-colors ml-2">privacy@fluxor.pro</a>
                    </div>
                    <div>
                      <strong className="text-white">Support:</strong> 
                      <a href="mailto:support@fluxor.pro" className="text-primary hover:text-white transition-colors ml-2">support@fluxor.pro</a>
                    </div>
                    <div>
                      <strong className="text-white">Address:</strong> 
                      <span className="text-muted ml-2">New York, NY, United States</span>
                    </div>
                    <div>
                      <strong className="text-white">Phone:</strong> 
                      <span className="text-muted ml-2">+1 (555) 123-4567</span>
                    </div>
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

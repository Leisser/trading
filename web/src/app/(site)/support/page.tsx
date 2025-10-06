import { Metadata } from "next";
import { Icon } from "@iconify/react";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Support Center | Fluxor",
  description: "Get help and support for your Fluxor trading account and platform questions",
};

export default function SupportPage() {
  return (
    <div className="min-h-screen bg-darkmode pt-32 pb-16">
      <div className="container mx-auto lg:max-w-screen-xl px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-white text-4xl font-bold mb-8">Support Center</h1>
          
          <div className="prose prose-invert max-w-none">
            <p className="text-muted text-lg mb-8">
              We're here to help you succeed with Fluxor. Get instant answers to your questions, access our knowledge base, or contact our support team for personalized assistance.
            </p>

            <div className="grid md:grid-cols-2 gap-8 mb-12">
              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:headphones" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">24/7 Support</h3>
                </div>
                <p className="text-muted">
                  Our support team is available around the clock to help you with any questions or issues you may have.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:book" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Knowledge Base</h3>
                </div>
                <p className="text-muted">
                  Access comprehensive guides, tutorials, and FAQs to help you get the most out of Fluxor.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:message-circle" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Live Chat</h3>
                </div>
                <p className="text-muted">
                  Get instant help through our live chat feature with our knowledgeable support agents.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:mail" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Email Support</h3>
                </div>
                <p className="text-muted">
                  Send us detailed questions via email and receive comprehensive responses within 24 hours.
                </p>
              </div>
            </div>

            <div className="bg-gradient-to-r from-primary to-charcoalGray rounded-lg p-8 text-center mb-12">
              <h3 className="text-white text-2xl font-semibold mb-4">Need Immediate Help?</h3>
              <p className="text-muted mb-6">
                Contact our support team directly for urgent issues or account-related questions.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link 
                  href="mailto:support@fluxor.pro" 
                  className="bg-white text-primary px-6 py-3 rounded-lg font-semibold hover:bg-opacity-90 transition-all"
                >
                  Email Support
                </Link>
                <Link 
                  href="tel:+15551234567" 
                  className="border border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white hover:text-primary transition-all"
                >
                  Call Us
                </Link>
              </div>
            </div>

            <div className="space-y-8">
              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">Frequently Asked Questions</h2>
                <div className="space-y-4">
                  {[
                    {
                      question: "How do I create a Fluxor account?",
                      answer: "Creating an account is simple. Click 'Sign Up' on our homepage, provide your email address, create a secure password, and complete the email verification process."
                    },
                    {
                      question: "What cryptocurrencies can I trade on Fluxor?",
                      answer: "We support over 200 cryptocurrencies including Bitcoin, Ethereum, Binance Coin, Cardano, Solana, and many more. New coins are added regularly."
                    },
                    {
                      question: "How secure is my account and funds?",
                      answer: "We use institutional-grade security including cold storage, multi-signature wallets, 2FA, and regular security audits to protect your funds."
                    },
                    {
                      question: "What are the trading fees?",
                      answer: "Our trading fees start from 0.1% for spot trading. Fees vary based on your trading volume and VIP level. Check our fee schedule for detailed information."
                    },
                    {
                      question: "How do I deposit funds to my account?",
                      answer: "You can deposit cryptocurrencies directly to your wallet address or use our fiat on-ramp services for USD deposits via bank transfer or credit card."
                    },
                    {
                      question: "Is there a mobile app available?",
                      answer: "Yes, we have mobile apps for both iOS and Android devices. Download them from the App Store or Google Play Store for trading on the go."
                    }
                  ].map((faq, index) => (
                    <div key={index} className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                      <h3 className="text-white font-semibold mb-2">{faq.question}</h3>
                      <p className="text-muted">{faq.answer}</p>
                    </div>
                  ))}
                </div>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">Contact Methods</h2>
                <div className="grid md:grid-cols-2 gap-6">
                  <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                    <h3 className="text-white font-semibold mb-4">General Support</h3>
                    <div className="space-y-3">
                      <div className="flex items-center">
                        <Icon icon="tabler:mail" width="20" height="20" className="text-primary mr-3" />
                        <span className="text-muted">support@fluxor.pro</span>
                      </div>
                      <div className="flex items-center">
                        <Icon icon="tabler:phone" width="20" height="20" className="text-primary mr-3" />
                        <span className="text-muted">+1 (555) 123-4567</span>
                      </div>
                      <div className="flex items-center">
                        <Icon icon="tabler:clock" width="20" height="20" className="text-primary mr-3" />
                        <span className="text-muted">24/7 Support</span>
                      </div>
                    </div>
                  </div>
                  <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                    <h3 className="text-white font-semibold mb-4">Business Inquiries</h3>
                    <div className="space-y-3">
                      <div className="flex items-center">
                        <Icon icon="tabler:mail" width="20" height="20" className="text-primary mr-3" />
                        <span className="text-muted">business@fluxor.pro</span>
                      </div>
                      <div className="flex items-center">
                        <Icon icon="tabler:building" width="20" height="20" className="text-primary mr-3" />
                        <span className="text-muted">Partnerships & API</span>
                      </div>
                      <div className="flex items-center">
                        <Icon icon="tabler:clock" width="20" height="20" className="text-primary mr-3" />
                        <span className="text-muted">Mon-Fri 9AM-6PM EST</span>
                      </div>
                    </div>
                  </div>
                </div>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">Support Resources</h2>
                <div className="grid md:grid-cols-3 gap-6">
                  <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6 text-center">
                    <Icon icon="tabler:book-open" width="48" height="48" className="text-primary mx-auto mb-4" />
                    <h3 className="text-white font-semibold mb-2">User Guide</h3>
                    <p className="text-muted text-sm mb-4">Comprehensive guide covering all platform features and trading basics.</p>
                    <Link href="/documentation" className="text-primary hover:text-white transition-colors text-sm">
                      Read Guide →
                    </Link>
                  </div>
                  <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6 text-center">
                    <Icon icon="tabler:video" width="48" height="48" className="text-primary mx-auto mb-4" />
                    <h3 className="text-white font-semibold mb-2">Video Tutorials</h3>
                    <p className="text-muted text-sm mb-4">Step-by-step video tutorials for common tasks and features.</p>
                    <Link href="#" className="text-primary hover:text-white transition-colors text-sm">
                      Watch Videos →
                    </Link>
                  </div>
                  <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6 text-center">
                    <Icon icon="tabler:users" width="48" height="48" className="text-primary mx-auto mb-4" />
                    <h3 className="text-white font-semibold mb-2">Community</h3>
                    <p className="text-muted text-sm mb-4">Join our community forum to connect with other traders.</p>
                    <Link href="#" className="text-primary hover:text-white transition-colors text-sm">
                      Join Community →
                    </Link>
                  </div>
                </div>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">Response Times</h2>
                <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <h3 className="text-white font-semibold mb-3">Standard Support</h3>
                      <ul className="text-muted space-y-2">
                        <li>• General questions: Within 24 hours</li>
                        <li>• Account issues: Within 12 hours</li>
                        <li>• Technical problems: Within 6 hours</li>
                      </ul>
                    </div>
                    <div>
                      <h3 className="text-white font-semibold mb-3">Priority Support</h3>
                      <ul className="text-muted space-y-2">
                        <li>• VIP customers: Within 2 hours</li>
                        <li>• High-volume traders: Within 4 hours</li>
                        <li>• Security issues: Immediate response</li>
                      </ul>
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

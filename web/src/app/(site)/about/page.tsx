import { Metadata } from "next";
import { Icon } from "@iconify/react";
import Link from "next/link";

export const metadata: Metadata = {
  title: "About Us | Fluxor",
  description: "Learn about Fluxor's mission to revolutionize cryptocurrency trading with institutional-grade technology",
};

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-darkmode pt-32 pb-16">
      <div className="container mx-auto lg:max-w-screen-xl px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-white text-4xl font-bold mb-8">About Fluxor</h1>
          
          <div className="prose prose-invert max-w-none">
            <p className="text-muted text-lg mb-8">
              Fluxor is a leading cryptocurrency trading platform that combines institutional-grade technology with user-friendly design. We're committed to democratizing access to professional trading tools and making cryptocurrency trading accessible to everyone.
            </p>

            <div className="grid md:grid-cols-2 gap-8 mb-12">
              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:target" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Our Mission</h3>
                </div>
                <p className="text-muted">
                  To provide a secure, fast, and intuitive platform that empowers traders of all levels to succeed in the cryptocurrency markets.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:eye" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Our Vision</h3>
                </div>
                <p className="text-muted">
                  To become the world's most trusted and innovative cryptocurrency trading platform, setting new standards for security and user experience.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:heart" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Our Values</h3>
                </div>
                <p className="text-muted">
                  Security, transparency, innovation, and user-centricity guide everything we do at Fluxor.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:users" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Our Team</h3>
                </div>
                <p className="text-muted">
                  A diverse team of experts in finance, technology, and blockchain working together to build the future of trading.
                </p>
              </div>
            </div>

            <div className="space-y-8">
              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">Company History</h2>
                <div className="space-y-6">
                  <div className="flex items-start space-x-4">
                    <div className="bg-primary bg-opacity-20 rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 mt-1">
                      <span className="text-primary text-sm font-bold">2018</span>
                    </div>
                    <div>
                      <h3 className="text-white font-semibold mb-1">Company Founded</h3>
                      <p className="text-muted">Fluxor was founded with a vision to revolutionize cryptocurrency trading through innovative technology and user-centric design.</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-4">
                    <div className="bg-primary bg-opacity-20 rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 mt-1">
                      <span className="text-primary text-sm font-bold">2020</span>
                    </div>
                    <div>
                      <h3 className="text-white font-semibold mb-1">Platform Launch</h3>
                      <p className="text-muted">Launched our first trading platform with spot trading, advanced charts, and institutional-grade security features.</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-4">
                    <div className="bg-primary bg-opacity-20 rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 mt-1">
                      <span className="text-primary text-sm font-bold">2022</span>
                    </div>
                    <div>
                      <h3 className="text-white font-semibold mb-1">Global Expansion</h3>
                      <p className="text-muted">Expanded to serve customers worldwide with regulatory compliance in multiple jurisdictions.</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-4">
                    <div className="bg-primary bg-opacity-20 rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 mt-1">
                      <span className="text-primary text-sm font-bold">2024</span>
                    </div>
                    <div>
                      <h3 className="text-white font-semibold mb-1">Advanced Features</h3>
                      <p className="text-muted">Introduced futures trading, margin trading, staking rewards, and comprehensive API access for professional traders.</p>
                    </div>
                  </div>
                </div>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">Key Statistics</h2>
                <div className="grid md:grid-cols-4 gap-6">
                  <div className="text-center">
                    <div className="text-primary text-3xl font-bold mb-2">500K+</div>
                    <div className="text-muted">Active Users</div>
                  </div>
                  <div className="text-center">
                    <div className="text-primary text-3xl font-bold mb-2">$50B+</div>
                    <div className="text-muted">Trading Volume</div>
                  </div>
                  <div className="text-center">
                    <div className="text-primary text-3xl font-bold mb-2">200+</div>
                    <div className="text-muted">Cryptocurrencies</div>
                  </div>
                  <div className="text-center">
                    <div className="text-primary text-3xl font-bold mb-2">99.9%</div>
                    <div className="text-muted">Uptime</div>
                  </div>
                </div>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">Leadership Team</h2>
                <div className="grid md:grid-cols-2 gap-6">
                  <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                    <h3 className="text-white font-semibold mb-2">Sarah Chen</h3>
                    <p className="text-primary text-sm mb-2">Chief Executive Officer</p>
                    <p className="text-muted text-sm">Former Goldman Sachs executive with 15+ years in financial technology and blockchain innovation.</p>
                  </div>
                  <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                    <h3 className="text-white font-semibold mb-2">Marcus Rodriguez</h3>
                    <p className="text-primary text-sm mb-2">Chief Technology Officer</p>
                    <p className="text-muted text-sm">Ex-Google engineer specializing in distributed systems and high-frequency trading infrastructure.</p>
                  </div>
                  <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                    <h3 className="text-white font-semibold mb-2">Dr. Emily Watson</h3>
                    <p className="text-primary text-sm mb-2">Chief Security Officer</p>
                    <p className="text-muted text-sm">Cybersecurity expert with PhD in cryptography and extensive experience in financial security.</p>
                  </div>
                  <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                    <h3 className="text-white font-semibold mb-2">James Park</h3>
                    <p className="text-primary text-sm mb-2">Chief Financial Officer</p>
                    <p className="text-muted text-sm">Former JP Morgan investment banker with deep expertise in digital asset markets and regulation.</p>
                  </div>
                </div>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">Contact Information</h2>
                <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <h3 className="text-white font-semibold mb-3">Headquarters</h3>
                      <div className="space-y-2 text-muted">
                        <p>123 Financial District</p>
                        <p>New York, NY 10004</p>
                        <p>United States</p>
                      </div>
                    </div>
                    <div>
                      <h3 className="text-white font-semibold mb-3">Contact Details</h3>
                      <div className="space-y-2 text-muted">
                        <p>Email: info@fluxor.pro</p>
                        <p>Phone: +1 (555) 123-4567</p>
                        <p>Support: support@fluxor.pro</p>
                      </div>
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

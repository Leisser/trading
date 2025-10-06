import { Metadata } from "next";
import { Icon } from "@iconify/react";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Careers | Fluxor",
  description: "Join the Fluxor team and help shape the future of cryptocurrency trading",
};

export default function CareersPage() {
  return (
    <div className="min-h-screen bg-darkmode pt-32 pb-16">
      <div className="container mx-auto lg:max-w-screen-xl px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-white text-4xl font-bold mb-8">Careers at Fluxor</h1>
          
          <div className="prose prose-invert max-w-none">
            <p className="text-muted text-lg mb-8">
              Join our mission to revolutionize cryptocurrency trading. We're looking for passionate individuals who want to build the future of finance with cutting-edge technology and innovative solutions.
            </p>

            <div className="grid md:grid-cols-2 gap-8 mb-12">
              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:rocket" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Innovation</h3>
                </div>
                <p className="text-muted">
                  Work on cutting-edge technology that's shaping the future of cryptocurrency trading and blockchain innovation.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:users" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Great Team</h3>
                </div>
                <p className="text-muted">
                  Collaborate with talented professionals from top tech companies and financial institutions worldwide.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:growth" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Growth</h3>
                </div>
                <p className="text-muted">
                  Accelerate your career with opportunities for professional development, mentorship, and rapid advancement.
                </p>
              </div>

              <div className="bg-dark_grey bg-opacity-50 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Icon icon="tabler:world" width="32" height="32" className="text-primary mr-3" />
                  <h3 className="text-white text-xl font-semibold">Global Impact</h3>
                </div>
                <p className="text-muted">
                  Make a real impact on millions of users worldwide and help democratize access to financial markets.
                </p>
              </div>
            </div>

            <div className="bg-gradient-to-r from-primary to-charcoalGray rounded-lg p-8 text-center mb-12">
              <h3 className="text-white text-2xl font-semibold mb-4">Ready to Join Us?</h3>
              <p className="text-muted mb-6">
                Explore our open positions and start your journey with Fluxor today.
              </p>
              <Link 
                href="mailto:careers@fluxor.pro" 
                className="bg-white text-primary px-6 py-3 rounded-lg font-semibold hover:bg-opacity-90 transition-all inline-block"
              >
                View Open Positions
              </Link>
            </div>

            <div className="space-y-8">
              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">Open Positions</h2>
                <div className="space-y-4">
                  {[
                    { title: "Senior Software Engineer", location: "New York, NY", type: "Full-time", department: "Engineering" },
                    { title: "Product Manager", location: "San Francisco, CA", type: "Full-time", department: "Product" },
                    { title: "DevOps Engineer", location: "Remote", type: "Full-time", department: "Engineering" },
                    { title: "UX/UI Designer", location: "New York, NY", type: "Full-time", department: "Design" },
                    { title: "Security Analyst", location: "Remote", type: "Full-time", department: "Security" },
                    { title: "Customer Success Manager", location: "London, UK", type: "Full-time", department: "Customer Success" }
                  ].map((job) => (
                    <div key={job.title} className="bg-dark_grey bg-opacity-50 rounded-lg p-6 hover:bg-opacity-70 transition-all">
                      <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                        <div>
                          <h3 className="text-white font-semibold text-lg mb-1">{job.title}</h3>
                          <div className="flex flex-wrap gap-4 text-sm text-muted">
                            <span className="flex items-center">
                              <Icon icon="tabler:map-pin" width="16" height="16" className="mr-1" />
                              {job.location}
                            </span>
                            <span className="flex items-center">
                              <Icon icon="tabler:briefcase" width="16" height="16" className="mr-1" />
                              {job.type}
                            </span>
                            <span className="flex items-center">
                              <Icon icon="tabler:building" width="16" height="16" className="mr-1" />
                              {job.department}
                            </span>
                          </div>
                        </div>
                        <Link 
                          href={`mailto:careers@fluxor.pro?subject=Application for ${job.title}`}
                          className="mt-4 md:mt-0 bg-primary text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-primary/90 transition-all"
                        >
                          Apply Now
                        </Link>
                      </div>
                    </div>
                  ))}
                </div>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">Benefits & Perks</h2>
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="text-white text-lg font-semibold mb-3">Compensation & Benefits</h3>
                    <ul className="text-muted list-disc list-inside space-y-1">
                      <li>Competitive salary and equity packages</li>
                      <li>Comprehensive health, dental, and vision insurance</li>
                      <li>401(k) with company matching</li>
                      <li>Flexible PTO and paid holidays</li>
                      <li>Professional development budget</li>
                    </ul>
                  </div>
                  <div>
                    <h3 className="text-white text-lg font-semibold mb-3">Work Environment</h3>
                    <ul className="text-muted list-disc list-inside space-y-1">
                      <li>Flexible remote work options</li>
                      <li>Modern office spaces in major cities</li>
                      <li>Top-tier equipment and tools</li>
                      <li>Team building events and activities</li>
                      <li>Free meals and snacks</li>
                    </ul>
                  </div>
                </div>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">Our Culture</h2>
                <div className="grid md:grid-cols-3 gap-6">
                  <div className="text-center">
                    <div className="bg-primary bg-opacity-20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                      <Icon icon="tabler:bulb" width="32" height="32" className="text-primary" />
                    </div>
                    <h3 className="text-white font-semibold mb-2">Innovation First</h3>
                    <p className="text-muted text-sm">We encourage creative thinking and bold ideas that push the boundaries of what's possible.</p>
                  </div>
                  <div className="text-center">
                    <div className="bg-primary bg-opacity-20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                      <Icon icon="tabler:handshake" width="32" height="32" className="text-primary" />
                    </div>
                    <h3 className="text-white font-semibold mb-2">Collaboration</h3>
                    <p className="text-muted text-sm">We believe in the power of teamwork and open communication across all levels.</p>
                  </div>
                  <div className="text-center">
                    <div className="bg-primary bg-opacity-20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                      <Icon icon="tabler:target" width="32" height="32" className="text-primary" />
                    </div>
                    <h3 className="text-white font-semibold mb-2">Excellence</h3>
                    <p className="text-muted text-sm">We strive for excellence in everything we do, from code quality to customer service.</p>
                  </div>
                </div>
              </section>

              <section>
                <h2 className="text-white text-2xl font-semibold mb-4">Application Process</h2>
                <div className="grid md:grid-cols-4 gap-6">
                  <div className="text-center">
                    <div className="bg-primary bg-opacity-20 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
                      <span className="text-primary text-lg font-bold">1</span>
                    </div>
                    <h3 className="text-white font-semibold mb-2">Apply</h3>
                    <p className="text-muted text-sm">Submit your application with resume and cover letter</p>
                  </div>
                  <div className="text-center">
                    <div className="bg-primary bg-opacity-20 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
                      <span className="text-primary text-lg font-bold">2</span>
                    </div>
                    <h3 className="text-white font-semibold mb-2">Review</h3>
                    <p className="text-muted text-sm">Our team reviews your application and qualifications</p>
                  </div>
                  <div className="text-center">
                    <div className="bg-primary bg-opacity-20 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
                      <span className="text-primary text-lg font-bold">3</span>
                    </div>
                    <h3 className="text-white font-semibold mb-2">Interview</h3>
                    <p className="text-muted text-sm">Technical and cultural fit interviews with the team</p>
                  </div>
                  <div className="text-center">
                    <div className="bg-primary bg-opacity-20 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
                      <span className="text-primary text-lg font-bold">4</span>
                    </div>
                    <h3 className="text-white font-semibold mb-2">Offer</h3>
                    <p className="text-muted text-sm">Receive your offer and join the Fluxor team</p>
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

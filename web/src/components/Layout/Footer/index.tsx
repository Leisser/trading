"use client";

import React, { FC, useState } from "react";
import Link from "next/link";
import { headerData } from "../Header/Navigation/menuData";
import { footerlabels } from "@/app/api/data";
import Image from "next/image";
import { Icon } from "@iconify/react";
import Logo from "../Header/Logo";
import { validateEmail } from "@/utils/validateEmail";

const Footer: FC = () => {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleNewsletterSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!email.trim()) {
      setMessage("Please enter your email address.");
      return;
    }

    if (!validateEmail(email)) {
      setMessage("Please enter a valid email address.");
      return;
    }

    setIsLoading(true);
    setMessage("");

    try {
      // Simulate API call - replace with actual newsletter subscription logic
      await new Promise(resolve => setTimeout(resolve, 1000));
      setMessage("Subscription successful! Thank you for subscribing to our newsletter.");
      setEmail("");
    } catch (error) {
      setMessage("Something went wrong. Please try again later.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <footer className="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 border-t border-slate-700">
      {/* Main Footer Content */}
      <div className="container mx-auto max-w-7xl px-4 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 lg:gap-12">
          
          {/* Company Info & Features */}
          <div className="lg:col-span-1 space-y-6">
            <div>
              <Logo />
              <p className="text-slate-300 text-sm mt-4 leading-relaxed">
                Professional cryptocurrency trading platform with institutional-grade security, 
                real-time analytics, and expert insights for confident trading.
              </p>
            </div>
            
            {/* Key Features */}
            <div>
              <h4 className="text-white font-semibold text-lg mb-4">Why Choose Fluxor</h4>
              <div className="space-y-3">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center">
                    <Icon icon="tabler:shield-check" width="16" height="16" className="text-primary" />
                  </div>
                  <span className="text-slate-300 text-sm">Bank-level Security</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center">
                    <Icon icon="tabler:chart-line" width="16" height="16" className="text-primary" />
                  </div>
                  <span className="text-slate-300 text-sm">Real-time Analytics</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center">
                    <Icon icon="tabler:zap" width="16" height="16" className="text-primary" />
                  </div>
                  <span className="text-slate-300 text-sm">Lightning Fast Trading</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center">
                    <Icon icon="tabler:users" width="16" height="16" className="text-primary" />
                  </div>
                  <span className="text-slate-300 text-sm">24/7 Expert Support</span>
                </div>
              </div>
            </div>
          </div>

          {/* Trading & Services */}
          <div className="lg:col-span-1">
            <h4 className="text-white font-semibold text-lg mb-6">Trading & Services</h4>
            <ul className="space-y-3">
              <li>
                <Link href="/trading" className="text-slate-300 hover:text-primary transition-colors text-sm flex items-center">
                  <Icon icon="tabler:chart-candle" width="16" height="16" className="mr-2" />
                  Spot Trading
                </Link>
              </li>
              <li>
                <Link href="/futures" className="text-slate-300 hover:text-primary transition-colors text-sm flex items-center">
                  <Icon icon="tabler:trending-up" width="16" height="16" className="mr-2" />
                  Futures Trading
                </Link>
              </li>
              <li>
                <Link href="/margin" className="text-slate-300 hover:text-primary transition-colors text-sm flex items-center">
                  <Icon icon="tabler:scale" width="16" height="16" className="mr-2" />
                  Margin Trading
                </Link>
              </li>
              <li>
                <Link href="/staking" className="text-slate-300 hover:text-primary transition-colors text-sm flex items-center">
                  <Icon icon="tabler:coins" width="16" height="16" className="mr-2" />
                  Staking Rewards
                </Link>
              </li>
              <li>
                <Link href="/api" className="text-slate-300 hover:text-primary transition-colors text-sm flex items-center">
                  <Icon icon="tabler:code" width="16" height="16" className="mr-2" />
                  API Access
                </Link>
              </li>
            </ul>
          </div>

          {/* Company & Support */}
          <div className="lg:col-span-1">
            <h4 className="text-white font-semibold text-lg mb-6">Company & Support</h4>
            <ul className="space-y-3">
              <li>
                <Link href="/about" className="text-slate-300 hover:text-primary transition-colors text-sm flex items-center">
                  <Icon icon="tabler:info-circle" width="16" height="16" className="mr-2" />
                  About Us
                </Link>
              </li>
              <li>
                <Link href="/careers" className="text-slate-300 hover:text-primary transition-colors text-sm flex items-center">
                  <Icon icon="tabler:briefcase" width="16" height="16" className="mr-2" />
                  Careers
                </Link>
              </li>
              <li>
                <Link href="/support" className="text-slate-300 hover:text-primary transition-colors text-sm flex items-center">
                  <Icon icon="tabler:headphones" width="16" height="16" className="mr-2" />
                  Support Center
                </Link>
              </li>
              <li>
                <Link href="/security" className="text-slate-300 hover:text-primary transition-colors text-sm flex items-center">
                  <Icon icon="tabler:shield-check" width="16" height="16" className="mr-2" />
                  Security
                </Link>
              </li>
              <li>
                <Link href="/news" className="text-slate-300 hover:text-primary transition-colors text-sm flex items-center">
                  <Icon icon="tabler:news" width="16" height="16" className="mr-2" />
                  News
                </Link>
              </li>
            </ul>
          </div>

          {/* Newsletter & Contact */}
          <div className="lg:col-span-1">
            <h4 className="text-white font-semibold text-lg mb-6">Stay Updated</h4>
            <p className="text-slate-300 text-sm mb-6 leading-relaxed">
              Get the latest cryptocurrency news, market insights, and trading tips delivered to your inbox.
            </p>
            
            <form onSubmit={handleNewsletterSubmit} className="space-y-4">
              <div className="relative">
                <input
                  type="email"
                  name="mail"
                  id="mail"
                  placeholder="Enter your email address"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-slate-800/50 border border-slate-600 rounded-lg py-3 px-4 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all"
                  disabled={isLoading}
                />
                <button
                  type="submit"
                  disabled={isLoading}
                  className="absolute right-2 top-1/2 transform -translate-y-1/2 p-2 text-primary hover:text-white transition-colors disabled:opacity-50"
                >
                  {isLoading ? (
                    <Icon
                      icon="tabler:loader-2"
                      width="20"
                      height="20"
                      className="animate-spin"
                    />
                  ) : (
                    <Icon
                      icon="tabler:send"
                      width="20"
                      height="20"
                    />
                  )}
                </button>
              </div>
              {message && (
                <div className={`text-sm ${
                  message.includes("successful") 
                    ? "text-green-400" 
                    : "text-red-400"
                }`}>
                  {message}
                </div>
              )}
            </form>

            {/* Contact Info */}
            <div className="mt-8 space-y-3">
              <div className="flex items-center space-x-3 text-slate-300 text-sm">
                <Icon icon="tabler:mail" width="16" height="16" className="text-primary" />
                <span>support@fluxor.pro</span>
              </div>
              <div className="flex items-center space-x-3 text-slate-300 text-sm">
                <Icon icon="tabler:phone" width="16" height="16" className="text-primary" />
                <span>+1 (555) 123-4567</span>
              </div>
              <div className="flex items-center space-x-3 text-slate-300 text-sm">
                <Icon icon="tabler:map-pin" width="16" height="16" className="text-primary" />
                <span>New York, NY</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer Bottom */}
      <div className="border-t border-slate-700 bg-slate-900/50">
        <div className="container mx-auto max-w-7xl px-4 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="text-slate-400 text-sm">
              © 2023 Fluxor. All rights reserved. | Professional Cryptocurrency Trading Platform
            </div>
            <div className="flex items-center space-x-6">
              <Link href="/terms" className="text-slate-400 hover:text-primary text-sm transition-colors">
                Terms of Service
              </Link>
              <Link href="/disclosures" className="text-slate-400 hover:text-primary text-sm transition-colors">
                Disclosures
              </Link>
              <Link href="/privacy" className="text-slate-400 hover:text-primary text-sm transition-colors">
                Privacy Policy
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

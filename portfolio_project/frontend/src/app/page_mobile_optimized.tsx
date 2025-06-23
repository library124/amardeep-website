'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Button as MovingBorderButton } from '@/components/ui/moving-border';
import { Pricing } from '@/components/ui/pricing-cards';
import FeaturedBlogPosts from '@/components/FeaturedBlogPosts';
import DhanReferralCard from '@/components/DhanReferralCard';

const HomePage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState('');

  const handleNewsletterSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setMessage('');

    try {
      const response = await fetch('http://localhost:8000/api/newsletter/subscribe/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, name }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(data.message);
        setEmail('');
        setName('');
      } else {
        setMessage(data.email?.[0] || data.message || 'Subscription failed. Please try again.');
      }
    } catch (error) {
      setMessage('Network error. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Hero Section - Mobile Optimized */}
      <section className="container mx-auto px-4 sm:px-6 py-12 sm:py-16 lg:py-20">
        <div className="flex flex-col lg:flex-row items-center justify-between gap-8 lg:gap-12">
          {/* Text Content - Mobile First */}
          <div className="flex-1 text-center lg:text-left order-2 lg:order-1">
            <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 mb-4 sm:mb-6 leading-tight">
              Amardeep Asode
            </h1>
            <h2 className="text-lg sm:text-xl md:text-2xl lg:text-3xl text-blue-600 font-semibold mb-4 sm:mb-6">
              Stock & Intraday Trader
            </h2>
            <p className="text-base sm:text-lg md:text-xl text-gray-600 mb-6 sm:mb-8 leading-relaxed px-2 sm:px-0">
              Expert in intraday strategies for consistent results
            </p>
            <div className="flex justify-center lg:justify-start">
              <MovingBorderButton
                borderRadius="1.75rem"
                className="bg-white dark:bg-slate-900 text-black dark:text-white border-neutral-200 dark:border-slate-800 text-sm sm:text-base px-6 py-3"
                containerClassName="w-auto h-auto"
              >
                Connect with Amardeep
              </MovingBorderButton>
            </div>
          </div>
          
          {/* Owner Image - Mobile Optimized */}
          <div className="flex-1 flex justify-center order-1 lg:order-2">
            <div className="relative">
              {/* Owner Image - Responsive Sizing */}
              <div className="w-64 h-64 sm:w-72 sm:h-72 md:w-80 md:h-80 lg:w-96 lg:h-96 rounded-full overflow-hidden shadow-2xl border-4 border-white">
                <Image
                  src="/owner_landing_page.jpg"
                  alt="Amardeep Asode - Professional Stock & Intraday Trader"
                  width={400}
                  height={400}
                  className="w-full h-full object-cover"
                  priority
                />
              </div>
              
              {/* Decorative Elements - Responsive */}
              <div className="absolute -top-2 -right-2 sm:-top-4 sm:-right-4 w-12 h-12 sm:w-16 sm:h-16 lg:w-20 lg:h-20 bg-blue-500 rounded-full opacity-20 animate-pulse"></div>
              <div className="absolute -bottom-2 -left-2 sm:-bottom-4 sm:-left-4 w-10 h-10 sm:w-12 sm:h-12 lg:w-16 lg:h-16 bg-green-500 rounded-full opacity-20 animate-pulse delay-1000"></div>
              
              {/* Achievement Badge - Mobile Optimized */}
              <div className="absolute top-2 right-2 sm:top-4 sm:right-4 bg-white rounded-full p-2 sm:p-3 shadow-lg">
                <div className="text-center">
                  <div className="text-lg sm:text-xl lg:text-2xl font-bold text-green-600">5+</div>
                  <div className="text-xs text-gray-600">Years</div>
                </div>
              </div>
              
              {/* Success Rate Badge - Mobile Optimized */}
              <div className="absolute bottom-2 left-2 sm:bottom-4 sm:left-4 bg-white rounded-full p-2 sm:p-3 shadow-lg">
                <div className="text-center">
                  <div className="text-lg sm:text-xl lg:text-2xl font-bold text-blue-600">85%</div>
                  <div className="text-xs text-gray-600">Win Rate</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* About Preview - Mobile Optimized */}
      <section className="bg-white py-12 sm:py-16">
        <div className="container mx-auto px-4 sm:px-6">
          <div className="max-w-4xl mx-auto text-center">
            <h3 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-4 sm:mb-6">About Amardeep</h3>
            <p className="text-base sm:text-lg text-gray-600 leading-relaxed mb-3 sm:mb-4 px-2 sm:px-0">
              With over 5 years of experience in stock and intraday trading, Amardeep has developed proven strategies that deliver consistent results. His approach combines technical analysis with disciplined risk management to maximize profits while minimizing losses.
            </p>
            <p className="text-base sm:text-lg text-gray-600 leading-relaxed mb-6 sm:mb-8 px-2 sm:px-0">
              Amardeep believes in empowering fellow traders through education, mentorship, and sharing actionable market insights that can transform trading performance.
            </p>
            <Link href="/about" className="text-blue-600 hover:text-blue-700 font-semibold text-base sm:text-lg transition-colors">
              Learn More →
            </Link>
          </div>
        </div>
      </section>

      {/* Services Section - Mobile Optimized */}
      <section className="py-12 sm:py-16 bg-slate-50">
        <div className="container mx-auto px-4 sm:px-6">
          <h3 className="text-2xl sm:text-3xl font-bold text-gray-900 text-center mb-8 sm:mb-12">Services</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
            <div className="bg-white p-6 sm:p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-blue-100 rounded-lg flex items-center justify-center mb-4 sm:mb-6">
                <span className="text-xl sm:text-2xl">📈</span>
              </div>
              <h4 className="text-lg sm:text-xl font-semibold text-gray-900 mb-3 sm:mb-4">Trading Signals</h4>
              <p className="text-sm sm:text-base text-gray-600 leading-relaxed">
                Real-time trading signals with precise entry and exit points for maximum profitability.
              </p>
            </div>
            <div className="bg-white p-6 sm:p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-blue-100 rounded-lg flex items-center justify-center mb-4 sm:mb-6">
                <span className="text-xl sm:text-2xl">📊</span>
              </div>
              <h4 className="text-lg sm:text-xl font-semibold text-gray-900 mb-3 sm:mb-4">Market Analysis</h4>
              <p className="text-sm sm:text-base text-gray-600 leading-relaxed">
                In-depth market analysis and insights to help you make informed trading decisions.
              </p>
            </div>
            <div className="bg-white p-6 sm:p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow sm:col-span-2 lg:col-span-1">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-blue-100 rounded-lg flex items-center justify-center mb-4 sm:mb-6">
                <span className="text-xl sm:text-2xl">🎯</span>
              </div>
              <h4 className="text-lg sm:text-xl font-semibold text-gray-900 mb-3 sm:mb-4">Mentorship</h4>
              <p className="text-sm sm:text-base text-gray-600 leading-relaxed">
                One-on-one mentorship to develop your trading skills and build winning strategies.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Performance Stats - Mobile Optimized */}
      <section className="py-12 sm:py-16 bg-white">
        <div className="container mx-auto px-4 sm:px-6">
          <h3 className="text-2xl sm:text-3xl font-bold text-gray-900 text-center mb-8 sm:mb-12">Performance Stats</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
            
            {/* Monthly Profit */}
            <article className="flex flex-col gap-3 sm:gap-4 rounded-lg border border-gray-100 bg-white p-4 sm:p-6">
              <div className="inline-flex gap-2 self-end rounded-sm bg-green-100 p-1 text-green-600">
                <svg xmlns="http://www.w3.org/2000/svg" className="size-3 sm:size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
                <span className="text-xs font-medium">67.81%</span>
              </div>
              <div>
                <strong className="block text-xs sm:text-sm font-medium text-gray-500">Monthly Profit</strong>
                <p>
                  <span className="text-lg sm:text-2xl font-medium text-gray-900">₹4,04,320</span>
                  <span className="text-xs text-gray-500 block sm:inline sm:ml-1">from ₹2,40,940</span>
                </p>
              </div>
            </article>

            {/* Win Rate */}
            <article className="flex flex-col gap-3 sm:gap-4 rounded-lg border border-gray-100 bg-white p-4 sm:p-6">
              <div className="inline-flex gap-2 self-end rounded-sm bg-green-100 p-1 text-green-600">
                <svg xmlns="http://www.w3.org/2000/svg" className="size-3 sm:size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
                <span className="text-xs font-medium">+5.2%</span>
              </div>
              <div>
                <strong className="block text-xs sm:text-sm font-medium text-gray-500">Win Rate</strong>
                <p>
                  <span className="text-lg sm:text-2xl font-medium text-gray-900">85.4%</span>
                  <span className="text-xs text-gray-500 block sm:inline sm:ml-1">this month</span>
                </p>
              </div>
            </article>

            {/* Total Trades */}
            <article className="flex flex-col gap-3 sm:gap-4 rounded-lg border border-gray-100 bg-white p-4 sm:p-6">
              <div className="inline-flex gap-2 self-end rounded-sm bg-blue-100 p-1 text-blue-600">
                <svg xmlns="http://www.w3.org/2000/svg" className="size-3 sm:size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <span className="text-xs font-medium">1000+</span>
              </div>
              <div>
                <strong className="block text-xs sm:text-sm font-medium text-gray-500">Total Trades</strong>
                <p>
                  <span className="text-lg sm:text-2xl font-medium text-gray-900">1,247</span>
                  <span className="text-xs text-gray-500 block sm:inline sm:ml-1">executed</span>
                </p>
              </div>
            </article>

            {/* Average Return */}
            <article className="flex flex-col gap-3 sm:gap-4 rounded-lg border border-gray-100 bg-white p-4 sm:p-6">
              <div className="inline-flex gap-2 self-end rounded-sm bg-red-100 p-1 text-red-600">
                <svg xmlns="http://www.w3.org/2000/svg" className="size-3 sm:size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
                </svg>
                <span className="text-xs font-medium">-2.1%</span>
              </div>
              <div>
                <strong className="block text-xs sm:text-sm font-medium text-gray-500">Avg Return</strong>
                <p>
                  <span className="text-lg sm:text-2xl font-medium text-gray-900">12.8%</span>
                  <span className="text-xs text-gray-500 block sm:inline sm:ml-1">per trade</span>
                </p>
              </div>
            </article>

          </div>
        </div>
      </section>

      {/* Featured Blog Posts - Mobile Optimized */}
      <section className="py-12 sm:py-16 bg-white">
        <div className="container mx-auto px-4 sm:px-6">
          <div className="text-center mb-8 sm:mb-12">
            <h3 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-3 sm:mb-4">Latest Trading Insights</h3>
            <p className="text-base sm:text-lg text-gray-600 max-w-2xl mx-auto px-2 sm:px-0">
              Stay updated with the latest market analysis, trading strategies, and insights from Amardeep.
            </p>
          </div>
          <FeaturedBlogPosts />
        </div>
      </section>

      {/* Dhan Referral Card Section */}
      <DhanReferralCard />

      {/* Pricing Section */}
      <Pricing />

      {/* Newsletter Signup - Mobile Optimized */}
      <section className="py-12 sm:py-16 bg-blue-600">
        <div className="container mx-auto px-4 sm:px-6">
          <div className="max-w-2xl mx-auto text-center">
            <h3 className="text-2xl sm:text-3xl font-bold text-white mb-3 sm:mb-4">Get Market Insights from Amardeep</h3>
            <p className="text-blue-100 mb-6 sm:mb-8 text-base sm:text-lg px-2 sm:px-0">
              Subscribe to receive weekly market analysis, trading tips, and exclusive insights directly to your inbox.
            </p>
            {message && (
              <div className={`mb-4 p-3 sm:p-4 rounded-lg mx-2 sm:mx-0 ${message.includes('successful') || message.includes('confirm') ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                <p className="text-sm sm:text-base">{message}</p>
              </div>
            )}
            <form onSubmit={handleNewsletterSubmit} className="flex flex-col gap-3 sm:gap-4 px-2 sm:px-0">
              <div className="flex flex-col gap-3 sm:gap-4">
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Your name (optional)"
                  className="w-full px-4 sm:px-6 py-3 sm:py-4 rounded-lg text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-white text-sm sm:text-base"
                />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email address"
                  className="w-full px-4 sm:px-6 py-3 sm:py-4 rounded-lg text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-white text-sm sm:text-base"
                  required
                />
              </div>
              <button
                type="submit"
                disabled={isSubmitting}
                className="bg-white text-blue-600 font-semibold py-3 sm:py-4 px-6 sm:px-8 rounded-lg hover:bg-gray-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm sm:text-base"
              >
                {isSubmitting ? 'Subscribing...' : 'Subscribe to Trading Insights'}
              </button>
            </form>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
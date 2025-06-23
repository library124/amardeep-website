'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { Button as MovingBorderButton } from '@/components/ui/moving-border';
import { Pricing } from '@/components/ui/pricing-cards';
import FeaturedBlogPosts from '@/components/FeaturedBlogPosts';

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
      {/* Hero Section */}
      <section className="container mx-auto px-6 py-20">
        <div className="flex flex-col lg:flex-row items-center justify-between gap-12">
          <div className="flex-1 text-center lg:text-left">
            <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 mb-6 leading-tight">
              Amardeep Asode
            </h1>
            <h2 className="text-2xl lg:text-3xl text-blue-600 font-semibold mb-6">
              Stock & Intraday Trader
            </h2>
            <p className="text-xl text-gray-600 mb-8 leading-relaxed">
              Expert in intraday strategies for consistent results
            </p>
            <MovingBorderButton
              borderRadius="1.75rem"
              className="bg-white dark:bg-slate-900 text-black dark:text-white border-neutral-200 dark:border-slate-800"
              containerClassName="w-auto h-auto"
            >
              Connect with Amardeep
            </MovingBorderButton>
          </div>
          <div className="flex-1 flex justify-center">
            <div className="w-80 h-80 bg-gradient-to-br from-blue-100 to-slate-200 rounded-full flex items-center justify-center shadow-2xl">
              <div className="w-72 h-72 bg-white rounded-full flex items-center justify-center">
                <span className="text-6xl text-gray-400">👤</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* About Preview */}
      <section className="bg-white py-16">
        <div className="container mx-auto px-6">
          <div className="max-w-4xl mx-auto text-center">
            <h3 className="text-3xl font-bold text-gray-900 mb-6">About Amardeep</h3>
            <p className="text-lg text-gray-600 leading-relaxed mb-4">
              With over 5 years of experience in stock and intraday trading, Amardeep has developed proven strategies that deliver consistent results. His approach combines technical analysis with disciplined risk management to maximize profits while minimizing losses.
            </p>
            <p className="text-lg text-gray-600 leading-relaxed mb-8">
              Amardeep believes in empowering fellow traders through education, mentorship, and sharing actionable market insights that can transform trading performance.
            </p>
            <Link href="/about" className="text-blue-600 hover:text-blue-700 font-semibold text-lg transition-colors">
              Learn More →
            </Link>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="py-16 bg-slate-50">
        <div className="container mx-auto px-6">
          <h3 className="text-3xl font-bold text-gray-900 text-center mb-12">Services</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
              <div className="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center mb-6">
                <span className="text-2xl">📈</span>
              </div>
              <h4 className="text-xl font-semibold text-gray-900 mb-4">Trading Signals</h4>
              <p className="text-gray-600 leading-relaxed">
                Real-time trading signals with precise entry and exit points for maximum profitability.
              </p>
            </div>
            <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
              <div className="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center mb-6">
                <span className="text-2xl">📊</span>
              </div>
              <h4 className="text-xl font-semibold text-gray-900 mb-4">Market Analysis</h4>
              <p className="text-gray-600 leading-relaxed">
                In-depth market analysis and insights to help you make informed trading decisions.
              </p>
            </div>
            <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
              <div className="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center mb-6">
                <span className="text-2xl">🎯</span>
              </div>
              <h4 className="text-xl font-semibold text-gray-900 mb-4">Mentorship</h4>
              <p className="text-gray-600 leading-relaxed">
                One-on-one mentorship to develop your trading skills and build winning strategies.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Performance Stats */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-6">
          <h3 className="text-3xl font-bold text-gray-900 text-center mb-12">Performance Stats</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            
            {/* Monthly Profit */}
            <article className="flex flex-col gap-4 rounded-lg border border-gray-100 bg-white p-6">
              <div className="inline-flex gap-2 self-end rounded-sm bg-green-100 p-1 text-green-600">
                <svg xmlns="http://www.w3.org/2000/svg" className="size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
                <span className="text-xs font-medium">67.81%</span>
              </div>
              <div>
                <strong className="block text-sm font-medium text-gray-500">Monthly Profit</strong>
                <p>
                  <span className="text-2xl font-medium text-gray-900">₹4,04,320</span>
                  <span className="text-xs text-gray-500">from ₹2,40,940</span>
                </p>
              </div>
            </article>

            {/* Win Rate */}
            <article className="flex flex-col gap-4 rounded-lg border border-gray-100 bg-white p-6">
              <div className="inline-flex gap-2 self-end rounded-sm bg-green-100 p-1 text-green-600">
                <svg xmlns="http://www.w3.org/2000/svg" className="size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
                <span className="text-xs font-medium">+5.2%</span>
              </div>
              <div>
                <strong className="block text-sm font-medium text-gray-500">Win Rate</strong>
                <p>
                  <span className="text-2xl font-medium text-gray-900">85.4%</span>
                  <span className="text-xs text-gray-500">this month</span>
                </p>
              </div>
            </article>

            {/* Total Trades */}
            <article className="flex flex-col gap-4 rounded-lg border border-gray-100 bg-white p-6">
              <div className="inline-flex gap-2 self-end rounded-sm bg-blue-100 p-1 text-blue-600">
                <svg xmlns="http://www.w3.org/2000/svg" className="size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <span className="text-xs font-medium">1000+</span>
              </div>
              <div>
                <strong className="block text-sm font-medium text-gray-500">Total Trades</strong>
                <p>
                  <span className="text-2xl font-medium text-gray-900">1,247</span>
                  <span className="text-xs text-gray-500">executed</span>
                </p>
              </div>
            </article>

            {/* Average Return */}
            <article className="flex flex-col gap-4 rounded-lg border border-gray-100 bg-white p-6">
              <div className="inline-flex gap-2 self-end rounded-sm bg-red-100 p-1 text-red-600">
                <svg xmlns="http://www.w3.org/2000/svg" className="size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
                </svg>
                <span className="text-xs font-medium">-2.1%</span>
              </div>
              <div>
                <strong className="block text-sm font-medium text-gray-500">Avg Return</strong>
                <p>
                  <span className="text-2xl font-medium text-gray-900">12.8%</span>
                  <span className="text-xs text-gray-500">per trade</span>
                </p>
              </div>
            </article>

          </div>
        </div>
      </section>

      {/* Featured Blog Posts */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-6">
          <div className="text-center mb-12">
            <h3 className="text-3xl font-bold text-gray-900 mb-4">Latest Trading Insights</h3>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Stay updated with the latest market analysis, trading strategies, and insights from Amardeep.
            </p>
          </div>
          <FeaturedBlogPosts />
        </div>
      </section>

      {/* Pricing Section */}
      <Pricing />

      {/* Newsletter Signup */}
      <section className="py-16 bg-blue-600">
        <div className="container mx-auto px-6">
          <div className="max-w-2xl mx-auto text-center">
            <h3 className="text-3xl font-bold text-white mb-4">Get Market Insights from Amardeep</h3>
            <p className="text-blue-100 mb-8 text-lg">
              Subscribe to receive weekly market analysis, trading tips, and exclusive insights directly to your inbox.
            </p>
            {message && (
              <div className={`mb-4 p-4 rounded-lg ${message.includes('successful') || message.includes('confirm') ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                {message}
              </div>
            )}
            <form onSubmit={handleNewsletterSubmit} className="flex flex-col gap-4">
              <div className="flex flex-col sm:flex-row gap-4">
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Your name (optional)"
                  className="flex-1 px-6 py-4 rounded-lg text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-white"
                />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email address"
                  className="flex-1 px-6 py-4 rounded-lg text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-white"
                  required
                />
              </div>
              <button
                type="submit"
                disabled={isSubmitting}
                className="bg-white text-blue-600 font-semibold py-4 px-8 rounded-lg hover:bg-gray-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
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

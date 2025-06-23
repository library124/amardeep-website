'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { Pricing } from '@/components/ui/pricing-cards';
import { Blog } from '@/components/ui/blog-section-with-rich-preview';
import DhanReferralCard from '@/components/DhanReferralCard';
import { AuroraHero } from '@/components/ui/aurora-hero';
import WorkshopNotifications from '@/components/WorkshopNotifications';

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
    <div className="min-h-screen">
      {/* Aurora Hero Section */}
      <AuroraHero />

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

      {/* Workshop Notifications */}
      <WorkshopNotifications />

      {/* Featured Blog Posts */}
      <Blog />

      {/* Dhan Referral Card Section */}
      <DhanReferralCard />

      {/* Pricing Section */}
      <Pricing />

      {/* Newsletter Signup */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden">
              <div className="grid grid-cols-1 lg:grid-cols-2">
                
                {/* Left Side - Content */}
                <div className="p-8 lg:p-12 flex flex-col justify-center">
                  <div className="mb-6">
                    <div className="inline-flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg mb-4">
                      <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                      </svg>
                    </div>
                    <h3 className="text-2xl md:text-3xl font-bold text-gray-900 mb-4">
                      Stay Updated with Market Insights
                    </h3>
                    <p className="text-gray-600 text-lg leading-relaxed">
                      Get weekly market analysis, trading strategies, and exclusive insights delivered directly to your inbox.
                    </p>
                  </div>
                  
                  {/* Benefits */}
                  <div className="space-y-3">
                    <div className="flex items-center space-x-3">
                      <div className="flex-shrink-0 w-5 h-5 bg-green-100 rounded-full flex items-center justify-center">
                        <svg className="w-3 h-3 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                      </div>
                      <span className="text-gray-700">Weekly market analysis</span>
                    </div>
                    <div className="flex items-center space-x-3">
                      <div className="flex-shrink-0 w-5 h-5 bg-green-100 rounded-full flex items-center justify-center">
                        <svg className="w-3 h-3 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                      </div>
                      <span className="text-gray-700">Exclusive trading tips</span>
                    </div>
                    <div className="flex items-center space-x-3">
                      <div className="flex-shrink-0 w-5 h-5 bg-green-100 rounded-full flex items-center justify-center">
                        <svg className="w-3 h-3 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                      </div>
                      <span className="text-gray-700">No spam, unsubscribe anytime</span>
                    </div>
                  </div>
                </div>

                {/* Right Side - Form */}
                <div className="p-8 lg:p-12 bg-gray-50">
                  <div className="h-full flex flex-col justify-center">
                    
                    {/* Message Display */}
                    {message && (
                      <div className={`mb-6 p-4 rounded-lg border ${
                        message.includes('successful') || message.includes('confirm') 
                          ? 'bg-green-50 border-green-200 text-green-800' 
                          : 'bg-red-50 border-red-200 text-red-800'
                      }`}>
                        <div className="flex items-start">
                          <div className="flex-shrink-0">
                            {message.includes('successful') || message.includes('confirm') ? (
                              <svg className="w-5 h-5 text-green-600 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                              </svg>
                            ) : (
                              <svg className="w-5 h-5 text-red-600 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                              </svg>
                            )}
                          </div>
                          <div className="ml-3">
                            <p className="text-sm font-medium">{message}</p>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Form */}
                    <form onSubmit={handleNewsletterSubmit} className="space-y-4">
                      <div>
                        <label htmlFor="newsletter-name" className="block text-sm font-medium text-gray-700 mb-2">
                          Name (optional)
                        </label>
                        <input
                          id="newsletter-name"
                          type="text"
                          value={name}
                          onChange={(e) => setName(e.target.value)}
                          placeholder="Your name"
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
                        />
                      </div>
                      
                      <div>
                        <label htmlFor="newsletter-email" className="block text-sm font-medium text-gray-700 mb-2">
                          Email address *
                        </label>
                        <input
                          id="newsletter-email"
                          type="email"
                          value={email}
                          onChange={(e) => setEmail(e.target.value)}
                          placeholder="Enter your email"
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
                          required
                        />
                      </div>
                      
                      <button
                        type="submit"
                        disabled={isSubmitting}
                        className="w-full bg-gray-900 text-white font-medium py-3 px-6 rounded-lg hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {isSubmitting ? (
                          <span className="flex items-center justify-center">
                            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Subscribing...
                          </span>
                        ) : (
                          'Subscribe to Newsletter'
                        )}
                      </button>
                    </form>
                    
                    <p className="text-xs text-gray-500 mt-4 text-center">
                      Join 500+ traders getting weekly insights. No spam, ever.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
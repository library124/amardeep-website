'use client';

import React from 'react';
import Link from 'next/link';
import TradingServices from '@/components/TradingServices';
import { Blog } from '@/components/ui/blog-section-with-rich-preview';
import TradingReferrals from '@/components/TradingReferrals';
import { AuroraHero } from '@/components/ui/aurora-hero';
import WorkshopNotifications from '@/components/WorkshopNotifications';

const HomePage: React.FC = () => {
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

      {/* Trading Referrals Section */}
      <TradingReferrals />

      {/* Trading Services Section */}
      <TradingServices />
    </div>
  );
};

export default HomePage;
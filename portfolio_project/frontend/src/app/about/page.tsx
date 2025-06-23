'use client';

import React from 'react';
import { motion } from 'framer-motion';

const AboutPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-white py-20">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
                About Amardeep
              </h1>
              <p className="text-xl text-gray-600 leading-relaxed max-w-3xl mx-auto">
                Passionate intraday trader with 5+ years of experience in navigating financial markets 
                and generating consistent returns through disciplined strategies and risk management.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <section className="py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-6xl mx-auto">
            
            {/* Story Section */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8 md:p-12 mb-12"
            >
              <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">My Journey</h2>
              <div className="prose prose-lg max-w-none text-gray-600 leading-relaxed">
                <p className="mb-6">
                  My journey in trading began several years ago, driven by a fascination with market dynamics 
                  and a desire to master the art of short-term price movements. What started as curiosity 
                  evolved into a disciplined approach to financial markets.
                </p>
                <p className="mb-6">
                  Over the years, I have developed and refined a robust set of trading strategies, focusing on 
                  technical analysis, risk management, and disciplined execution. My expertise lies in identifying 
                  high-probability setups and capitalizing on intraday volatility across various asset classes.
                </p>
                <p>
                  Today, I'm committed to continuous learning and adapting to evolving market conditions while 
                  sharing valuable insights with fellow traders to help them achieve consistent profitability.
                </p>
              </div>
            </motion.div>

            {/* Expertise Grid */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="mb-12"
            >
              <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Areas of Expertise</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                
                <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6 hover:shadow-xl transition-shadow">
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                    <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">Technical Analysis</h3>
                  <p className="text-gray-600">
                    Advanced chart patterns, indicators, and market structure analysis for precise entry and exit points.
                  </p>
                </div>

                <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6 hover:shadow-xl transition-shadow">
                  <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                    <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">Risk Management</h3>
                  <p className="text-gray-600">
                    Disciplined position sizing, stop-loss strategies, and portfolio protection techniques.
                  </p>
                </div>

                <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6 hover:shadow-xl transition-shadow">
                  <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                    <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">Intraday Trading</h3>
                  <p className="text-gray-600">
                    Specialized in short-term price movements across equities, commodities, and forex markets.
                  </p>
                </div>

                <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6 hover:shadow-xl transition-shadow">
                  <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center mb-4">
                    <svg className="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">Market Psychology</h3>
                  <p className="text-gray-600">
                    Understanding market sentiment, crowd behavior, and emotional discipline in trading decisions.
                  </p>
                </div>

                <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6 hover:shadow-xl transition-shadow">
                  <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mb-4">
                    <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">Strategy Development</h3>
                  <p className="text-gray-600">
                    Creating and backtesting systematic trading approaches for consistent market performance.
                  </p>
                </div>

                <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6 hover:shadow-xl transition-shadow">
                  <div className="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-4">
                    <svg className="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">Mentorship</h3>
                  <p className="text-gray-600">
                    Guiding aspiring traders through personalized coaching and educational content.
                  </p>
                </div>

              </div>
            </motion.div>

            {/* Values Section */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.6 }}
              className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8 md:p-12"
            >
              <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Core Values</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                
                <div className="text-center">
                  <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">Discipline</h3>
                  <p className="text-gray-600">
                    Consistent execution of proven strategies without emotional interference.
                  </p>
                </div>

                <div className="text-center">
                  <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">Education</h3>
                  <p className="text-gray-600">
                    Continuous learning and sharing knowledge to elevate the trading community.
                  </p>
                </div>

                <div className="text-center">
                  <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">Excellence</h3>
                  <p className="text-gray-600">
                    Striving for consistent improvement and superior market performance.
                  </p>
                </div>

              </div>
            </motion.div>

          </div>
        </div>
      </section>
    </div>
  );
};

export default AboutPage;
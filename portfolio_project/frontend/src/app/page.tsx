'use client';

import React from 'react';
import Link from 'next/link';
import TradingServices from '@/components/TradingServices';
import { Blog } from '@/components/ui/blog-section-with-rich-preview';
import TradingReferrals from '@/components/TradingReferrals';
import { SplitHero } from '@/components/ui/split-hero';
import WorkshopNotifications from '@/components/WorkshopNotifications';

const HomePage: React.FC = () => {
  return (
    <div className="min-h-screen">
      {/* Split Hero Section */}
      <SplitHero />

      {/* About Preview */}
      <section className="bg-white py-12 sm:py-16 lg:py-20">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto text-center">
            <h3 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-4 sm:mb-6">About Amardeep</h3>
            <p className="text-base sm:text-lg text-gray-600 leading-relaxed mb-3 sm:mb-4">
              With over 5 years of experience in stock and intraday trading, Amardeep has developed proven strategies that deliver consistent results. His approach combines technical analysis with disciplined risk management to maximize profits while minimizing losses.
            </p>
            <p className="text-base sm:text-lg text-gray-600 leading-relaxed mb-6 sm:mb-8">
              Amardeep believes in empowering fellow traders through education, mentorship, and sharing actionable market insights that can transform trading performance.
            </p>
            <Link href="/about" className="inline-flex items-center text-blue-600 hover:text-blue-700 font-semibold text-base sm:text-lg transition-colors group">
              Learn More 
              <svg className="ml-2 w-4 h-4 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
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
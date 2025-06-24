'use client';

import React from 'react';
import Image from 'next/image';
import { motion } from 'framer-motion';

interface ReferralPlatform {
  id: string;
  name: string;
  logo: string;
  description: string;
  features: string[];
  referralLink: string;
  buttonText: string;
}

const TradingReferrals: React.FC = () => {
  // You can update these referral links when you provide them
  const platforms: ReferralPlatform[] = [
    {
      id: 'dhan',
      name: 'Dhan',
      logo: '/dhan.png',
      description: 'Advanced stock trading platform with zero brokerage on equity delivery',
      features: [
        'Zero brokerage on equity delivery',
        'Advanced charting tools',
        'Options & Futures trading',
        'TradingView integration'
      ],
      referralLink: 'http://invite.dhan.co/?invite=MRXHK69413',
      buttonText: 'Join Dhan'
    },
    {
      id: 'delta',
      name: 'Delta Exchange India',
      logo: '/india_delta.png',
      description: 'India\'s premier crypto derivatives platform for Bitcoin & Ethereum F&O',
      features: [
        'Crypto futures & options',
        'INR settlement',
        '24/7 trading',
        'FIU registered & compliant'
      ],
      referralLink: 'https://www.delta.exchange/?code=OPRAWU',
      buttonText: 'Join Delta'
    }
  ];

  return (
    <section className="py-20 bg-gray-50">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          
          {/* Header */}
          <div className="text-center mb-16">
            <motion.h2 
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="text-3xl md:text-4xl font-bold text-gray-900 mb-4"
            >
              Start Your Trading Journey
            </motion.h2>
            <motion.p 
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="text-lg text-gray-600 max-w-3xl mx-auto"
            >
              Join these trusted platforms through my referral and support my work while getting access to premium trading tools
            </motion.p>
          </div>

          {/* Platform Cards */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {platforms.map((platform, index) => (
              <motion.div
                key={platform.id}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl transition-shadow duration-300"
              >
                {/* Platform Header */}
                <div className="p-8 pb-6">
                  <div className="flex items-center justify-center mb-6">
                    <div className="relative w-32 h-16">
                      <Image
                        src={platform.logo}
                        alt={`${platform.name} logo`}
                        fill
                        className="object-contain"
                        priority
                      />
                    </div>
                  </div>
                  
                  <h3 className="text-2xl font-bold text-gray-900 text-center mb-3">
                    {platform.name}
                  </h3>
                  
                  <p className="text-gray-600 text-center leading-relaxed mb-6">
                    {platform.description}
                  </p>
                </div>

                {/* Features */}
                <div className="px-8 pb-6">
                  <h4 className="font-semibold text-gray-900 mb-4">Key Features</h4>
                  <div className="space-y-3">
                    {platform.features.map((feature, featureIndex) => (
                      <div key={featureIndex} className="flex items-center space-x-3">
                        <div className="w-5 h-5 rounded-full bg-green-100 flex items-center justify-center flex-shrink-0">
                          <svg className="w-3 h-3 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                          </svg>
                        </div>
                        <span className="text-gray-700 text-sm">{feature}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* CTA Button */}
                <div className="px-8 pb-8">
                  <a
                    href={platform.referralLink}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-full inline-flex items-center justify-center px-6 py-4 bg-gray-900 text-white font-semibold rounded-xl hover:bg-gray-800 transform hover:scale-105 transition-all duration-300 shadow-lg"
                  >
                    <span>{platform.buttonText}</span>
                    <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                  </a>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Support Message */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="text-center mt-12"
          >
            <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100 max-w-2xl mx-auto">
              <div className="flex items-center justify-center mb-4">
                <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                  <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                </div>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Support My Work</h3>
              <p className="text-gray-600">
                By using my referral links, you help support my trading education content while getting access to excellent platforms. 
                Thank you for your support!
              </p>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default TradingReferrals;

'use client';

import React, { useState } from 'react';
import Image from 'next/image';
import { motion } from 'framer-motion';

const DhanReferralCard: React.FC = () => {
  const [imageError, setImageError] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const dhanCardImagePath = '/dhan_card.jpg';

  const handleImageError = () => {
    setImageError(true);
  };

  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  return (
    <>
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto">
            
            {/* Header */}
            <div className="text-center mb-16">
              <motion.h2 
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
                className="text-3xl md:text-4xl font-bold text-gray-900 mb-4"
              >
                Join Dhan Trading
              </motion.h2>
              <motion.p 
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.1 }}
                className="text-lg text-gray-600 max-w-2xl mx-auto"
              >
                Support my journey while getting access to zero-brokerage trading and advanced tools
              </motion.p>
            </div>

            {/* Main Card */}
            <motion.div 
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.2 }}
              className="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden"
            >
              <div className="grid grid-cols-1 lg:grid-cols-2">
                
                {/* Left Side - QR Code */}
                <div className="p-8 lg:p-12 flex flex-col items-center justify-center bg-gradient-to-br from-gray-50 to-white">
                  <div className="w-full max-w-sm">
                    {!imageError ? (
                      <div 
                        className="cursor-pointer transition-all duration-300 hover:scale-105"
                        onClick={openModal}
                      >
                        <Image
                          src={dhanCardImagePath}
                          alt="Dhan referral QR code"
                          width={400}
                          height={300}
                          className="w-full h-auto rounded-xl shadow-lg"
                          onError={handleImageError}
                          priority
                        />
                      </div>
                    ) : (
                      <div className="w-full aspect-[4/3] bg-gray-100 rounded-xl flex flex-col items-center justify-center border-2 border-dashed border-gray-300">
                        <div className="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mb-4">
                          <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                          </svg>
                        </div>
                        <p className="text-gray-500 text-sm text-center">
                          QR Code will appear here
                        </p>
                      </div>
                    )}
                    
                    <button 
                      onClick={openModal}
                      className="w-full mt-6 bg-gray-900 text-white font-medium py-3 px-6 rounded-lg hover:bg-gray-800 transition-colors duration-200"
                    >
                      View QR Code
                    </button>
                  </div>
                </div>

                {/* Right Side - Information */}
                <div className="p-8 lg:p-12">
                  <div className="h-full flex flex-col justify-center">
                    
                    <h3 className="text-2xl font-semibold text-gray-900 mb-6">
                      How it works
                    </h3>
                    
                    <div className="space-y-6 mb-8">
                      <div className="flex items-start space-x-4">
                        <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                          <span className="text-blue-600 font-semibold text-sm">1</span>
                        </div>
                        <div>
                          <p className="font-medium text-gray-900">Scan the QR code</p>
                          <p className="text-gray-600 text-sm mt-1">Use your phone camera or Dhan app</p>
                        </div>
                      </div>
                      
                      <div className="flex items-start space-x-4">
                        <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                          <span className="text-blue-600 font-semibold text-sm">2</span>
                        </div>
                        <div>
                          <p className="font-medium text-gray-900">Download & register</p>
                          <p className="text-gray-600 text-sm mt-1">Complete your account setup</p>
                        </div>
                      </div>
                      
                      <div className="flex items-start space-x-4">
                        <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                          <span className="text-blue-600 font-semibold text-sm">3</span>
                        </div>
                        <div>
                          <p className="font-medium text-gray-900">Start trading</p>
                          <p className="text-gray-600 text-sm mt-1">Enjoy zero brokerage benefits</p>
                        </div>
                      </div>
                    </div>

                    {/* Benefits */}
                    <div className="bg-gray-50 rounded-lg p-6">
                      <h4 className="font-semibold text-gray-900 mb-4">Key Benefits</h4>
                      <ul className="space-y-2">
                        <li className="flex items-center text-sm text-gray-700">
                          <svg className="w-4 h-4 text-green-500 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                          </svg>
                          Zero brokerage on equity delivery
                        </li>
                        <li className="flex items-center text-sm text-gray-700">
                          <svg className="w-4 h-4 text-green-500 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                          </svg>
                          Advanced trading tools
                        </li>
                        <li className="flex items-center text-sm text-gray-700">
                          <svg className="w-4 h-4 text-green-500 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                          </svg>
                          Instant account opening
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Support Message */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="text-center mt-12"
            >
              <p className="text-gray-600 max-w-2xl mx-auto">
                By using my referral, you help support my work while getting access to excellent trading benefits. 
                Thank you for your support!
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Modal */}
      {isModalOpen && (
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
          onClick={closeModal}
        >
          <motion.div 
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="bg-white rounded-2xl p-8 max-w-lg w-full"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-semibold text-gray-900">Dhan Referral QR Code</h3>
              <button
                onClick={closeModal}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            {!imageError ? (
              <div className="text-center">
                <Image
                  src={dhanCardImagePath}
                  alt="Dhan referral QR code"
                  width={400}
                  height={300}
                  className="w-full h-auto rounded-lg"
                  onError={handleImageError}
                />
                <p className="text-gray-600 mt-4 text-sm">
                  Scan with your phone camera or Dhan app
                </p>
              </div>
            ) : (
              <div className="text-center">
                <div className="w-full aspect-[4/3] bg-gray-100 rounded-lg flex flex-col items-center justify-center">
                  <div className="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mb-4">
                    <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                    </svg>
                  </div>
                  <p className="text-gray-500">QR Code not available</p>
                </div>
              </div>
            )}
          </motion.div>
        </motion.div>
      )}
    </>
  );
};

export default DhanReferralCard;
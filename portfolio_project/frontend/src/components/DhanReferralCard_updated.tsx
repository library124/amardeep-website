'use client';

import React, { useState } from 'react';
import Image from 'next/image';

const DhanReferralCard: React.FC = () => {
  const [imageError, setImageError] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Using the existing Dhan card image from public directory
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
      <section className="py-16 bg-gradient-to-br from-green-50 to-blue-50">
        <div className="container mx-auto px-6">
          <div className="max-w-6xl mx-auto">
            {/* Section Header */}
            <div className="text-center mb-12">
              <h3 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
                🚀 Support Me on Dhan!
              </h3>
              <p className="text-lg text-gray-600 max-w-3xl mx-auto leading-relaxed">
                Join Dhan through my referral and help me earn rewards while you get access to exciting offers too!
              </p>
            </div>

            {/* Main Content */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
              
              {/* Left Side - Information */}
              <div className="space-y-6">
                <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100">
                  <h4 className="text-2xl font-semibold text-gray-900 mb-4 flex items-center">
                    <span className="text-3xl mr-3">📱</span>
                    How to Use My Referral
                  </h4>
                  
                  <div className="space-y-4">
                    <div className="flex items-start space-x-3">
                      <div className="flex-shrink-0 w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                        <span className="text-green-600 font-bold text-sm">1</span>
                      </div>
                      <div>
                        <p className="text-gray-700 font-medium">Download the Dhan app</p>
                        <p className="text-gray-600 text-sm">Available on Google Play Store and App Store</p>
                      </div>
                    </div>
                    
                    <div className="flex items-start space-x-3">
                      <div className="flex-shrink-0 w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                        <span className="text-green-600 font-bold text-sm">2</span>
                      </div>
                      <div>
                        <p className="text-gray-700 font-medium">Scan the QR code</p>
                        <p className="text-gray-600 text-sm">Use your phone camera or Dhan app to scan</p>
                      </div>
                    </div>
                    
                    <div className="flex items-start space-x-3">
                      <div className="flex-shrink-0 w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                        <span className="text-green-600 font-bold text-sm">3</span>
                      </div>
                      <div>
                        <p className="text-gray-700 font-medium">Complete your registration</p>
                        <p className="text-gray-600 text-sm">Sign up and start trading with exclusive benefits</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Benefits Section */}
                <div className="bg-gradient-to-r from-green-500 to-blue-600 p-8 rounded-2xl text-white">
                  <h4 className="text-xl font-semibold mb-4 flex items-center">
                    <span className="text-2xl mr-3">🎁</span>
                    Your Benefits
                  </h4>
                  <ul className="space-y-2">
                    <li className="flex items-center">
                      <span className="text-green-200 mr-2">✓</span>
                      Zero brokerage on equity delivery trades
                    </li>
                    <li className="flex items-center">
                      <span className="text-green-200 mr-2">✓</span>
                      Advanced trading tools and charts
                    </li>
                    <li className="flex items-center">
                      <span className="text-green-200 mr-2">✓</span>
                      Instant account opening
                    </li>
                    <li className="flex items-center">
                      <span className="text-green-200 mr-2">✓</span>
                      24/7 customer support
                    </li>
                  </ul>
                </div>
              </div>

              {/* Right Side - QR Code Card */}
              <div className="flex justify-center">
                <div className="bg-white p-8 rounded-2xl shadow-2xl border border-gray-200 max-w-md w-full">
                  <div className="text-center mb-6">
                    <h4 className="text-xl font-semibold text-gray-900 mb-2">
                      Scan to Join Dhan
                    </h4>
                    <p className="text-gray-600 text-sm">
                      Use your phone camera to scan this QR code
                    </p>
                  </div>

                  {/* QR Code Image */}
                  <div className="relative mb-6">
                    {!imageError ? (
                      <div 
                        className="cursor-pointer transition-transform hover:scale-105"
                        onClick={openModal}
                      >
                        <Image
                          src={dhanCardImagePath}
                          alt="Dhan referral card with QR code - Support Amardeep Asode"
                          width={400}
                          height={300}
                          className="w-full h-auto rounded-lg shadow-lg"
                          onError={handleImageError}
                          priority
                        />
                      </div>
                    ) : (
                      // Fallback when image is not available
                      <div className="w-full h-64 bg-gradient-to-br from-green-100 to-blue-100 rounded-lg flex flex-col items-center justify-center border-2 border-dashed border-gray-300">
                        <div className="text-6xl mb-4">📱</div>
                        <p className="text-gray-600 text-center px-4">
                          Dhan Referral QR Code
                        </p>
                        <p className="text-gray-500 text-sm text-center px-4 mt-2">
                          Image not found at /dhan_card.jpg
                        </p>
                      </div>
                    )}
                  </div>

                  {/* Call to Action */}
                  <div className="text-center">
                    <button 
                      className="w-full bg-gradient-to-r from-green-500 to-blue-600 text-white font-semibold py-4 px-6 rounded-lg hover:from-green-600 hover:to-blue-700 transition-all duration-300 transform hover:scale-105 shadow-lg"
                      onClick={openModal}
                    >
                      <span className="flex items-center justify-center">
                        <span className="text-xl mr-2">📱</span>
                        Scan now and start benefiting!
                      </span>
                    </button>
                    
                    <p className="text-gray-500 text-xs mt-3">
                      Thank you for your support! 🙏
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Additional Information */}
            <div className="mt-12 text-center">
              <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-100 max-w-4xl mx-auto">
                <p className="text-gray-700 leading-relaxed">
                  <strong>Support Me on Dhan!</strong> Scan the QR code below to join Dhan through my referral. 
                  When you use my code, you help me earn rewards, and you get access to exciting offers too! 
                  Thank you for your support! 🚀
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Modal for enlarged QR code */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl p-8 max-w-2xl w-full max-h-[90vh] overflow-auto">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-2xl font-bold text-gray-900">Dhan Referral QR Code</h3>
              <button
                onClick={closeModal}
                className="text-gray-500 hover:text-gray-700 text-3xl font-bold"
              >
                ×
              </button>
            </div>
            
            {!imageError ? (
              <div className="text-center">
                <Image
                  src={dhanCardImagePath}
                  alt="Dhan referral card with QR code - Support Amardeep Asode"
                  width={600}
                  height={450}
                  className="w-full h-auto rounded-lg shadow-lg"
                  onError={handleImageError}
                />
                <p className="text-gray-600 mt-4">
                  Scan this QR code with your phone camera or Dhan app
                </p>
              </div>
            ) : (
              <div className="text-center">
                <div className="w-full h-96 bg-gradient-to-br from-green-100 to-blue-100 rounded-lg flex flex-col items-center justify-center border-2 border-dashed border-gray-300">
                  <div className="text-8xl mb-4">📱</div>
                  <p className="text-gray-600 text-xl">Dhan Referral QR Code</p>
                  <p className="text-gray-500 mt-2 px-4">
                    Image not found at /dhan_card.jpg
                  </p>
                </div>
              </div>
            )}
            
            <div className="mt-6 text-center">
              <button
                onClick={closeModal}
                className="bg-gray-500 text-white px-6 py-3 rounded-lg hover:bg-gray-600 transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default DhanReferralCard;
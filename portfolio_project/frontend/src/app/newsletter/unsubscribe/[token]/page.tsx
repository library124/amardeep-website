'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';

const UnsubscribePage: React.FC = () => {
  const params = useParams();
  const token = params.token as string;
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('');
  const [email, setEmail] = useState('');

  useEffect(() => {
    const unsubscribe = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/newsletter/unsubscribe/${token}/`);
        const data = await response.json();

        if (response.ok) {
          setStatus('success');
          setMessage(data.message);
          setEmail(data.email);
        } else {
          setStatus('error');
          setMessage(data.error || 'Unsubscribe failed');
        }
      } catch (error) {
        setStatus('error');
        setMessage('Network error occurred');
      }
    };

    if (token) {
      unsubscribe();
    }
  }, [token]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center">
      <div className="max-w-md mx-auto bg-white p-8 rounded-lg shadow-lg text-center">
        {status === 'loading' && (
          <>
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Processing Unsubscribe...</h2>
            <p className="text-gray-600">Please wait while we process your request.</p>
          </>
        )}

        {status === 'success' && (
          <>
            <div className="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Successfully Unsubscribed</h2>
            <p className="text-gray-600 mb-6">{message}</p>
            {email && (
              <p className="text-sm text-gray-500 mb-6">
                Unsubscribed: <strong>{email}</strong>
              </p>
            )}
            <div className="bg-gray-50 p-4 rounded-lg mb-6">
              <p className="text-gray-700 mb-2">We're sorry to see you go!</p>
              <p className="text-sm text-gray-600">
                You will no longer receive trading insights and market analysis emails from Amardeep Asode.
              </p>
            </div>
            <div className="text-sm text-gray-600">
              <p>Changed your mind? You can always subscribe again from our homepage.</p>
            </div>
          </>
        )}

        {status === 'error' && (
          <>
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Unsubscribe Failed</h2>
            <p className="text-gray-600 mb-6">{message}</p>
            <p className="text-sm text-gray-500">
              If you continue to have issues, please contact support.
            </p>
          </>
        )}

        <div className="mt-8">
          <Link 
            href="/" 
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
          >
            Return to Homepage
          </Link>
        </div>
      </div>
    </div>
  );
};

export default UnsubscribePage;
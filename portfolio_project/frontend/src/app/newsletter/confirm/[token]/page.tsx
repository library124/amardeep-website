'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';

const ConfirmSubscriptionPage: React.FC = () => {
  const params = useParams();
  const token = params.token as string;
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('');
  const [email, setEmail] = useState('');

  useEffect(() => {
    const confirmSubscription = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/newsletter/confirm/${token}/`);
        const data = await response.json();

        if (response.ok) {
          setStatus('success');
          setMessage(data.message);
          setEmail(data.email);
        } else {
          setStatus('error');
          setMessage(data.error || 'Confirmation failed');
        }
      } catch (error) {
        setStatus('error');
        setMessage('Network error occurred');
      }
    };

    if (token) {
      confirmSubscription();
    }
  }, [token]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center">
      <div className="max-w-md mx-auto bg-white p-8 rounded-lg shadow-lg text-center">
        {status === 'loading' && (
          <>
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Confirming Subscription...</h2>
            <p className="text-gray-600">Please wait while we confirm your subscription.</p>
          </>
        )}

        {status === 'success' && (
          <>
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Subscription Confirmed!</h2>
            <p className="text-gray-600 mb-6">{message}</p>
            {email && (
              <p className="text-sm text-gray-500 mb-6">
                Confirmed for: <strong>{email}</strong>
              </p>
            )}
            <div className="space-y-3">
              <p className="text-gray-700">You'll now receive:</p>
              <ul className="text-left text-gray-600 space-y-1">
                <li>• Weekly market analysis</li>
                <li>• Trading tips and strategies</li>
                <li>• Exclusive insights from Amardeep</li>
                <li>• Performance updates</li>
              </ul>
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
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Confirmation Failed</h2>
            <p className="text-gray-600 mb-6">{message}</p>
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

export default ConfirmSubscriptionPage;
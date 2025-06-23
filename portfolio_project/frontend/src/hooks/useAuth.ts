'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../context/AuthContext';

const useAuthProtection = (redirectPath = '/login') => {
  const { isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push(redirectPath);
    }
  }, [isAuthenticated, router, redirectPath]);

  return isAuthenticated;
};

export default useAuthProtection;
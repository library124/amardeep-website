'use client';

import React, { createContext, useState, useContext, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface AuthContextType {
  isAuthenticated: boolean;
  login: (token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const router = useRouter();

  useEffect(() => {
    // Check for token in localStorage or httpOnly cookie on initial load
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('jwt_token');
      if (token) {
        setIsAuthenticated(true);
      }
    }
  }, []);

  const login = (token: string) => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('jwt_token', token);
    }
    setIsAuthenticated(true);
    router.push('/dashboard');
  };

  const logout = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('jwt_token');
    }
    setIsAuthenticated(false);
    router.push('/login');
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
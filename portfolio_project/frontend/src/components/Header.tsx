'use client';

import Link from 'next/link';
import { useAuth } from '../context/AuthContext';
import { usePathname } from 'next/navigation';
import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Logo from './Logo';

const Header: React.FC = () => {
  const { isAuthenticated, logout } = useAuth();
  const pathname = usePathname();
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [hoveredItem, setHoveredItem] = useState<string | null>(null);

  const navItems = [
    { href: '/', label: 'Home' },
    { href: '/about', label: 'About' },
    { href: '/courses', label: 'Courses' },
    { href: '/achievements', label: 'Performance' },
    { href: '/products', label: 'Services' },
    { href: '/blog', label: 'Blog' },
    { href: '/contact', label: 'Contact' },
  ];

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const isActive = (href: string) => {
    if (href === '/') {
      return pathname === '/';
    }
    return pathname.startsWith(href);
  };

  return (
    <header 
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled 
          ? 'bg-white/80 backdrop-blur-md border-b border-gray-200/50 shadow-sm' 
          : 'bg-white/10 backdrop-blur-sm'
      }`}
    >
      <nav className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20 sm:h-24">
          {/* Logo */}
          <Logo 
            size="xl" 
            isScrolled={isScrolled} 
            showText={false}
            className="flex-shrink-0"
          />

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-1">
            <div className="flex items-center space-x-1 relative">
              {navItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`relative px-3 py-2 text-sm font-medium rounded-md transition-colors duration-200 ${
                    isActive(item.href)
                      ? isScrolled 
                        ? 'text-gray-900' 
                        : 'text-gray-900'
                      : isScrolled 
                        ? 'text-gray-600 hover:text-gray-900' 
                        : 'text-gray-700 hover:text-gray-900'
                  }`}
                  onMouseEnter={() => setHoveredItem(item.href)}
                  onMouseLeave={() => setHoveredItem(null)}
                >
                  <span className="relative z-10">{item.label}</span>
                  
                  {/* Hover background */}
                  {hoveredItem === item.href && (
                    <motion.div
                      layoutId="navbar-hover"
                      className={`absolute inset-0 rounded-md ${
                        isScrolled 
                          ? 'bg-gray-100' 
                          : 'bg-white/20'
                      }`}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      transition={{
                        type: "spring",
                        bounce: 0.25,
                        stiffness: 130,
                        damping: 9,
                        duration: 0.3
                      }}
                    />
                  )}
                  
                  {/* Active indicator */}
                  {isActive(item.href) && (
                    <motion.div
                      layoutId="navbar-active"
                      className={`absolute inset-0 rounded-md ${
                        isScrolled 
                          ? 'bg-gray-900/5 border border-gray-900/10' 
                          : 'bg-white/30 border border-white/30'
                      }`}
                      transition={{
                        type: "spring",
                        bounce: 0.25,
                        stiffness: 130,
                        damping: 9,
                        duration: 0.3
                      }}
                    />
                  )}
                </Link>
              ))}
            </div>

            {/* Auth buttons */}
            <div className="flex items-center space-x-2 ml-6">
              {isAuthenticated ? (
                <>
                  <Link
                    href="/dashboard"
                    className={`px-3 py-2 text-sm font-medium rounded-md transition-colors duration-200 ${
                      isScrolled 
                        ? 'text-gray-600 hover:text-gray-900 hover:bg-gray-100' 
                        : 'text-gray-700 hover:text-gray-900 hover:bg-white/20'
                    }`}
                  >
                    Dashboard
                  </Link>
                  <button
                    onClick={logout}
                    className={`px-3 py-2 text-sm font-medium rounded-md transition-colors duration-200 ${
                      isScrolled 
                        ? 'text-gray-600 hover:text-gray-900 hover:bg-gray-100' 
                        : 'text-gray-700 hover:text-gray-900 hover:bg-white/20'
                    }`}
                  >
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link
                    href="/login"
                    className={`px-3 py-2 text-sm font-medium rounded-md transition-colors duration-200 ${
                      isScrolled 
                        ? 'text-gray-600 hover:text-gray-900 hover:bg-gray-100' 
                        : 'text-gray-700 hover:text-gray-900 hover:bg-white/20'
                    }`}
                  >
                    Login
                  </Link>
                  <Link
                    href="/signup"
                    className={`px-4 py-2 text-sm font-medium rounded-md transition-all duration-200 ${
                      isScrolled 
                        ? 'bg-gray-900 text-white hover:bg-gray-800' 
                        : 'bg-gray-900 text-white hover:bg-gray-800'
                    }`}
                  >
                    Sign Up
                  </Link>
                </>
              )}
            </div>
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className={`md:hidden p-2 rounded-md transition-colors duration-200 ${
              isScrolled 
                ? 'text-gray-600 hover:text-gray-900 hover:bg-gray-100' 
                : 'text-gray-700 hover:text-gray-900 hover:bg-white/20'
            }`}
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              {isMobileMenuOpen ? (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              ) : (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Navigation */}
        <AnimatePresence>
          {isMobileMenuOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.2 }}
              className="md:hidden border-t border-gray-200/50 bg-white/95 backdrop-blur-md"
            >
              <div className="px-2 pt-2 pb-3 space-y-1">
                {navItems.map((item) => (
                  <Link
                    key={item.href}
                    href={item.href}
                    onClick={() => setIsMobileMenuOpen(false)}
                    className={`block px-3 py-2 text-base font-medium rounded-md transition-colors duration-200 ${
                      isActive(item.href)
                        ? 'text-gray-900 bg-gray-100'
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                    }`}
                  >
                    {item.label}
                  </Link>
                ))}
                
                <div className="border-t border-gray-200/50 pt-3 mt-3">
                  {isAuthenticated ? (
                    <>
                      <Link
                        href="/dashboard"
                        onClick={() => setIsMobileMenuOpen(false)}
                        className="block px-3 py-2 text-base font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md transition-colors duration-200"
                      >
                        Dashboard
                      </Link>
                      <button
                        onClick={() => {
                          logout();
                          setIsMobileMenuOpen(false);
                        }}
                        className="block w-full text-left px-3 py-2 text-base font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md transition-colors duration-200"
                      >
                        Logout
                      </button>
                    </>
                  ) : (
                    <>
                      <Link
                        href="/login"
                        onClick={() => setIsMobileMenuOpen(false)}
                        className="block px-3 py-2 text-base font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md transition-colors duration-200"
                      >
                        Login
                      </Link>
                      <Link
                        href="/signup"
                        onClick={() => setIsMobileMenuOpen(false)}
                        className="block px-3 py-2 text-base font-medium bg-gray-900 text-white hover:bg-gray-800 rounded-md transition-colors duration-200 mt-2"
                      >
                        Sign Up
                      </Link>
                    </>
                  )}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </nav>
    </header>
  );
};

export default Header;
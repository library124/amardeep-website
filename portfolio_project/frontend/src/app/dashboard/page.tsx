'use client';

import React from 'react';
import useAuthProtection from '../../hooks/useAuth';

const DashboardPage: React.FC = () => {
  useAuthProtection(); // Protect this route

  return (
    <div className="container mx-auto p-8">
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
      <p className="text-lg">Welcome to your personalized dashboard!</p>
      {/* Add more dashboard content here, e.g., user stats, recent activities */}
    </div>
  );
};

export default DashboardPage;
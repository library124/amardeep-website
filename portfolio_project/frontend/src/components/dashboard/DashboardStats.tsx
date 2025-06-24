'use client';

import React from 'react';
import { DashboardData } from '../../types';

interface DashboardStatsProps {
  data: DashboardData;
}

const DashboardStats: React.FC<DashboardStatsProps> = ({ data }) => {
  const stats = [
    {
      title: 'Total Courses',
      value: data.courses_count,
      icon: '📚',
      color: 'bg-blue-500'
    },
    {
      title: 'Active Courses',
      value: data.active_courses_count,
      icon: '🎯',
      color: 'bg-green-500'
    },
    {
      title: 'Completed Courses',
      value: data.purchased_courses.filter(course => course.status === 'completed').length,
      icon: '✅',
      color: 'bg-purple-500'
    },
    {
      title: 'Member Since',
      value: new Date(data.user.date_joined).getFullYear(),
      icon: '📅',
      color: 'bg-orange-500'
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {stats.map((stat, index) => (
        <div key={index} className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">{stat.title}</p>
              <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
            </div>
            <div className={`${stat.color} rounded-full p-3 text-white text-2xl`}>
              {stat.icon}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default DashboardStats;
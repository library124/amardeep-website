'use client';

import React, { useEffect, useState } from 'react';
import api from '../../utils/api';
import { Achievement } from '../../types';

const AchievementsPage: React.FC = () => {
  const [achievements, setAchievements] = useState<Achievement[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchAchievements = async () => {
      try {
        const response = await api.get('/achievements/'); // Assuming Django API endpoint for achievements
        setAchievements(response.data);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to fetch achievements.');
      } finally {
        setLoading(false);
      }
    };

    fetchAchievements();
  }, []);

  if (loading) {
    return <div className="container mx-auto p-8 text-center">Loading achievements...</div>;
  }

  if (error) {
    return <div className="container mx-auto p-8 text-center text-red-500">{error}</div>;
  }

  return (
    <div className="container mx-auto p-8">
      <h1 className="text-3xl font-bold mb-6">My Achievements</h1>
      {achievements.length === 0 ? (
        <p className="text-lg text-gray-600">No achievements found.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {achievements.map((achievement) => (
            <div key={achievement.id} className="bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-xl font-semibold mb-2">{achievement.title}</h2>
              <p className="text-gray-700 mb-2">{achievement.description}</p>
              <p className="text-gray-500 text-sm">Date: {achievement.date}</p>
              <div className="text-gray-600 text-sm mt-1">
                <strong>Metrics:</strong>
                {Object.entries(achievement.metrics).map(([key, value]) => (
                  <span key={key} className="block">
                    {key}: {typeof value === 'number' ? value.toLocaleString() : value}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AchievementsPage;
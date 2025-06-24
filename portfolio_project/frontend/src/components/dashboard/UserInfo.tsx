'use client';

import React from 'react';
import { User, UserProfile } from '../../types';

interface UserInfoProps {
  user: User;
  profile: UserProfile | null;
}

const UserInfo: React.FC<UserInfoProps> = ({ user, profile }) => {
  const getExperienceColor = (experience: string) => {
    switch (experience) {
      case 'beginner':
        return 'bg-green-100 text-green-800';
      case 'intermediate':
        return 'bg-yellow-100 text-yellow-800';
      case 'advanced':
        return 'bg-orange-100 text-orange-800';
      case 'expert':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getMarketIcon = (market: string) => {
    switch (market) {
      case 'equity':
        return '📈';
      case 'options':
        return '⚡';
      case 'futures':
        return '🔮';
      case 'forex':
        return '💱';
      case 'crypto':
        return '₿';
      default:
        return '📊';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4">Personal Information</h2>
      
      <div className="flex items-start gap-6">
        {/* Profile Picture */}
        <div className="flex-shrink-0">
          {profile?.profile_picture ? (
            <img
              src={profile.profile_picture}
              alt="Profile"
              className="w-20 h-20 rounded-full object-cover border-2 border-gray-200"
            />
          ) : (
            <div className="w-20 h-20 rounded-full bg-gray-200 flex items-center justify-center text-2xl font-semibold text-gray-600">
              {user.first_name ? user.first_name.charAt(0).toUpperCase() : user.username.charAt(0).toUpperCase()}
            </div>
          )}
        </div>

        {/* User Details */}
        <div className="flex-1">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-sm text-gray-500">Full Name</label>
              <p className="font-medium">
                {user.first_name && user.last_name 
                  ? `${user.first_name} ${user.last_name}` 
                  : profile?.full_name || user.username}
              </p>
            </div>
            
            <div>
              <label className="text-sm text-gray-500">Email</label>
              <p className="font-medium">{user.email}</p>
            </div>
            
            {profile?.phone && (
              <div>
                <label className="text-sm text-gray-500">Phone</label>
                <p className="font-medium">{profile.phone}</p>
              </div>
            )}
            
            {profile?.date_of_birth && (
              <div>
                <label className="text-sm text-gray-500">Date of Birth</label>
                <p className="font-medium">{new Date(profile.date_of_birth).toLocaleDateString()}</p>
              </div>
            )}
            
            <div>
              <label className="text-sm text-gray-500">Member Since</label>
              <p className="font-medium">{new Date(user.date_joined).toLocaleDateString()}</p>
            </div>
            
            {profile?.trading_experience && (
              <div>
                <label className="text-sm text-gray-500">Trading Experience</label>
                <div className="flex items-center gap-2">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getExperienceColor(profile.trading_experience)}`}>
                    {profile.trading_experience.charAt(0).toUpperCase() + profile.trading_experience.slice(1)}
                  </span>
                </div>
              </div>
            )}
            
            {profile?.preferred_market && (
              <div>
                <label className="text-sm text-gray-500">Preferred Market</label>
                <div className="flex items-center gap-2">
                  <span className="text-lg">{getMarketIcon(profile.preferred_market)}</span>
                  <p className="font-medium capitalize">{profile.preferred_market}</p>
                </div>
              </div>
            )}
          </div>
          
          {profile?.bio && (
            <div className="mt-4">
              <label className="text-sm text-gray-500">Bio</label>
              <p className="font-medium text-gray-700">{profile.bio}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UserInfo;
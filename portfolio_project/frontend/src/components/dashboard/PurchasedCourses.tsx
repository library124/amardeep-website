'use client';

import React from 'react';
import { PurchasedCourse } from '../../types';

interface PurchasedCoursesProps {
  courses: PurchasedCourse[];
}

const PurchasedCourses: React.FC<PurchasedCoursesProps> = ({ courses }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800';
      case 'completed':
        return 'bg-blue-100 text-blue-800';
      case 'expired':
        return 'bg-red-100 text-red-800';
      case 'cancelled':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getCourseTypeIcon = (type: string) => {
    switch (type) {
      case 'workshop':
        return '🎯';
      case 'mentorship':
        return '👨‍🏫';
      case 'signals':
        return '📊';
      case 'course':
        return '📚';
      default:
        return '📖';
    }
  };

  if (courses.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">Purchased Courses</h2>
        <div className="text-center py-8">
          <div className="text-6xl mb-4">📚</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Courses Purchased</h3>
          <p className="text-gray-600 mb-4">
            You haven't purchased any courses yet. Explore our available courses and workshops to get started.
          </p>
          <a
            href="/workshops"
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
          >
            Browse Courses
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4">Purchased Courses ({courses.length})</h2>
      <div className="space-y-4">
        {courses.map((course) => (
          <div key={course.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-2xl">{getCourseTypeIcon(course.course_type)}</span>
                  <h3 className="font-semibold text-lg">{course.course_name}</h3>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(course.status)}`}>
                    {course.status.charAt(0).toUpperCase() + course.status.slice(1)}
                  </span>
                </div>
                
                {course.description && (
                  <p className="text-gray-600 mb-3">{course.description}</p>
                )}
                
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  <div>
                    <span className="text-gray-500">Purchase Date:</span>
                    <p className="font-medium">{new Date(course.purchase_date).toLocaleDateString()}</p>
                  </div>
                  <div>
                    <span className="text-gray-500">Amount Paid:</span>
                    <p className="font-medium">{course.price_display}</p>
                  </div>
                  <div>
                    <span className="text-gray-500">Progress:</span>
                    <div className="flex items-center gap-2">
                      <div className="flex-1 bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-blue-600 h-2 rounded-full" 
                          style={{ width: `${course.progress_percentage}%` }}
                        ></div>
                      </div>
                      <span className="font-medium">{course.progress_percentage}%</span>
                    </div>
                  </div>
                  {course.days_remaining && course.days_remaining > 0 && (
                    <div>
                      <span className="text-gray-500">Days Remaining:</span>
                      <p className="font-medium text-orange-600">{course.days_remaining} days</p>
                    </div>
                  )}
                </div>
                
                {course.last_accessed && (
                  <div className="mt-2 text-sm text-gray-500">
                    Last accessed: {new Date(course.last_accessed).toLocaleDateString()}
                  </div>
                )}
              </div>
              
              <div className="ml-4">
                {course.is_active && course.access_url && (
                  <a
                    href={course.access_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center px-3 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors text-sm"
                  >
                    Access Course
                  </a>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PurchasedCourses;
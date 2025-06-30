'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { courseApi } from '../lib/courseApi';
import PaymentButton from './PaymentButton';
import { Course } from '../types';

export default function FeaturedCourses() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchFeaturedCourses();
  }, []);

  const fetchFeaturedCourses = async () => {
    try {
      const data = await courseApi.getFeaturedCourses();
      setCourses(data.slice(0, 3)); // Show only 3 featured courses
    } catch (error) {
      console.error('Error fetching featured courses:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900">Featured Courses</h2>
            <p className="mt-4 text-lg text-gray-600">
              Start your trading journey with our most popular courses
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[1, 2, 3].map((i) => (
              <div key={i} className="bg-white rounded-lg shadow-md overflow-hidden animate-pulse">
                <div className="h-48 bg-gray-200"></div>
                <div className="p-6">
                  <div className="h-4 bg-gray-200 rounded mb-2"></div>
                  <div className="h-6 bg-gray-200 rounded mb-4"></div>
                  <div className="h-4 bg-gray-200 rounded mb-4"></div>
                  <div className="h-8 bg-gray-200 rounded"></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    );
  }

  if (courses.length === 0) {
    return null;
  }

  return (
    <section className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900">Featured Courses</h2>
          <p className="mt-4 text-lg text-gray-600">
            Start your trading journey with our most popular courses
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {courses.map((course) => (
            <div key={course.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
              {/* Course Image */}
              <div className="relative h-48">
                {course.featured_image ? (
                  <Image
                    src={course.featured_image}
                    alt={course.title}
                    fill
                    className="object-cover"
                  />
                ) : (
                  <div className="w-full h-full bg-gray-200 flex items-center justify-center">
                    <span className="text-gray-400">No Image</span>
                  </div>
                )}
                <div className="absolute top-4 left-4 bg-yellow-500 text-white px-2 py-1 rounded-md text-sm font-medium">
                  Featured
                </div>
                {course.discount_percentage > 0 && (
                  <div className="absolute top-4 right-4 bg-red-500 text-white px-2 py-1 rounded-md text-sm font-medium">
                    {course.discount_percentage}% OFF
                  </div>
                )}
              </div>

              {/* Course Content */}
              <div className="p-6">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-blue-600 font-medium capitalize">
                    {course.course_type.replace('_', ' ')}
                  </span>
                  <span className="text-sm text-gray-500 capitalize">
                    {course.difficulty_level}
                  </span>
                </div>

                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {course.title}
                </h3>

                <p className="text-gray-600 mb-4 line-clamp-2">
                  {course.short_description}
                </p>

                <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                  <span>{course.duration_display}</span>
                  <span>{course.enrolled_count} enrolled</span>
                </div>

                <div className="flex items-center justify-between mb-4">
                  <div>
                    <span className="text-2xl font-bold text-gray-900">
                      {course.price_display}
                    </span>
                    {course.original_price_display && (
                      <span className="text-lg text-gray-500 line-through ml-2">
                        {course.original_price_display}
                      </span>
                    )}
                  </div>
                  <span className="text-sm text-gray-600">
                    by {course.instructor_name}
                  </span>
                </div>

                <div className="flex gap-2">
                  <Link
                    href={`/courses/${course.slug}`}
                    className="flex-1 bg-gray-100 text-gray-700 text-center py-2 px-4 rounded-md font-medium hover:bg-gray-200 transition-colors"
                  >
                    Learn More
                  </Link>
                  <PaymentButton
                    item={course}
                    itemType="course"
                    className="flex-1"
                    size="sm"
                  >
                    Enroll Now
                  </PaymentButton>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="text-center mt-12">
          <Link
            href="/courses"
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-blue-600 bg-blue-100 hover:bg-blue-200 transition-colors"
          >
            View All Courses
            <svg className="ml-2 -mr-1 w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </Link>
        </div>
      </div>
    </section>
  );
}
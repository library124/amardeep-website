'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { motion } from 'framer-motion';
import { courseApi } from '../../lib/courseApi';
import PaymentButton from '../../components/PaymentButton';
import { Course } from '../../types';

// Loading component following Single Responsibility Principle
const LoadingState: React.FC = () => (
  <div className="min-h-screen bg-white flex items-center justify-center">
    <div className="text-center">
      <div className="w-6 h-6 border-2 border-gray-200 border-t-gray-900 rounded-full animate-spin mx-auto mb-3"></div>
      <p className="text-gray-600 text-sm">Loading courses...</p>
    </div>
  </div>
);

// Error component following Single Responsibility Principle
const ErrorState: React.FC<{ error: string; onRetry: () => void }> = ({ error, onRetry }) => (
  <div className="min-h-screen bg-white flex items-center justify-center">
    <div className="text-center max-w-md">
      <div className="w-10 h-10 bg-red-50 rounded-lg flex items-center justify-center mx-auto mb-4">
        <svg className="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
        </svg>
      </div>
      <h3 className="text-lg font-medium text-gray-900 mb-2">Something went wrong</h3>
      <p className="text-gray-600 text-sm mb-6">{error}</p>
      <button 
        onClick={onRetry}
        className="inline-flex items-center px-4 py-2 border border-gray-200 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 transition-colors"
      >
        Try again
      </button>
    </div>
  </div>
);

// Filter component following Single Responsibility Principle
interface FilterProps {
  filters: {
    type: string;
    difficulty: string;
    featured: boolean;
  };
  onFilterChange: (key: string, value: string | boolean) => void;
  onClearFilters: () => void;
  courseCount: number;
}

const CourseFilters: React.FC<FilterProps> = ({ filters, onFilterChange, onClearFilters, courseCount }) => {
  const hasActiveFilters = Boolean(filters.type || filters.difficulty || filters.featured);

  return (
    <div className="space-y-6">
      {/* Filter Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <h2 className="text-lg font-medium text-gray-900">
            {courseCount} {courseCount === 1 ? 'course' : 'courses'}
          </h2>
          {hasActiveFilters && (
            <button
              onClick={onClearFilters}
              className="text-sm text-gray-600 hover:text-gray-900 transition-colors"
            >
              Clear all filters
            </button>
          )}
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3">
        {/* Type Filter */}
        <div className="relative">
          <select
            value={filters.type}
            onChange={(e) => onFilterChange('type', e.target.value)}
            className="appearance-none bg-white border border-gray-200 rounded-lg px-4 py-2 pr-8 text-sm font-medium text-gray-700 hover:border-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent transition-colors"
          >
            <option value="">All types</option>
            <option value="video">Video Course</option>
            <option value="live">Live Course</option>
            <option value="workshop">Workshop</option>
            <option value="mentorship">Mentorship</option>
            <option value="signals">Trading Signals</option>
          </select>
          <div className="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
            <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>

        {/* Level Filter */}
        <div className="relative">
          <select
            value={filters.difficulty}
            onChange={(e) => onFilterChange('difficulty', e.target.value)}
            className="appearance-none bg-white border border-gray-200 rounded-lg px-4 py-2 pr-8 text-sm font-medium text-gray-700 hover:border-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent transition-colors"
          >
            <option value="">All levels</option>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
            <option value="expert">Expert</option>
          </select>
          <div className="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
            <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>

        {/* Featured Filter */}
        <button
          onClick={() => onFilterChange('featured', !filters.featured)}
          className={`px-4 py-2 text-sm font-medium rounded-lg border transition-colors ${
            filters.featured
              ? 'bg-gray-900 text-white border-gray-900'
              : 'bg-white text-gray-700 border-gray-200 hover:border-gray-300'
          }`}
        >
          Featured only
        </button>
      </div>
    </div>
  );
};

// Course card component following Single Responsibility Principle
const CourseCard: React.FC<{ course: Course; index: number }> = ({ course, index }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.4, delay: index * 0.05 }}
    className="group bg-white border border-gray-200 rounded-xl overflow-hidden hover:shadow-lg hover:border-gray-300 transition-all duration-300"
  >
    {/* Course Image */}
    <div className="relative aspect-[16/10] bg-gray-50 overflow-hidden">
      {course.featured_image ? (
        <Image
          src={course.featured_image}
          alt={course.title}
          fill
          className="object-cover group-hover:scale-105 transition-transform duration-500"
        />
      ) : (
        <div className="w-full h-full flex items-center justify-center">
          <div className="w-12 h-12 bg-gray-100 rounded-xl flex items-center justify-center">
            <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          </div>
        </div>
      )}
      
      {/* Badges */}
      <div className="absolute top-4 left-4 flex gap-2">
        {course.is_featured && (
          <span className="px-2.5 py-1 bg-yellow-100 text-yellow-800 text-xs font-medium rounded-md backdrop-blur-sm">
            Featured
          </span>
        )}
        {course.discount_percentage > 0 && (
          <span className="px-2.5 py-1 bg-red-100 text-red-800 text-xs font-medium rounded-md backdrop-blur-sm">
            {course.discount_percentage}% off
          </span>
        )}
      </div>
    </div>

    {/* Course Content */}
    <div className="p-6">
      {/* Meta info */}
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-medium text-gray-600 uppercase tracking-wider">
          {course.course_type.replace('_', ' ')}
        </span>
        <span className="text-xs text-gray-500 capitalize bg-gray-50 px-2 py-1 rounded-md">
          {course.difficulty_level}
        </span>
      </div>

      {/* Title */}
      <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2 group-hover:text-gray-700 transition-colors">
        {course.title}
      </h3>

      {/* Description */}
      <p className="text-gray-600 text-sm mb-4 line-clamp-2 leading-relaxed">
        {course.short_description}
      </p>

      {/* Stats */}
      <div className="flex items-center gap-4 text-xs text-gray-500 mb-5">
        <div className="flex items-center gap-1">
          <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>{course.duration_display}</span>
        </div>
        <div className="flex items-center gap-1">
          <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
          <span>{course.lessons_count} lessons</span>
        </div>
        <div className="flex items-center gap-1">
          <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
          </svg>
          <span>{course.enrolled_count} enrolled</span>
        </div>
      </div>

      {/* Price and instructor */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-baseline gap-2">
          <span className="text-xl font-semibold text-gray-900">
            {course.price_display}
          </span>
          {course.original_price_display && (
            <span className="text-sm text-gray-500 line-through">
              {course.original_price_display}
            </span>
          )}
        </div>
        <span className="text-xs text-gray-500">
          by {course.instructor_name}
        </span>
      </div>

      {/* Actions */}
      <div className="flex gap-3">
        <Link
          href={`/courses/${course.slug}`}
          className="flex-1 px-4 py-2.5 text-sm font-medium text-gray-700 border border-gray-200 rounded-lg hover:bg-gray-50 hover:border-gray-300 transition-all text-center"
        >
          View details
        </Link>
        <PaymentButton
          item={course}
          itemType="course"
          className={`flex-1 px-4 py-2.5 text-sm font-medium rounded-lg transition-all text-center ${
            course.is_full 
              ? 'bg-gray-100 text-gray-500 cursor-not-allowed' 
              : 'bg-gray-900 text-white hover:bg-gray-800'
          }`}
          disabled={course.is_full}
        >
          {course.is_full ? 'Course full' : 'Enroll now'}
        </PaymentButton>
      </div>
    </div>
  </motion.div>
);

// Empty state component following Single Responsibility Principle
const EmptyState: React.FC<{ hasFilters: boolean; onClearFilters: () => void }> = ({ hasFilters, onClearFilters }) => (
  <div className="text-center py-20">
    <div className="w-16 h-16 bg-gray-50 rounded-2xl flex items-center justify-center mx-auto mb-6">
      <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
      </svg>
    </div>
    <h3 className="text-lg font-medium text-gray-900 mb-2">
      {hasFilters ? 'No courses match your filters' : 'No courses found'}
    </h3>
    <p className="text-gray-600 text-sm mb-6">
      {hasFilters 
        ? 'Try adjusting your filters to see more results.' 
        : 'Check back later for new courses.'}
    </p>
    {hasFilters && (
      <button
        onClick={onClearFilters}
        className="inline-flex items-center px-4 py-2 border border-gray-200 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 transition-colors"
      >
        Clear all filters
      </button>
    )}
  </div>
);

// Main component following Open/Closed Principle
export default function CoursesPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState({
    type: '',
    difficulty: '',
    featured: false
  });

  useEffect(() => {
    fetchCourses();
  }, [filters]);

  const fetchCourses = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await courseApi.getCourses(filters);
      setCourses(data);
    } catch (err) {
      setError('Failed to load courses. Please try again.');
      console.error('Error fetching courses:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key: string, value: string | boolean) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleClearFilters = () => {
    setFilters({ type: '', difficulty: '', featured: false });
  };

  const hasActiveFilters = Boolean(filters.type || filters.difficulty || filters.featured);

  if (loading) return <LoadingState />;
  if (error) return <ErrorState error={error} onRetry={fetchCourses} />;

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <div className="border-b border-gray-100">
        <div className="max-w-6xl mx-auto px-6 py-20">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center"
          >
            <h1 className="text-5xl font-bold text-gray-900 mb-6">
              Trading Courses
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
              Master the markets with our comprehensive trading courses designed for every skill level.
            </p>
          </motion.div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        {/* Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="mb-12"
        >
          <CourseFilters
            filters={filters}
            onFilterChange={handleFilterChange}
            onClearFilters={handleClearFilters}
            courseCount={courses.length}
          />
        </motion.div>

        {/* Course Grid */}
        {courses.length === 0 ? (
          <EmptyState hasFilters={hasActiveFilters} onClearFilters={handleClearFilters} />
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
          >
            {courses.map((course, index) => (
              <CourseCard key={course.id} course={course} index={index} />
            ))}
          </motion.div>
        )}
      </div>
    </div>
  );
}
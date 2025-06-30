'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Image from 'next/image';
import { motion } from 'framer-motion';
import { courseApi } from '../../../lib/courseApi';
import { useAuth } from '../../../context/AuthContext';
import PaymentButton from '../../../components/PaymentButton';

interface Course {
  id: number;
  title: string;
  slug: string;
  short_description: string;
  description: string;
  featured_image: string;
  preview_video?: string;
  course_type: string;
  difficulty_level: string;
  duration_display: string;
  lessons_count: number;
  price: number;
  price_display: string;
  original_price_display?: string;
  discount_percentage: number;
  what_you_learn: string;
  requirements: string;
  course_content: any[];
  instructor_name: string;
  is_featured: boolean;
  enrolled_count: number;
  is_full: boolean;
  spots_remaining?: number;
}

// Loading component following Single Responsibility Principle
const LoadingState: React.FC = () => (
  <div className="min-h-screen bg-white flex items-center justify-center">
    <div className="text-center">
      <div className="w-8 h-8 border-2 border-gray-200 border-t-gray-900 rounded-full animate-spin mx-auto mb-4"></div>
      <p className="text-gray-600 text-sm">Loading course details...</p>
    </div>
  </div>
);

// Error component following Single Responsibility Principle
const ErrorState: React.FC<{ error: string; onBack: () => void }> = ({ error, onBack }) => (
  <div className="min-h-screen bg-white flex items-center justify-center">
    <div className="text-center max-w-md">
      <div className="w-12 h-12 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
        </svg>
      </div>
      <h3 className="text-lg font-medium text-gray-900 mb-2">Course not found</h3>
      <p className="text-gray-600 text-sm mb-6">{error}</p>
      <button 
        onClick={onBack}
        className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 transition-colors"
      >
        ← Go back
      </button>
    </div>
  </div>
);

// Course stats component following Single Responsibility Principle
const CourseStats: React.FC<{ course: Course }> = ({ course }) => (
  <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
    <div className="text-center">
      <div className="text-2xl font-semibold text-gray-900 mb-1">{course.duration_display}</div>
      <div className="text-sm text-gray-600">Duration</div>
    </div>
    <div className="text-center">
      <div className="text-2xl font-semibold text-gray-900 mb-1">{course.lessons_count}</div>
      <div className="text-sm text-gray-600">Lessons</div>
    </div>
    <div className="text-center">
      <div className="text-2xl font-semibold text-gray-900 mb-1">{course.enrolled_count}</div>
      <div className="text-sm text-gray-600">Students</div>
    </div>
    <div className="text-center">
      <div className="text-2xl font-semibold text-gray-900 mb-1">
        {course.spots_remaining || '∞'}
      </div>
      <div className="text-sm text-gray-600">Spots left</div>
    </div>
  </div>
);

// Course content section following Single Responsibility Principle
const CourseContent: React.FC<{ title: string; content: string; icon: React.ReactNode }> = ({ title, content, icon }) => (
  <div className="border border-gray-200 rounded-lg p-6">
    <div className="flex items-center gap-3 mb-4">
      <div className="w-8 h-8 bg-gray-100 rounded-lg flex items-center justify-center">
        {icon}
      </div>
      <h2 className="text-lg font-semibold text-gray-900">{title}</h2>
    </div>
    <div className="space-y-2">
      {content.split('\n').filter(item => item.trim()).map((item, index) => (
        <div key={index} className="flex items-start gap-2">
          <div className="w-1.5 h-1.5 bg-gray-400 rounded-full mt-2 flex-shrink-0"></div>
          <span className="text-gray-700 text-sm">{item.trim()}</span>
        </div>
      ))}
    </div>
  </div>
);

// Purchase sidebar component following Single Responsibility Principle
const PurchaseSidebar: React.FC<{ course: Course; user: any; onPaymentSuccess: (result: any) => void; onPaymentError: (error: any) => void; onLogin: () => void }> = ({ 
  course, 
  user, 
  onPaymentSuccess, 
  onPaymentError, 
  onLogin 
}) => (
  <div className="border border-gray-200 rounded-lg p-6 sticky top-8">
    {/* Preview Video */}
    {course.preview_video && (
      <div className="mb-6">
        <video
          controls
          className="w-full rounded-lg border border-gray-200"
          poster={course.featured_image}
        >
          <source src={course.preview_video} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      </div>
    )}

    {/* Pricing */}
    <div className="text-center mb-6">
      <div className="text-3xl font-semibold text-gray-900 mb-2">
        {course.price_display}
      </div>
      {course.original_price_display && (
        <div className="text-lg text-gray-500 line-through mb-1">
          {course.original_price_display}
        </div>
      )}
      {course.discount_percentage > 0 && (
        <div className="text-green-600 font-medium text-sm">
          Save {course.discount_percentage}%
        </div>
      )}
    </div>

    {/* Purchase Button */}
    {user ? (
      <PaymentButton
        item={course}
        itemType="course"
        onPaymentSuccess={onPaymentSuccess}
        onPaymentError={onPaymentError}
        className="w-full mb-6 px-4 py-3 bg-gray-900 text-white rounded-md hover:bg-gray-800 transition-colors font-medium"
        disabled={course.is_full}
      >
        {course.is_full ? 'Course Full' : 'Enroll Now'}
      </PaymentButton>
    ) : (
      <button
        onClick={onLogin}
        className="w-full mb-6 px-4 py-3 bg-gray-900 text-white rounded-md hover:bg-gray-800 transition-colors font-medium"
      >
        Login to Enroll
      </button>
    )}

    {/* Course Features */}
    <div className="pt-6 border-t border-gray-200">
      <h3 className="font-medium text-gray-900 mb-4">This course includes</h3>
      <div className="space-y-3 text-sm">
        <div className="flex items-center gap-2">
          <svg className="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
          <span className="text-gray-700">{course.duration_display} of content</span>
        </div>
        <div className="flex items-center gap-2">
          <svg className="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
          <span className="text-gray-700">{course.lessons_count} lessons</span>
        </div>
        <div className="flex items-center gap-2">
          <svg className="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
          <span className="text-gray-700">Lifetime access</span>
        </div>
        <div className="flex items-center gap-2">
          <svg className="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
          <span className="text-gray-700">Certificate of completion</span>
        </div>
        <div className="flex items-center gap-2">
          <svg className="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
          <span className="text-gray-700">30-day money-back guarantee</span>
        </div>
      </div>
    </div>
  </div>
);

// Main component following Open/Closed Principle
export default function CourseDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { user } = useAuth();
  const [course, setCourse] = useState<Course | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (params.slug) {
      fetchCourse(params.slug as string);
    }
  }, [params.slug]);

  const fetchCourse = async (slug: string) => {
    try {
      setLoading(true);
      setError(null);
      const data = await courseApi.getCourse(slug);
      setCourse(data);
    } catch (err) {
      setError('Failed to load course details. Please try again.');
      console.error('Error fetching course:', err);
    } finally {
      setLoading(false);
    }
  };

  const handlePaymentSuccess = (result: any) => {
    alert(result.message || 'Course purchased successfully!');
    router.push('/dashboard');
  };

  const handlePaymentError = (error: any) => {
    console.error('Payment failed:', error);
    alert('Payment failed. Please try again.');
  };

  const handleLogin = () => {
    router.push('/login');
  };

  const handleBack = () => {
    router.back();
  };

  if (loading) return <LoadingState />;
  if (error || !course) return <ErrorState error={error || 'Course not found'} onBack={handleBack} />;

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <div className="border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-6 py-12">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            {/* Breadcrumb */}
            <nav className="mb-8">
              <button
                onClick={handleBack}
                className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900 transition-colors"
              >
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                Back to courses
              </button>
            </nav>

            {/* Course Header */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
              <div className="lg:col-span-2">
                {/* Badges */}
                <div className="flex items-center gap-3 mb-4">
                  <span className="px-3 py-1 bg-gray-100 text-gray-800 text-sm font-medium rounded-full capitalize">
                    {course.course_type.replace('_', ' ')}
                  </span>
                  <span className="px-3 py-1 bg-gray-100 text-gray-800 text-sm font-medium rounded-full capitalize">
                    {course.difficulty_level}
                  </span>
                  {course.is_featured && (
                    <span className="px-3 py-1 bg-yellow-100 text-yellow-800 text-sm font-medium rounded-full">
                      Featured
                    </span>
                  )}
                </div>

                {/* Title */}
                <h1 className="text-4xl font-bold text-gray-900 mb-4">
                  {course.title}
                </h1>

                {/* Description */}
                <p className="text-lg text-gray-600 mb-6">
                  {course.short_description}
                </p>

                {/* Stats */}
                <CourseStats course={course} />

                {/* Instructor */}
                <div className="mt-8 pt-8 border-t border-gray-200">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
                      <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                    </div>
                    <div>
                      <div className="font-medium text-gray-900">Instructor</div>
                      <div className="text-gray-600">{course.instructor_name}</div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Course Image */}
              <div className="lg:col-span-1">
                <div className="relative aspect-video bg-gray-100 rounded-lg overflow-hidden">
                  {course.featured_image ? (
                    <Image
                      src={course.featured_image}
                      alt={course.title}
                      fill
                      className="object-cover"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center">
                      <div className="w-16 h-16 bg-gray-200 rounded-lg flex items-center justify-center">
                        <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                        </svg>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-6xl mx-auto px-6 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Course Description */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
            >
              <div className="border border-gray-200 rounded-lg p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">About this course</h2>
                <div className="prose prose-gray max-w-none">
                  {course.description.split('\n').map((paragraph, index) => (
                    <p key={index} className="text-gray-700 mb-4 last:mb-0">{paragraph}</p>
                  ))}
                </div>
              </div>
            </motion.div>

            {/* What You'll Learn */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <CourseContent
                title="What you'll learn"
                content={course.what_you_learn}
                icon={
                  <svg className="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                }
              />
            </motion.div>

            {/* Requirements */}
            {course.requirements && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.3 }}
              >
                <CourseContent
                  title="Requirements"
                  content={course.requirements}
                  icon={
                    <svg className="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  }
                />
              </motion.div>
            )}
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
            >
              <PurchaseSidebar
                course={course}
                user={user}
                onPaymentSuccess={handlePaymentSuccess}
                onPaymentError={handlePaymentError}
                onLogin={handleLogin}
              />
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}
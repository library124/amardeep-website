export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  date_joined: string;
  profile?: UserProfile;
}

export interface UserProfile {
  phone: string;
  date_of_birth: string;
  bio: string;
  profile_picture: string;
  trading_experience: 'beginner' | 'intermediate' | 'advanced' | 'expert';
  preferred_market: 'equity' | 'options' | 'futures' | 'forex' | 'crypto';
  
  newsletter_subscribed: boolean;
  email_notifications: boolean;
  sms_notifications: boolean;
  full_name: string;
  display_name: string;
  created_at: string;
  updated_at: string;
}

export interface PurchasedCourse {
  id: number;
  course_name: string;
  course_type: 'workshop' | 'mentorship' | 'signals' | 'course';
  description: string;
  purchase_date: string;
  start_date: string;
  end_date: string;
  status: 'active' | 'completed' | 'expired' | 'cancelled';
  amount_paid: number;
  currency: string;
  price_display: string;
  access_url: string;
  progress_percentage: number;
  last_accessed: string;
  is_active: boolean;
  days_remaining: number;
  created_at: string;
}

export interface DashboardData {
  user: User;
  profile: UserProfile;
  purchased_courses: PurchasedCourse[];
  courses_count: number;
  active_courses_count: number;
}

export interface ChangePasswordData {
  old_password: string;
  new_password: string;
  confirm_password: string;
}

export interface AuthResponse {
  token: string;
  user: User;
}

export interface Achievement {
  id: number;
  title: string;
  description: string;
  date: string;
  metrics: Record<string, string | number | boolean>;
  user: number;
}

export interface Product {
  id: number;
  name: string;
  description: string;
  price: number | string;
  download_link: string;
}

export interface Workshop {
  id: number;
  title: string;
  slug: string;
  short_description: string;
  description: string;
  featured_image: string;
  instructor_name: string;
  is_paid: boolean;
  price: number;
  currency: string;
  price_display: string;
  start_date: string;
  end_date: string;
  duration_hours: number;
  duration_display: string;
  max_participants: number;
  registered_count: number;
  spots_remaining: number;
  is_full: boolean;
  status: 'upcoming' | 'ongoing' | 'completed' | 'cancelled';
  is_featured: boolean;
  requirements: string;
  what_you_learn: string;
  is_upcoming: boolean;
  is_ongoing: boolean;
  is_completed: boolean;
  created_at: string;
}

// Course content structure following Single Responsibility Principle
export interface CourseLesson {
  id: number;
  title: string;
  duration: number;
  video_url?: string;
  content?: string;
  order: number;
}

export interface CourseModule {
  id: number;
  title: string;
  description: string;
  lessons: CourseLesson[];
  order: number;
}

export interface Course {
  id: number;
  title: string;
  slug: string;
  short_description: string;
  description: string;
  featured_image: string;
  preview_video?: string;
  course_type: 'video' | 'live' | 'workshop' | 'mentorship' | 'signals';
  difficulty_level: 'beginner' | 'intermediate' | 'advanced' | 'expert';
  duration_hours: number;
  duration_display: string;
  lessons_count: number;
  price: number;
  original_price?: number;
  currency: string;
  price_display: string;
  original_price_display?: string;
  discount_percentage: number;
  what_you_learn: string;
  requirements: string;
  course_content: CourseModule[];
  instructor_name: string;
  is_active: boolean;
  is_featured: boolean;
  max_students?: number;
  enrolled_count: number;
  is_full: boolean;
  spots_remaining?: number;
  created_at: string;
  updated_at: string;
}

// Payment related interfaces following Interface Segregation Principle
export interface PaymentOrder {
  order_id: string;
  amount: number;
  currency: string;
  course_title?: string;
  workshop_title?: string;
  service_name?: string;
  course_price?: string;
}

export interface PaymentSuccess {
  success: boolean;
  message: string;
  order_id: string;
}

export interface CreateOrderRequest {
  course_id?: number;
  workshop_id?: number;
  service_id?: number;
  amount: number;
  currency: string;
}

export interface PaymentSuccessRequest {
  razorpay_payment_id: string;
  razorpay_order_id: string;
  razorpay_signature: string;
}

// API Response types following Dependency Inversion Principle
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  errors?: Record<string, string[]>;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// Form data interfaces
export interface ContactFormData {
  name: string;
  email: string;
  subject: string;
  message: string;
}

export interface WorkshopApplicationData {
  name: string;
  email: string;
  phone?: string;
  experience_level: 'beginner' | 'intermediate' | 'advanced';
  motivation?: string;
}

export interface ServiceBookingData {
  name: string;
  email: string;
  phone: string;
  message?: string;
  preferred_contact_method: 'whatsapp' | 'call' | 'email';
  preferred_time?: string;
}
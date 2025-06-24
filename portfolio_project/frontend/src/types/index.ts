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
  token: string; // Assuming JWT token
  user: User;
}

export interface Achievement {
  id: number;
  title: string;
  description: string;
  date: string;
  metrics: Record<string, any>;
  user: number;
  // Add other achievement fields as needed
}

export interface Product {
  id: number;
  name: string;
  description: string;
  price: number | string; // Django DecimalField can be serialized as string
  download_link: string;
  // Add other product fields as needed
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

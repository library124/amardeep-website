export interface User {
  id: number;
  username: string;
  email: string;
  // Add other user fields as needed
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
import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';
import { enhancedApiService, ApiUtils } from '../services/EnhancedApiService';

const API_BASE_URL = process.env.NEXT_PUBLIC_DJANGO_API_URL || 'http://localhost:8000/api'; // Default to local Django API

// Legacy axios instance for backward compatibility
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Check if we're in the browser before accessing localStorage
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('jwt_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// Enhanced API wrapper with fallback mechanisms
const enhancedApi = {
  async get(endpoint: string, params?: any) {
    try {
      const response = await enhancedApiService.get(endpoint, params);
      return { data: ApiUtils.handleResponse(response) };
    } catch (error) {
      // Fallback to legacy axios for backward compatibility
      console.warn('Enhanced API failed, falling back to legacy axios');
      return await api.get(endpoint, { params });
    }
  },

  async post(endpoint: string, data?: any) {
    try {
      const response = await enhancedApiService.post(endpoint, data);
      return { data: ApiUtils.handleResponse(response) };
    } catch (error) {
      // Fallback to legacy axios for backward compatibility
      console.warn('Enhanced API failed, falling back to legacy axios');
      return await api.post(endpoint, data);
    }
  },

  async put(endpoint: string, data?: any) {
    try {
      const response = await enhancedApiService.put(endpoint, data);
      return { data: ApiUtils.handleResponse(response) };
    } catch (error) {
      // Fallback to legacy axios for backward compatibility
      console.warn('Enhanced API failed, falling back to legacy axios');
      return await api.put(endpoint, data);
    }
  },

  async delete(endpoint: string) {
    try {
      const response = await enhancedApiService.delete(endpoint);
      return { data: ApiUtils.handleResponse(response) };
    } catch (error) {
      // Fallback to legacy axios for backward compatibility
      console.warn('Enhanced API failed, falling back to legacy axios');
      return await api.delete(endpoint);
    }
  },

  // Health check method
  async checkHealth() {
    return await enhancedApiService.checkHealth();
  },

  // Get API status
  async getStatus() {
    return await enhancedApiService.getApiStatus();
  }
};

// Export both for flexibility
export default enhancedApi;
export { api as legacyApi };
export { enhancedApiService, ApiUtils };
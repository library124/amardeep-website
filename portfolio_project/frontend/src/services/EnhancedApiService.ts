// Enhanced API Service with health checks and fallback mechanisms
// Following SOLID principles for robust API communication

import axios, { AxiosError, AxiosResponse } from 'axios';
import { apiHealthService, HealthUtils } from './ApiHealthService';
import { ErrorUtils } from './ErrorHandlingService';

// Interface for API request configuration
export interface ApiRequestConfig {
  endpoint: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  data?: any;
  params?: any;
  headers?: Record<string, string>;
  timeout?: number;
  retries?: number;
  useFallback?: boolean;
}

// Interface for API response
export interface ApiResponse<T = any> {
  success: boolean;
  data: T;
  message?: string;
  error?: string;
  fromFallback?: boolean;
  responseTime?: number;
}

// Enhanced API Service with health monitoring
export class EnhancedApiService {
  private static instance: EnhancedApiService;
  private baseURL: string;
  private defaultTimeout: number = 10000;
  private maxRetries: number = 3;

  private constructor() {
    this.baseURL = process.env.NEXT_PUBLIC_DJANGO_API_URL || 'http://localhost:8000/api';
  }

  public static getInstance(): EnhancedApiService {
    if (!EnhancedApiService.instance) {
      EnhancedApiService.instance = new EnhancedApiService();
    }
    return EnhancedApiService.instance;
  }

  // Main request method with health checks and fallbacks
  async request<T = any>(config: ApiRequestConfig): Promise<ApiResponse<T>> {
    const startTime = Date.now();
    
    try {
      // Check API health first for critical endpoints
      if (config.useFallback !== false) {
        const healthCheck = await HealthUtils.checkEndpoint(
          `${this.baseURL}${config.endpoint}`,
          config.timeout || this.defaultTimeout
        );

        // Use fallback if API is unhealthy
        if (apiHealthService.shouldUseFallback(healthCheck)) {
          console.warn(`API unhealthy for ${config.endpoint}, using fallback data`);
          const fallbackData = apiHealthService.getFallbackData(config.endpoint);
          
          return {
            success: true,
            data: fallbackData,
            message: 'Using cached data due to API unavailability',
            fromFallback: true,
            responseTime: Date.now() - startTime
          };
        }
      }

      // Attempt API request with retries
      const response = await this.makeRequestWithRetries(config);
      
      return {
        success: true,
        data: response.data,
        responseTime: Date.now() - startTime
      };

    } catch (error) {
      // Handle error with centralized error handling
      const processedError = ErrorUtils.handleNetworkError(error, `API Request: ${config.endpoint}`);
      
      // Use fallback data if available and enabled
      if (config.useFallback !== false) {
        console.warn(`API request failed for ${config.endpoint}, using fallback data`);
        const fallbackData = apiHealthService.getFallbackData(config.endpoint);
        
        return {
          success: true,
          data: fallbackData,
          message: 'Using cached data due to API error',
          error: processedError.userMessage,
          fromFallback: true,
          responseTime: Date.now() - startTime
        };
      }

      // Return error response
      return {
        success: false,
        data: null as T,
        error: processedError.userMessage,
        responseTime: Date.now() - startTime
      };
    }
  }

  // Make request with retry logic
  private async makeRequestWithRetries(config: ApiRequestConfig): Promise<AxiosResponse> {
    const retries = config.retries || this.maxRetries;
    let lastError: any;

    for (let attempt = 0; attempt <= retries; attempt++) {
      try {
        const axiosConfig = {
          url: `${this.baseURL}${config.endpoint}`,
          method: config.method,
          data: config.data,
          params: config.params,
          headers: {
            'Content-Type': 'application/json',
            ...this.getAuthHeaders(),
            ...config.headers
          },
          timeout: config.timeout || this.defaultTimeout
        };

        const response = await axios(axiosConfig);
        return response;

      } catch (error) {
        lastError = error;
        
        // Don't retry on certain errors
        if (this.shouldNotRetry(error)) {
          throw error;
        }

        // Wait before retry (exponential backoff)
        if (attempt < retries) {
          const delay = Math.pow(2, attempt) * 1000; // 1s, 2s, 4s, 8s
          await this.delay(delay);
          console.warn(`API request attempt ${attempt + 1} failed, retrying in ${delay}ms...`);
        }
      }
    }

    throw lastError;
  }

  // Check if error should not be retried
  private shouldNotRetry(error: any): boolean {
    if (axios.isAxiosError(error)) {
      const status = error.response?.status;
      // Don't retry on client errors (4xx) except for specific cases
      return status !== undefined && status >= 400 && status < 500 && status !== 408 && status !== 429;
    }
    return false;
  }

  // Get authentication headers
  private getAuthHeaders(): Record<string, string> {
    const headers: Record<string, string> = {};
    
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('jwt_token');
      if (token) {
        headers.Authorization = `Bearer ${token}`;
      }
    }
    
    return headers;
  }

  // Utility delay function
  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Convenience methods for common HTTP operations
  async get<T = any>(endpoint: string, params?: any, options?: Partial<ApiRequestConfig>): Promise<ApiResponse<T>> {
    return this.request<T>({
      endpoint,
      method: 'GET',
      params,
      ...options
    });
  }

  async post<T = any>(endpoint: string, data?: any, options?: Partial<ApiRequestConfig>): Promise<ApiResponse<T>> {
    return this.request<T>({
      endpoint,
      method: 'POST',
      data,
      ...options
    });
  }

  async put<T = any>(endpoint: string, data?: any, options?: Partial<ApiRequestConfig>): Promise<ApiResponse<T>> {
    return this.request<T>({
      endpoint,
      method: 'PUT',
      data,
      ...options
    });
  }

  async delete<T = any>(endpoint: string, options?: Partial<ApiRequestConfig>): Promise<ApiResponse<T>> {
    return this.request<T>({
      endpoint,
      method: 'DELETE',
      ...options
    });
  }

  // Health check method
  async checkHealth(): Promise<boolean> {
    try {
      const response = await this.get('/health/', {}, { useFallback: false, timeout: 5000 });
      return response.success;
    } catch {
      return false;
    }
  }

  // Get API status for display
  async getApiStatus(): Promise<{
    status: 'healthy' | 'degraded' | 'unhealthy';
    message: string;
    isHealthy: boolean;
  }> {
    return await HealthUtils.getHealthStatus();
  }
}

// Export singleton instance
export const enhancedApiService = EnhancedApiService.getInstance();

// Utility functions for common API patterns
export const ApiUtils = {
  // Check if API is available
  checkAvailability: async () => {
    return await enhancedApiService.checkHealth();
  },

  // Get API status
  getStatus: async () => {
    return await enhancedApiService.getApiStatus();
  },

  // Make a simple GET request with fallback
  get: async <T = any>(endpoint: string, params?: any) => {
    return await enhancedApiService.get<T>(endpoint, params);
  },

  // Make a simple POST request with fallback
  post: async <T = any>(endpoint: string, data?: any) => {
    return await enhancedApiService.post<T>(endpoint, data);
  },

  // Handle API response consistently
  handleResponse: <T = any>(response: ApiResponse<T>) => {
    if (response.fromFallback) {
      console.warn('Using fallback data:', response.message);
    }
    
    if (!response.success) {
      throw new Error(response.error || 'API request failed');
    }
    
    return response.data;
  }
};
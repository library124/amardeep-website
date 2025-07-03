// API Health Check Service following SOLID principles
// Single Responsibility: Handles API health monitoring and fallback strategies
// Open/Closed: Extensible for new health check types
// Interface Segregation: Separate interfaces for different health concerns
// Dependency Inversion: Depends on abstractions, not concrete implementations

export interface HealthCheckResult {
  isHealthy: boolean;
  status: 'healthy' | 'degraded' | 'unhealthy';
  responseTime: number;
  error?: string;
  timestamp: string;
}

export interface ApiEndpoint {
  name: string;
  url: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  timeout: number;
  critical: boolean;
}

export interface HealthChecker {
  checkHealth(endpoint: ApiEndpoint): Promise<HealthCheckResult>;
}

export interface FallbackStrategy {
  shouldUseFallback(healthResult: HealthCheckResult): boolean;
  getFallbackData(endpoint: string): any;
}

// Concrete implementation of health checker
export class HttpHealthChecker implements HealthChecker {
  async checkHealth(endpoint: ApiEndpoint): Promise<HealthCheckResult> {
    const startTime = Date.now();
    const timestamp = new Date().toISOString();

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), endpoint.timeout);

      const response = await fetch(endpoint.url, {
        method: endpoint.method,
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
        },
      });

      clearTimeout(timeoutId);
      const responseTime = Date.now() - startTime;

      if (response.ok) {
        return {
          isHealthy: true,
          status: 'healthy',
          responseTime,
          timestamp,
        };
      } else {
        return {
          isHealthy: false,
          status: 'degraded',
          responseTime,
          error: `HTTP ${response.status}: ${response.statusText}`,
          timestamp,
        };
      }
    } catch (error) {
      const responseTime = Date.now() - startTime;
      
      let errorMessage = 'Unknown error';
      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          errorMessage = `Request timeout after ${endpoint.timeout}ms`;
        } else {
          errorMessage = error.message;
        }
      }

      return {
        isHealthy: false,
        status: 'unhealthy',
        responseTime,
        error: errorMessage,
        timestamp,
      };
    }
  }
}

// Fallback strategy for when API is unavailable
export class MockDataFallbackStrategy implements FallbackStrategy {
  shouldUseFallback(healthResult: HealthCheckResult): boolean {
    return !healthResult.isHealthy || healthResult.status === 'unhealthy';
  }

  getFallbackData(endpoint: string): any {
    // Return mock data based on endpoint
    if (endpoint.includes('/courses/')) {
      return this.getMockCourses();
    } else if (endpoint.includes('/workshops/')) {
      return this.getMockWorkshops();
    } else if (endpoint.includes('/blog/')) {
      return this.getMockBlogPosts();
    } else if (endpoint.includes('/products/')) {
      return this.getMockProducts();
    } else if (endpoint.includes('/achievements/')) {
      return this.getMockAchievements();
    }
    
    return { message: 'API temporarily unavailable. Using cached data.' };
  }

  private getMockCourses() {
    return [
      {
        id: 1,
        title: "Advanced Intraday Trading Strategies",
        slug: "advanced-intraday-trading",
        description: "Master advanced intraday trading techniques with proven strategies for consistent profits.",
        price: 4999,
        price_display: "₹4,999",
        currency: "INR",
        is_featured: true,
        duration: "8 weeks",
        level: "Advanced",
        image: "/course-placeholder.jpg"
      }
    ];
  }

  private getMockWorkshops() {
    return [
      {
        id: 1,
        title: "Weekend Trading Bootcamp",
        slug: "weekend-trading-bootcamp",
        description: "Intensive weekend workshop covering essential trading concepts.",
        price: 2999,
        price_display: "₹2,999",
        currency: "INR",
        is_paid: true,
        start_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
        end_date: new Date(Date.now() + 9 * 24 * 60 * 60 * 1000).toISOString(),
        max_participants: 50,
        current_participants: 23
      }
    ];
  }

  private getMockBlogPosts() {
    return [
      {
        id: 1,
        title: "Market Analysis: Key Trends This Week",
        slug: "market-analysis-key-trends",
        excerpt: "Comprehensive analysis of current market trends and trading opportunities.",
        featured_image: "/blog-placeholder.jpg",
        author_name: "Amardeep Asode",
        category_name: "Market Analysis",
        publish_date: new Date().toISOString(),
        reading_time: 5,
        views_count: 1250
      }
    ];
  }

  private getMockProducts() {
    return [
      {
        id: 1,
        name: "Trading Signals Premium",
        description: "Daily trading signals with entry and exit points.",
        price: 1999,
        price_display: "₹1,999",
        currency: "INR"
      }
    ];
  }

  private getMockAchievements() {
    return [
      {
        id: 1,
        title: "5+ Years Trading Experience",
        description: "Successfully trading in Indian stock markets for over 5 years.",
        date: "2019-01-01",
        metrics: {
          "Years of Experience": 5,
          "Success Rate": "85%",
          "Clients Mentored": 200
        }
      }
    ];
  }
}

// Main API Health Service
export class ApiHealthService {
  private static instance: ApiHealthService;
  private healthChecker: HealthChecker;
  private fallbackStrategy: FallbackStrategy;
  private healthCache: Map<string, HealthCheckResult> = new Map();
  private cacheTimeout = 30000; // 30 seconds

  private constructor(
    healthChecker: HealthChecker = new HttpHealthChecker(),
    fallbackStrategy: FallbackStrategy = new MockDataFallbackStrategy()
  ) {
    this.healthChecker = healthChecker;
    this.fallbackStrategy = fallbackStrategy;
  }

  public static getInstance(): ApiHealthService {
    if (!ApiHealthService.instance) {
      ApiHealthService.instance = new ApiHealthService();
    }
    return ApiHealthService.instance;
  }

  // Define critical API endpoints
  private getCriticalEndpoints(): ApiEndpoint[] {
    const baseUrl = process.env.NEXT_PUBLIC_DJANGO_API_URL || 'http://localhost:8000/api';
    
    return [
      {
        name: 'Django API Health',
        url: `${baseUrl}/health/`,
        method: 'GET',
        timeout: 5000,
        critical: true
      },
      {
        name: 'Courses API',
        url: `${baseUrl}/courses/`,
        method: 'GET',
        timeout: 5000,
        critical: false
      },
      {
        name: 'Workshops API',
        url: `${baseUrl}/workshops/`,
        method: 'GET',
        timeout: 5000,
        critical: false
      },
      {
        name: 'Payment API',
        url: `${baseUrl}/create-order/`,
        method: 'POST',
        timeout: 10000,
        critical: true
      }
    ];
  }

  // Check health of a specific endpoint
  async checkEndpointHealth(endpoint: ApiEndpoint): Promise<HealthCheckResult> {
    const cacheKey = `${endpoint.name}_${endpoint.url}`;
    const cached = this.healthCache.get(cacheKey);
    
    // Return cached result if still valid
    if (cached && Date.now() - new Date(cached.timestamp).getTime() < this.cacheTimeout) {
      return cached;
    }

    const result = await this.healthChecker.checkHealth(endpoint);
    this.healthCache.set(cacheKey, result);
    
    return result;
  }

  // Check health of all critical endpoints
  async checkOverallHealth(): Promise<{
    isHealthy: boolean;
    status: 'healthy' | 'degraded' | 'unhealthy';
    endpoints: Record<string, HealthCheckResult>;
    summary: string;
  }> {
    const endpoints = this.getCriticalEndpoints();
    const results: Record<string, HealthCheckResult> = {};
    
    // Check all endpoints in parallel
    const healthChecks = endpoints.map(async (endpoint) => {
      const result = await this.checkEndpointHealth(endpoint);
      results[endpoint.name] = result;
      return { endpoint, result };
    });

    await Promise.all(healthChecks);

    // Determine overall health
    const criticalEndpoints = endpoints.filter(e => e.critical);
    const criticalResults = criticalEndpoints.map(e => results[e.name]);
    
    const allCriticalHealthy = criticalResults.every(r => r.isHealthy);
    const anyCriticalUnhealthy = criticalResults.some(r => r.status === 'unhealthy');
    
    let overallStatus: 'healthy' | 'degraded' | 'unhealthy';
    let summary: string;
    
    if (allCriticalHealthy) {
      overallStatus = 'healthy';
      summary = 'All critical services are operational';
    } else if (anyCriticalUnhealthy) {
      overallStatus = 'unhealthy';
      summary = 'Critical services are unavailable. Using fallback data.';
    } else {
      overallStatus = 'degraded';
      summary = 'Some services are experiencing issues';
    }

    return {
      isHealthy: allCriticalHealthy,
      status: overallStatus,
      endpoints: results,
      summary
    };
  }

  // Get fallback data for an endpoint
  getFallbackData(endpoint: string): any {
    return this.fallbackStrategy.getFallbackData(endpoint);
  }

  // Check if fallback should be used
  shouldUseFallback(healthResult: HealthCheckResult): boolean {
    return this.fallbackStrategy.shouldUseFallback(healthResult);
  }

  // Clear health cache
  clearCache(): void {
    this.healthCache.clear();
  }
}

// Export singleton instance
export const apiHealthService = ApiHealthService.getInstance();

// Utility functions for common health check patterns
export const HealthUtils = {
  // Check if API is available
  checkApiAvailability: async () => {
    const health = await apiHealthService.checkOverallHealth();
    return health.isHealthy;
  },

  // Get fallback data for endpoint
  getFallbackData: (endpoint: string) => {
    return apiHealthService.getFallbackData(endpoint);
  },

  // Check specific endpoint
  checkEndpoint: async (url: string, timeout: number = 5000) => {
    const endpoint: ApiEndpoint = {
      name: 'Custom Check',
      url,
      method: 'GET',
      timeout,
      critical: false
    };
    return await apiHealthService.checkEndpointHealth(endpoint);
  },

  // Get health status for display
  getHealthStatus: async () => {
    const health = await apiHealthService.checkOverallHealth();
    return {
      status: health.status,
      message: health.summary,
      isHealthy: health.isHealthy
    };
  }
};
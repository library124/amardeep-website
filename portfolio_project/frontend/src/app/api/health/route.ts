import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // Basic health check for frontend
    const healthData = {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      version: '1.0.0',
      environment: process.env.NODE_ENV || 'development',
      api_url: process.env.NEXT_PUBLIC_DJANGO_API_URL || 'not configured',
      razorpay_configured: !!process.env.NEXT_PUBLIC_RAZORPAY_KEY_ID,
    };

    return NextResponse.json(healthData, { status: 200 });
  } catch (error) {
    return NextResponse.json(
      {
        status: 'unhealthy',
        timestamp: new Date().toISOString(),
        error: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 503 }
    );
  }
}
# Deployment Guide

This guide covers deploying the Amardeep Portfolio application with frontend on Vercel and backend on Render.com.

## Architecture Overview

- **Frontend**: Next.js 15 application deployed on Vercel
- **Backend**: Django REST API deployed on Render.com
- **Database**: PostgreSQL on Render.com
- **Payment**: Razorpay integration
- **Email**: Brevo (Sendinblue) integration

## Prerequisites

1. GitHub repository with the code
2. Vercel account
3. Render.com account
4. Razorpay account (for payments)
5. Brevo account (for emails)

## Backend Deployment (Render.com)

### 1. Database Setup

1. Go to Render.com dashboard
2. Create a new PostgreSQL database:
   - Name: `portfolio-db`
   - Plan: Free (or paid as needed)
   - Note down the connection details

### 2. Web Service Setup

1. Create a new Web Service on Render.com
2. Connect your GitHub repository
3. Configure the service:
   - **Name**: `amardeep-portfolio-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT`
   - **Plan**: Free (or paid as needed)

### 3. Environment Variables

Set the following environment variables in Render.com:

```bash
# Django Configuration
DJANGO_SETTINGS_MODULE=backend.settings
DEBUG=False
SECRET_KEY=<generate-a-secure-secret-key>
ALLOWED_HOSTS=.onrender.com,localhost,127.0.0.1

# Database (automatically set by Render when you connect the database)
DATABASE_URL=<postgresql-connection-string>

# Razorpay Configuration
RAZORPAY_KEY_ID=<your-razorpay-key-id>
RAZORPAY_KEY_SECRET=<your-razorpay-key-secret>
RAZORPAY_WEBHOOK_SECRET=<your-razorpay-webhook-secret>

# Email Configuration (Brevo)
EMAIL_HOST_USER=<your-brevo-email>
EMAIL_HOST_PASSWORD=<your-brevo-smtp-password>
BREVO_API_KEY=<your-brevo-api-key>

# Frontend URL
FRONTEND_URL=https://amardeep-portfolio-frontend.vercel.app

# Production Flag
RENDER=true
```

### 4. Deploy Backend

1. Connect the PostgreSQL database to your web service
2. Deploy the service
3. Monitor the build logs for any issues
4. Test the health endpoint: `https://your-backend-url.onrender.com/api/health/`

## Frontend Deployment (Vercel)

### 1. Project Setup

1. Go to Vercel dashboard
2. Import your GitHub repository
3. Select the `frontend` folder as the root directory
4. Framework preset: Next.js

### 2. Environment Variables

Set the following environment variables in Vercel:

```bash
# API Configuration
NEXT_PUBLIC_DJANGO_API_URL=https://your-backend-url.onrender.com/api
NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com

# Razorpay Configuration
NEXT_PUBLIC_RAZORPAY_KEY_ID=<your-razorpay-key-id>
```

### 3. Build Configuration

Vercel will automatically detect the Next.js configuration. The build should work with the existing `next.config.ts`.

### 4. Deploy Frontend

1. Deploy the project
2. Test the deployment
3. Verify API connectivity with the backend

## Post-Deployment Configuration

### 1. Update CORS Settings

Update the backend CORS settings to include your Vercel domain:

```python
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-domain.vercel.app",
    "https://amardeepasode.com",  # if you have a custom domain
]
```

### 2. Configure Custom Domain (Optional)

#### For Frontend (Vercel):
1. Go to your project settings in Vercel
2. Add your custom domain
3. Configure DNS records as instructed

#### For Backend (Render):
1. Go to your service settings in Render
2. Add custom domain
3. Update ALLOWED_HOSTS in Django settings

### 3. SSL/HTTPS Configuration

Both Vercel and Render provide automatic SSL certificates. Ensure:
- All API calls use HTTPS
- Update any hardcoded HTTP URLs to HTTPS

## Environment-Specific Configuration

### Development
- Use local Django server and Next.js dev server
- SQLite database for local development
- Mock payment gateway for testing

### Production
- Django on Render.com with PostgreSQL
- Next.js on Vercel with optimized builds
- Real Razorpay integration
- Production email service

## Monitoring and Maintenance

### Health Checks

The application includes health check endpoints:
- Backend: `/api/health/`
- Payment status: `/api/payment/status/`
- API status: `/api/status/`

### Logging

- Backend logs are available in Render.com dashboard
- Frontend logs are available in Vercel dashboard
- Monitor for errors and performance issues

### Database Backups

- Render.com provides automatic backups for paid plans
- For free plans, consider manual backup strategies

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure frontend domain is in CORS_ALLOWED_ORIGINS
2. **Database Connection**: Check DATABASE_URL and connection settings
3. **Static Files**: Ensure collectstatic runs successfully
4. **Environment Variables**: Verify all required variables are set
5. **Build Failures**: Check build logs for missing dependencies

### Debug Steps

1. Check health endpoints
2. Review deployment logs
3. Verify environment variables
4. Test API endpoints individually
5. Check database connectivity

## Security Considerations

1. **Environment Variables**: Never commit sensitive data to Git
2. **HTTPS**: Ensure all communications use HTTPS
3. **CORS**: Restrict CORS to specific domains
4. **Database**: Use strong passwords and connection encryption
5. **API Keys**: Rotate keys regularly

## Performance Optimization

1. **Frontend**: Use Next.js optimization features
2. **Backend**: Enable Django caching
3. **Database**: Optimize queries and add indexes
4. **CDN**: Use Vercel's built-in CDN
5. **Monitoring**: Set up performance monitoring

## Backup and Recovery

1. **Database**: Regular backups of PostgreSQL
2. **Code**: Git repository serves as code backup
3. **Environment Variables**: Document all configurations
4. **Media Files**: Backup uploaded files if any

## Support and Maintenance

- Monitor application health regularly
- Update dependencies for security patches
- Review and rotate API keys
- Monitor usage and scaling needs
- Keep documentation updated

---

For any issues during deployment, refer to the respective platform documentation:
- [Vercel Documentation](https://vercel.com/docs)
- [Render.com Documentation](https://render.com/docs)
- [Django Deployment Guide](https://docs.djangoproject.com/en/stable/howto/deployment/)
- [Next.js Deployment Guide](https://nextjs.org/docs/deployment)
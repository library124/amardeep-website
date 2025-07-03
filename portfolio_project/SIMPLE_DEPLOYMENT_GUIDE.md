# Simple Deployment Guide

This guide provides step-by-step instructions to deploy your portfolio project to Render.com (backend) and Vercel (frontend).

## Prerequisites

1. GitHub account with your code pushed
2. Render.com account (free)
3. Vercel account (free)
4. Razorpay account for payments
5. Brevo account for emails

## Backend Deployment (Render.com)

### Step 1: Prepare Your Repository

1. Ensure your code is pushed to GitHub
2. Make sure the `render.yaml` file exists in the backend folder
3. Verify `build.sh` has execute permissions

### Step 2: Create Database on Render

1. Go to [Render.com Dashboard](https://dashboard.render.com/)
2. Click "New" → "PostgreSQL"
3. Configure:
   - Name: `portfolio-db`
   - Database: `portfolio_db`
   - User: `portfolio_user`
   - Plan: Free
4. Click "Create Database"
5. Note down the connection details

### Step 3: Create Web Service

1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - Name: `amardeep-portfolio-backend`
   - Environment: `Python 3`
   - Root Directory: `portfolio_project/backend`
   - Build Command: `./build.sh`
   - Start Command: `gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT`
   - Plan: Free

### Step 4: Set Environment Variables

In the Render dashboard, add these environment variables:

```
DJANGO_SETTINGS_MODULE=backend.settings_production
DEBUG=False
SECRET_KEY=your-generated-secret-key-here
ALLOWED_HOSTS=.onrender.com,localhost,127.0.0.1
DATABASE_URL=postgresql://user:password@host:port/database
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
RAZORPAY_WEBHOOK_SECRET=your_razorpay_webhook_secret
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
BREVO_API_KEY=your_brevo_api_key
FRONTEND_URL=https://amardeep-portfolio-frontend.vercel.app
RENDER=true
```

### Step 5: Connect Database and Deploy

1. In the web service settings, connect the PostgreSQL database
2. Click "Deploy"
3. Monitor the build logs
4. Test the deployment: `https://your-service.onrender.com/api/health/`

## Frontend Deployment (Vercel)

### Step 1: Import Project

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import from GitHub
4. Select your repository
5. Configure:
   - Framework Preset: Next.js
   - Root Directory: `portfolio_project/frontend`

### Step 2: Set Environment Variables

In Vercel project settings, add:

```
NEXT_PUBLIC_DJANGO_API_URL=https://your-backend.onrender.com/api
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
NEXT_PUBLIC_RAZORPAY_KEY_ID=your_razorpay_key_id
NODE_ENV=production
```

### Step 3: Deploy

1. Click "Deploy"
2. Wait for build to complete
3. Test the deployment

## Post-Deployment Configuration

### Update CORS Settings

1. Once frontend is deployed, note the Vercel URL
2. Update backend environment variable:
   ```
   FRONTEND_URL=https://your-frontend.vercel.app
   ```
3. Redeploy backend

### Test Integration

1. Visit your frontend URL
2. Test user registration/login
3. Test payment integration
4. Test contact form

## Environment Variables Reference

### Backend (Render.com)

| Variable | Description | Example |
|----------|-------------|---------|
| `DJANGO_SETTINGS_MODULE` | Django settings module | `backend.settings_production` |
| `DEBUG` | Debug mode | `False` |
| `SECRET_KEY` | Django secret key | Generate 50-char random string |
| `ALLOWED_HOSTS` | Allowed hosts | `.onrender.com,localhost,127.0.0.1` |
| `DATABASE_URL` | Database connection | Auto-set by Render |
| `RAZORPAY_KEY_ID` | Razorpay public key | From Razorpay dashboard |
| `RAZORPAY_KEY_SECRET` | Razorpay secret key | From Razorpay dashboard |
| `EMAIL_HOST_USER` | Email username | Your email |
| `EMAIL_HOST_PASSWORD` | Email password | Your email password |
| `BREVO_API_KEY` | Brevo API key | From Brevo dashboard |
| `FRONTEND_URL` | Frontend URL | Your Vercel URL |

### Frontend (Vercel)

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_DJANGO_API_URL` | Backend API URL | `https://your-backend.onrender.com/api` |
| `NEXT_PUBLIC_API_URL` | Backend base URL | `https://your-backend.onrender.com` |
| `NEXT_PUBLIC_RAZORPAY_KEY_ID` | Razorpay public key | Same as backend |

## Troubleshooting

### Common Issues

1. **Build Fails on Render**
   - Check build logs
   - Ensure all dependencies are in requirements.txt
   - Verify build.sh has correct permissions

2. **Database Connection Error**
   - Verify DATABASE_URL is set correctly
   - Check if database is connected to web service

3. **CORS Errors**
   - Ensure FRONTEND_URL is set correctly
   - Check CORS_ALLOWED_ORIGINS in Django settings

4. **Frontend Can't Connect to Backend**
   - Verify API URLs in frontend environment variables
   - Check if backend is running and accessible

### Health Checks

- Backend health: `https://your-backend.onrender.com/api/health/`
- Simple health: `https://your-backend.onrender.com/api/health/simple/`

## Security Checklist

- [ ] All environment variables are set
- [ ] Secret keys are generated and secure
- [ ] DEBUG is set to False in production
- [ ] CORS is configured properly
- [ ] Database credentials are secure
- [ ] API keys are not exposed in frontend code

## Support

If you encounter issues:

1. Check the deployment logs in Render/Vercel dashboards
2. Verify all environment variables are set correctly
3. Test health endpoints
4. Check CORS configuration
5. Review Django and Next.js documentation

---

This deployment guide follows SOLID principles and provides a robust foundation for your portfolio application.
# Django Backend Deployment Guide for Render.com

## 🚀 Complete Step-by-Step Deployment Guide

### Prerequisites
- ✅ Django backend ready for deployment
- ✅ GitHub account with your code pushed to a repository
- ✅ Render.com account (free tier available)

---

## 📋 Phase 1: Prepare Your Django Project

### 1. **Verify Required Files** ✅
Your project now includes these essential files:
- `requirements.txt` - Updated with production dependencies
- `build.sh` - Build script for Render
- `render.yaml` - Infrastructure as Code configuration
- `backend/settings_production.py` - Production settings
- `.env.production` - Environment variables template

### 2. **Update Your Main Settings** 
Add this to your main `settings.py` to conditionally load production settings:

```python
# At the bottom of settings.py
if 'RENDER' in os.environ:
    from .settings_production import *
```

### 3. **Test Production Settings Locally** (Optional)
```bash
# Set environment variable
export DJANGO_SETTINGS_MODULE=backend.settings_production
export DATABASE_URL=sqlite:///./db.sqlite3  # For testing only

# Test the settings
python manage.py check --deploy
```

---

## 🗄️ Phase 2: Set Up PostgreSQL Database on Render

### 1. **Create PostgreSQL Database**
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"PostgreSQL"**
3. Configure your database:
   - **Name**: `portfolio-db`
   - **Database**: `portfolio`
   - **User**: `portfolio`
   - **Region**: Choose closest to your users
   - **Plan**: Free (or paid for production)
4. Click **"Create Database"**

### 2. **Save Database Credentials**
After creation, copy these values:
- **Internal Database URL** (for connecting services within Render)
- **External Database URL** (for external connections)
- **Database Name, User, Password** (individual credentials)

---

## 🌐 Phase 3: Deploy Web Service

### Option A: Using render.yaml (Recommended)

1. **Push to GitHub**
```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

2. **Deploy via Blueprint**
   - Go to [Render Blueprints](https://dashboard.render.com/blueprints)
   - Click **"New Blueprint Instance"**
   - Connect your GitHub repository
   - Name your blueprint: `amardeep-portfolio`
   - Click **"Apply"**

### Option B: Manual Setup

1. **Create Web Service**
   - Go to Render Dashboard
   - Click **"New +"** → **"Web Service"**
   - Connect your GitHub repository
   - Select the backend directory if it's in a subdirectory

2. **Configure Service Settings**
   - **Name**: `amardeep-portfolio-backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `python -m gunicorn backend.wsgi:application`
   - **Plan**: Free (or paid for production)

3. **Set Environment Variables**
   Add these environment variables in Render:

   | Key | Value | Notes |
   |-----|-------|-------|
   | `DATABASE_URL` | *From your PostgreSQL service* | Internal URL |
   | `SECRET_KEY` | *Generate secure key* | Use Render's generator |
   | `DEBUG` | `False` | Production setting |
   | `DJANGO_SETTINGS_MODULE` | `backend.settings_production` | Load production settings |
   | `FRONTEND_URL` | `https://your-frontend-domain.com` | Your frontend URL |
   | `EMAIL_HOST_USER` | `your-email@domain.com` | Brevo email |
   | `EMAIL_HOST_PASSWORD` | `your-brevo-password` | Brevo SMTP password |
   | `BREVO_API_KEY` | `your-brevo-api-key` | Brevo API key |
   | `RAZORPAY_KEY_ID` | `your-razorpay-key` | Payment gateway |
   | `RAZORPAY_KEY_SECRET` | `your-razorpay-secret` | Payment gateway |
   | `WEB_CONCURRENCY` | `4` | Server workers |

---

## 🔧 Phase 4: Post-Deployment Setup

### 1. **Run Database Migrations**
After successful deployment, use Render Shell:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 2. **Create Superuser**
```bash
python manage.py createsuperuser
```

### 3. **Test Your Deployment**
- Visit your Render service URL
- Test API endpoints
- Check admin panel: `https://your-service.onrender.com/admin/`

---

## 🔒 Phase 5: Security & Production Checklist

### 1. **Environment Variables Security**
- ✅ Never commit `.env` files to Git
- ✅ Use Render's environment variable system
- ✅ Generate strong SECRET_KEY
- ✅ Set DEBUG=False in production

### 2. **Database Security**
- ✅ Use Internal Database URL for better performance
- ✅ Enable SSL connections
- ✅ Regular backups (Render handles this)

### 3. **CORS Configuration**
- ✅ Set specific frontend domains in CORS_ALLOWED_ORIGINS
- ✅ Avoid using wildcards (*) in production

---

## 🚨 Troubleshooting Common Issues

### Build Failures
```bash
# Check build logs in Render dashboard
# Common issues:
# 1. Missing dependencies in requirements.txt
# 2. Python version compatibility
# 3. Build script permissions
```

### Database Connection Issues
```bash
# Verify environment variables
# Check DATABASE_URL format
# Ensure PostgreSQL service is running
```

### Static Files Not Loading
```bash
# Run collectstatic manually
python manage.py collectstatic --noinput

# Check STATIC_ROOT and STATIC_URL settings
# Verify WhiteNoise configuration
```

### CORS Errors
```bash
# Update CORS_ALLOWED_ORIGINS
# Check frontend URL configuration
# Verify CORS middleware order
```

---

## 📊 Monitoring & Maintenance

### 1. **Monitor Your Service**
- Use Render's built-in monitoring
- Check logs regularly
- Set up alerts for downtime

### 2. **Database Maintenance**
- Monitor database usage
- Plan for scaling when needed
- Regular health checks

### 3. **Updates & Deployments**
- Render auto-deploys on Git push
- Use staging environment for testing
- Monitor deployment logs

---

## 🎯 Production Optimization Tips

### 1. **Performance**
- Use Redis for caching (add as separate service)
- Optimize database queries
- Enable gzip compression
- Use CDN for static files

### 2. **Scaling**
- Monitor resource usage
- Upgrade to paid plans when needed
- Consider horizontal scaling

### 3. **Security**
- Regular security updates
- Monitor for vulnerabilities
- Use HTTPS everywhere
- Implement rate limiting

---

## 📞 Support & Resources

- **Render Documentation**: https://render.com/docs
- **Django Deployment Checklist**: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
- **Render Community**: https://community.render.com

---

## ✅ Deployment Checklist

- [ ] All required files created and configured
- [ ] Code pushed to GitHub
- [ ] PostgreSQL database created on Render
- [ ] Web service deployed successfully
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Superuser created
- [ ] API endpoints tested
- [ ] Admin panel accessible
- [ ] CORS configured for frontend
- [ ] SSL certificate active
- [ ] Monitoring set up

**🎉 Your Django backend is now live on Render!**

Your API will be available at: `https://your-service-name.onrender.com`
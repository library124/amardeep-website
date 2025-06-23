# Amardeep Asode - Trading Portfolio Website

A comprehensive portfolio website for Amardeep Asode, featuring trading insights, workshops, blog posts, and newsletter functionality.

## 🚀 Features

### Core Features
- **Modern Portfolio Design**: Clean, professional design showcasing trading expertise
- **Workshop/Masterclass System**: Complete workshop management with notifications and WhatsApp integration
- **Blog System**: Full-featured blog with categories, tags, and rich content management
- **Newsletter System**: Email subscription with confirmation and management
- **Achievement Showcase**: Display trading achievements and performance metrics
- **Contact System**: Contact form with professional inquiry handling

### Workshop System
- **Admin Management**: Create and manage workshops through Django admin
- **Homepage Notifications**: Automatic display of upcoming workshops
- **WhatsApp Integration**: Direct application via WhatsApp with pre-filled messages
- **Participant Tracking**: Real-time participant count and capacity management
- **Status Management**: Upcoming, ongoing, completed, and cancelled statuses
- **Application System**: Track and manage workshop applications

### Blog System
- **Rich Content Management**: Full WYSIWYG editor support
- **SEO Optimization**: Meta titles, descriptions, and URL optimization
- **Category & Tag System**: Organize content with categories and tags
- **Featured Posts**: Highlight important blog posts
- **Reading Time**: Automatic reading time calculation
- **Related Posts**: Smart related content suggestions

### Newsletter System
- **Email Subscription**: Double opt-in subscription system
- **Confirmation System**: Email confirmation with unique tokens
- **Admin Management**: Send newsletters to confirmed subscribers
- **Unsubscribe System**: Easy unsubscribe functionality
- **Subscriber Management**: Track and manage subscriber base

## 🛠 Tech Stack

### Backend
- **Django 5.2.3**: Python web framework
- **Django REST Framework**: API development
- **SQLite**: Database (easily switchable to PostgreSQL)
- **Django Admin**: Content management interface

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Animation library
- **Responsive Design**: Mobile-first approach

### Additional Tools
- **Email System**: SMTP email configuration
- **WhatsApp Integration**: Direct messaging for workshop applications
- **SEO Optimization**: Meta tags and structured data
- **Performance Optimization**: Image optimization and lazy loading

## 📁 Project Structure

```
PORTFOLIO/
├── portfolio_project/
│   ├── backend/                 # Django backend
│   │   ├── backend/            # Django settings
│   │   ├── manage.py           # Django management
│   │   └── requirements.txt    # Python dependencies
│   └── frontend/               # Next.js frontend
│       ├── src/
│       │   ├── app/           # Next.js app router pages
│       │   ├── components/    # React components
│       │   ├── types/         # TypeScript interfaces
│       │   ├── utils/         # Utility functions
│       │   └── hooks/         # Custom React hooks
│       ├── public/            # Static assets
│       ├── package.json       # Node.js dependencies
│       └── tailwind.config.js # Tailwind configuration
├── portfolio_app/             # Django app
│   ├── models.py             # Database models
│   ├── views.py              # API views
│   ├── admin.py              # Admin configuration
│   ├── serializers.py        # API serializers
│   └── urls.py               # URL routing
└── Documentation/            # Project documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup
1. Navigate to backend directory:
   ```bash
   cd portfolio_project/backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Start development server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup
1. Navigate to frontend directory:
   ```bash
   cd portfolio_project/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start development server:
   ```bash
   npm run dev
   ```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/

## 📚 Documentation

### Detailed Guides
- [Workshop System Documentation](WORKSHOP_NOTIFICATIONS_IMPLEMENTATION.md)
- [Blog System Documentation](BLOG_SYSTEM_DOCUMENTATION.md)
- [Newsletter System Documentation](NEWSLETTER_SYSTEM_DOCUMENTATION.md)
- [Email Setup Guide](EMAIL_SETUP_GUIDE.md)
- [Blog Admin Guide](BLOG_ADMIN_GUIDE.md)

### API Endpoints

#### Workshops
- `GET /api/workshops/` - List all workshops
- `GET /api/workshops/upcoming/` - Get upcoming workshops
- `GET /api/workshops/featured/` - Get featured workshops
- `GET /api/workshops/<slug>/` - Get workshop details

#### Blog
- `GET /api/blog/` - List blog posts
- `GET /api/blog/post/<slug>/` - Get blog post details
- `GET /api/blog/categories/` - List categories
- `GET /api/blog/tags/` - List tags
- `GET /api/blog/featured/` - Get featured posts

#### Newsletter
- `POST /api/newsletter/subscribe/` - Subscribe to newsletter
- `GET /api/newsletter/confirm/<token>/` - Confirm subscription
- `GET /api/newsletter/unsubscribe/<token>/` - Unsubscribe

#### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login

## 🎯 Key Features Explained

### Workshop Notifications
When an admin creates a workshop in Django admin:
1. Workshop automatically appears on homepage if upcoming and active
2. Users see workshop cards with details (date, time, price, spots remaining)
3. Users can apply via WhatsApp with pre-filled message
4. Admin can manage applications through admin interface

### Blog System
- Rich content management with categories and tags
- SEO-optimized with meta titles and descriptions
- Featured posts system for highlighting important content
- Related posts suggestions based on categories and tags

### Newsletter System
- Double opt-in subscription process
- Email confirmation with unique tokens
- Admin can send newsletters to confirmed subscribers
- Easy unsubscribe functionality

## 🔧 Configuration

### Environment Variables
Create `.env` files in both backend and frontend directories:

#### Backend (.env)
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
FRONTEND_URL=http://localhost:3000
```

#### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### WhatsApp Integration
Update the WhatsApp number in `src/components/WorkshopNotifications.tsx`:
```javascript
const whatsappNumber = '919876543210'; // Replace with actual number
```

## 🚀 Deployment

### Backend Deployment
1. Set up production database (PostgreSQL recommended)
2. Configure email settings for production
3. Set DEBUG=False in production
4. Configure static files serving
5. Set up CORS for frontend domain

### Frontend Deployment
1. Build the application: `npm run build`
2. Deploy to Vercel, Netlify, or similar platform
3. Update API URLs for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Commit your changes: `git commit -m 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Amardeep Asode**
- Professional Stock & Intraday Trader
- 5+ years of trading experience
- Specializes in technical analysis and risk management

## 📞 Contact

For any queries or support:
- Email: amardipasode@gmail.com
- WhatsApp: +91 9876543210 (Replace with actual number)

---

**Note**: This is a professional portfolio website showcasing trading expertise and providing educational content. All trading involves risk, and past performance does not guarantee future results.
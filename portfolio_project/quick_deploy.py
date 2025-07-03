#!/usr/bin/env python3
"""
Quick Deploy Script for Amardeep Portfolio Project
Provides interactive deployment assistance
Following SOLID principles for user-friendly deployment

Author: Amardeep Asode
"""

import os
import sys
import webbrowser
from pathlib import Path

def print_banner():
    """Print deployment banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                 AMARDEEP PORTFOLIO DEPLOYMENT                ║
║                     Quick Deploy Assistant                   ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def print_menu():
    """Print main menu"""
    menu = """
Choose an option:

1. 📋 Check Deployment Readiness
2. 🚀 Open Deployment Guide
3. 🔧 Open Render.com Dashboard
4. ⚡ Open Vercel Dashboard
5. 📊 Monitor Deployment Health
6. 📖 View Documentation
7. ❌ Exit

"""
    print(menu)

def check_readiness():
    """Check deployment readiness"""
    print("\n🔍 Checking deployment readiness...")
    try:
        os.system("python deployment_checklist.py")
    except Exception as e:
        print(f"❌ Error running readiness check: {str(e)}")

def open_deployment_guide():
    """Open deployment guide"""
    guide_path = Path("SIMPLE_DEPLOYMENT_GUIDE.md")
    if guide_path.exists():
        print("\n📖 Opening deployment guide...")
        if sys.platform.startswith('win'):
            os.startfile(guide_path)
        elif sys.platform.startswith('darwin'):
            os.system(f"open {guide_path}")
        else:
            os.system(f"xdg-open {guide_path}")
    else:
        print("❌ Deployment guide not found!")

def open_render_dashboard():
    """Open Render.com dashboard"""
    print("\n🔧 Opening Render.com dashboard...")
    webbrowser.open("https://dashboard.render.com/")
    print("📝 Remember to:")
    print("   1. Create PostgreSQL database first")
    print("   2. Then create web service")
    print("   3. Set environment variables from .env.production")

def open_vercel_dashboard():
    """Open Vercel dashboard"""
    print("\n⚡ Opening Vercel dashboard...")
    webbrowser.open("https://vercel.com/dashboard")
    print("📝 Remember to:")
    print("   1. Import project from GitHub")
    print("   2. Set root directory to 'portfolio_project/frontend'")
    print("   3. Set environment variables from .env.production")

def monitor_health():
    """Monitor deployment health"""
    print("\n📊 Monitoring deployment health...")
    try:
        os.system("python monitor_deployment.py --mode check")
    except Exception as e:
        print(f"❌ Error running health monitor: {str(e)}")

def view_documentation():
    """View documentation menu"""
    print("\n📖 Available Documentation:")
    print("1. SIMPLE_DEPLOYMENT_GUIDE.md - Step-by-step deployment")
    print("2. DEPLOYMENT_SUMMARY.md - Complete deployment overview")
    print("3. deployment_readiness_report.md - Latest readiness report")
    
    choice = input("\nEnter document number to open (1-3): ").strip()
    
    docs = {
        "1": "SIMPLE_DEPLOYMENT_GUIDE.md",
        "2": "DEPLOYMENT_SUMMARY.md", 
        "3": "deployment_readiness_report.md"
    }
    
    if choice in docs:
        doc_path = Path(docs[choice])
        if doc_path.exists():
            if sys.platform.startswith('win'):
                os.startfile(doc_path)
            elif sys.platform.startswith('darwin'):
                os.system(f"open {doc_path}")
            else:
                os.system(f"xdg-open {doc_path}")
        else:
            print(f"❌ Document not found: {docs[choice]}")
    else:
        print("❌ Invalid choice!")

def show_environment_info():
    """Show environment variable information"""
    print("\n🔧 Environment Variables Setup:")
    print("\nBackend (.env.production):")
    print("   DJANGO_SETTINGS_MODULE=backend.settings_production")
    print("   DEBUG=False")
    print("   SECRET_KEY=<generate-secure-key>")
    print("   DATABASE_URL=<auto-set-by-render>")
    print("   RAZORPAY_KEY_ID=<your-key>")
    print("   RAZORPAY_KEY_SECRET=<your-secret>")
    print("   EMAIL_HOST_USER=<your-email>")
    print("   EMAIL_HOST_PASSWORD=<your-password>")
    print("   BREVO_API_KEY=<your-api-key>")
    print("   FRONTEND_URL=https://your-frontend.vercel.app")
    
    print("\nFrontend (.env.production):")
    print("   NEXT_PUBLIC_DJANGO_API_URL=https://your-backend.onrender.com/api")
    print("   NEXT_PUBLIC_API_URL=https://your-backend.onrender.com")
    print("   NEXT_PUBLIC_RAZORPAY_KEY_ID=<your-public-key>")

def main():
    """Main function"""
    print_banner()
    
    # Check if we're in the right directory
    if not Path("SIMPLE_DEPLOYMENT_GUIDE.md").exists():
        print("❌ Please run this script from the portfolio_project directory!")
        sys.exit(1)
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            check_readiness()
        elif choice == "2":
            open_deployment_guide()
        elif choice == "3":
            open_render_dashboard()
        elif choice == "4":
            open_vercel_dashboard()
        elif choice == "5":
            monitor_health()
        elif choice == "6":
            view_documentation()
        elif choice == "7":
            print("\n👋 Happy deploying! Good luck with your portfolio!")
            break
        else:
            print("❌ Invalid choice! Please enter 1-7.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Deployment assistant closed. Good luck!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
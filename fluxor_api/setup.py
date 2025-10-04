#!/usr/bin/env python3
"""
Setup script for Fluxor API - Bitcoin Trading System
"""

import os
import sys
import subprocess
import secrets
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def create_env_file():
    """Create .env file from template"""
    if os.path.exists('.env'):
        print("⚠️  .env file already exists, skipping...")
        return True
    
    print("📝 Creating .env file...")
    
    # Generate a secure secret key
    secret_key = ''.join(secrets.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50))
    
    env_content = f"""# Django Settings
SECRET_KEY={secret_key}
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=fluxor_api
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Bitcoin Network (testnet for development, mainnet for production)
BITCOIN_NETWORK=testnet
COMPANY_WALLET_LABEL=company_wallet

# Email (optional)
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created successfully")
    print("⚠️  Please update the database password and email settings in .env file")
    return True

def check_prerequisites():
    """Check if required software is installed"""
    print("🔍 Checking prerequisites...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    
    # Check if PostgreSQL is installed
    if not run_command("which psql", "Checking PostgreSQL"):
        print("❌ PostgreSQL is not installed or not in PATH")
        return False
    
    # Check if Redis is installed
    if not run_command("which redis-server", "Checking Redis"):
        print("❌ Redis is not installed or not in PATH")
        return False
    
    print("✅ All prerequisites are satisfied")
    return True

def setup_database():
    """Setup PostgreSQL database"""
    print("🗄️  Setting up database...")
    
    # Create database
    if not run_command("createdb fluxor_api", "Creating PostgreSQL database"):
        print("⚠️  Database creation failed. You may need to:")
        print("   1. Install PostgreSQL")
        print("   2. Start PostgreSQL service")
        print("   3. Create database manually: createdb fluxor_api")
        return False
    
    return True

def install_dependencies():
    """Install Python dependencies"""
    return run_command("pip install -r requirements.txt", "Installing Python dependencies")

def run_migrations():
    """Run Django migrations"""
    return run_command("python manage.py makemigrations", "Creating migrations") and \
           run_command("python manage.py migrate", "Running migrations")

def create_superuser():
    """Create Django superuser"""
    print("👤 Creating superuser...")
    print("Please enter the following information:")
    
    email = input("Email: ").strip()
    full_name = input("Full Name: ").strip()
    password = input("Password: ").strip()
    
    if not email or not full_name or not password:
        print("❌ All fields are required")
        return False
    
    # Create superuser using Django management command
    command = f"python manage.py shell -c \"from accounts.models import User; User.objects.create_superuser('{email}', '{full_name}', '{password}')\""
    
    return run_command(command, "Creating superuser")

def main():
    """Main setup function"""
    print("🚀 Fluxor API Setup Script")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Setup failed. Please install missing prerequisites.")
        sys.exit(1)
    
    # Create virtual environment if not exists
    if not os.path.exists('venv'):
        print("🐍 Creating virtual environment...")
        if not run_command("python -m venv venv", "Creating virtual environment"):
            print("❌ Failed to create virtual environment")
            sys.exit(1)
        print("✅ Virtual environment created")
        print("⚠️  Please activate it: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)")
        print("⚠️  Then run this script again")
        sys.exit(0)
    
    # Create .env file
    if not create_env_file():
        print("❌ Failed to create .env file")
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        print("❌ Database setup failed")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Run migrations
    if not run_migrations():
        print("❌ Failed to run migrations")
        sys.exit(1)
    
    # Create superuser
    if not create_superuser():
        print("❌ Failed to create superuser")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start Redis server: redis-server")
    print("2. Start Django server: python manage.py runserver")
    print("3. Start Celery worker: celery -A fluxor_api worker -l info")
    print("4. Start Celery beat: celery -A fluxor_api beat -l info")
    print("5. Access admin interface: http://localhost:8000/admin/")
    print("6. Test API endpoints: http://localhost:8000/api/")

if __name__ == "__main__":
    main() 
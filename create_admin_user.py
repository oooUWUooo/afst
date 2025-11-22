#!/usr/bin/env python3
"""
Script to create an initial admin user in the database
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app.models.user import User
from app.auth.jwt_handler import get_password_hash

def create_admin_user():
    db = SessionLocal()
    
    try:
        # Check if admin user already exists
        existing_admin = db.query(User).filter(User.email == "admin@example.com").first()
        if existing_admin:
            print("Admin user already exists!")
            print(f"Email: {existing_admin.email}")
            return
        
        # Create a hashed password for "admin123"
        password = "admin123"[:72]  # Truncate to 72 characters for bcrypt
        hashed_password = get_password_hash(password)
        
        # Create admin user
        admin_user = User(
            email="admin@example.com",
            hashed_password=hashed_password,
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("Admin user created successfully!")
        print("Email: admin@example.com")
        print("Password: admin123")
        print("Please change this password after your first login for security.")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
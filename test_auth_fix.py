#!/usr/bin/env python3
"""
Test script to verify that the authentication fixes work properly.
This tests the password length validation and bcrypt functionality.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.auth.jwt_handler import get_password_hash, verify_password

def test_password_validation():
    print("Testing password validation and hashing...")
    
    # Test normal password
    normal_password = "normalpassword123"
    try:
        hashed = get_password_hash(normal_password)
        verified = verify_password(normal_password, hashed)
        print(f"✓ Normal password: {verified}")
    except Exception as e:
        print(f"✗ Normal password failed: {e}")
    
    # Test long password (should be truncated automatically)
    long_password = "a" * 80  # 80 characters, longer than 72-byte bcrypt limit
    try:
        hashed = get_password_hash(long_password)
        # Verify with original long password (should work due to truncation in verify function)
        verified = verify_password(long_password, hashed)
        print(f"✓ Long password (80 chars) truncated and verified: {verified}")
    except Exception as e:
        print(f"✗ Long password failed: {e}")
    
    # Test very long password with special characters
    very_long_password = "p@ssw0rd_123!@#$%^&*()" + "x" * 70  # More than 72 bytes
    try:
        hashed = get_password_hash(very_long_password)
        verified = verify_password(very_long_password, hashed)
        print(f"✓ Very long password with special chars verified: {verified}")
    except Exception as e:
        print(f"✗ Very long password with special chars failed: {e}")
    
    print("Password validation tests completed!")

if __name__ == "__main__":
    test_password_validation()
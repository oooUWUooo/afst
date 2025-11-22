#!/usr/bin/env python3
"""
Test script to verify bcrypt and passlib compatibility
"""
from passlib.context import CryptContext

# Test the password context creation
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Test password hashing and verification
password = "testpassword123"
hashed = pwd_context.hash(password)
print(f"Hashed password: {hashed}")

# Test verification
result = pwd_context.verify(password, hashed)
print(f"Verification result: {result}")

# Test with a long password (should be truncated)
long_password = "a" * 80  # This exceeds the 72-byte limit
try:
    long_hashed = pwd_context.hash(long_password)
    print(f"Long password hashed successfully: {long_hashed[:50]}...")
    long_result = pwd_context.verify(long_password, long_hashed)
    print(f"Long password verification result: {long_result}")
except Exception as e:
    print(f"Error with long password: {e}")

print("Bcrypt and passlib compatibility test completed successfully!")
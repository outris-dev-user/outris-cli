"""
Tests for authentication commands
"""

import pytest
from outris.client import MockBackendClient

def test_signup():
    """Test signup flow with mock backend"""
    client = MockBackendClient()
    
    # Test OTP request
    result = client.signup("test@example.com", "Test Org")
    assert "message" in result
    assert result["expires_in"] == 300
    
    # Test OTP verification
    result = client.verify_otp("test@example.com", "123456")
    assert "api_key" in result
    assert result["api_key"].startswith("sk_outris_")

def test_login():
    """Test login flow with mock backend"""
    client = MockBackendClient()
    
    result = client.login("test@example.com")
    assert "message" in result
    assert result["expires_in"] == 300

"""
Tests for API management commands
"""

import pytest
from outris.client import MockBackendClient

def test_register_api():
    """Test API registration"""
    client = MockBackendClient()
    
    spec = {
        "openapi": "3.0.0",
        "info": {"title": "Test API"},
        "paths": {
            "/users": {"get": {}},
            "/posts": {"get": {}, "post": {}}
        }
    }
    
    result = client.register_api(spec, "Test API", "org")
    assert result["name"] == "Test API"
    assert result["endpoints"] == 2
    assert result["visibility"] == "org"

def test_list_apis():
    """Test listing APIs"""
    client = MockBackendClient()
    
    result = client.list_apis("all")
    assert result["count"] == 3
    assert len(result["apis"]) == 3

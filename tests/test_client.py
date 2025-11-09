"""
Tests for backend client
"""

import pytest
from outris.client import create_client, MockBackendClient, RealBackendClient
import os

def test_create_mock_client():
    """Test mock client creation"""
    os.environ["OUTRIS_USE_MOCK"] = "true"
    client = create_client()
    assert isinstance(client, MockBackendClient)

def test_create_real_client():
    """Test real client creation"""
    os.environ["OUTRIS_USE_MOCK"] = "false"
    client = create_client()
    assert isinstance(client, RealBackendClient)

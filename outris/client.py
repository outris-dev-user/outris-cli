"""
Backend API client - supports mock and real backends
"""

import os
import requests
from typing import Dict, Any, Protocol
from outris.config import get_api_key

class BackendClient(Protocol):
    """Interface for backend clients"""
    def signup(self, email: str, org_name: str) -> Dict[str, Any]: ...
    def verify_otp(self, email: str, otp: str) -> Dict[str, Any]: ...
    def login(self, email: str) -> Dict[str, Any]: ...
    def register_api(self, spec: Dict, name: str, visibility: str) -> Dict[str, Any]: ...
    def add_secret(self, api_name: str, key_name: str, value: str) -> Dict[str, Any]: ...
    def list_apis(self, scope: str = "all") -> Dict[str, Any]: ...
    def query(self, query_text: str) -> Dict[str, Any]: ...
    def get_history(self, limit: int = 10) -> Dict[str, Any]: ...
    def invite_member(self, email: str, role: str) -> Dict[str, Any]: ...
    def accept_invitation(self, token: str, email: str, otp: str) -> Dict[str, Any]: ...
    def list_team(self) -> Dict[str, Any]: ...
    def get_marketplace(self) -> Dict[str, Any]: ...
    def install_from_marketplace(self, api_name: str) -> Dict[str, Any]: ...


class MockBackendClient:
    """Mock client for development when backend isn't ready"""
    
    def signup(self, email: str, org_name: str) -> Dict[str, Any]:
        return {
            "message": "OTP sent to email (MOCKED)",
            "expires_in": 300
        }
    
    def verify_otp(self, email: str, otp: str) -> Dict[str, Any]:
        return {
            "api_key": "sk_outris_mock_abc123",
            "org_id": "org_mock_123",
            "org_name": email.split('@')[0],
            "email": email
        }
    
    def login(self, email: str) -> Dict[str, Any]:
        return {
            "message": "OTP sent to email (MOCKED)",
            "expires_in": 300
        }
    
    def register_api(self, spec: Dict, name: str, visibility: str) -> Dict[str, Any]:
        return {
            "api_id": "api_mock_456",
            "name": name,
            "endpoints": len(spec.get("paths", {})),
            "intent_mappings": 10,
            "visibility": visibility
        }
    
    def add_secret(self, api_name: str, key_name: str, value: str) -> Dict[str, Any]:
        return {
            "message": f"Secret {key_name} stored (MOCKED)"
        }
    
    def list_apis(self, scope: str = "all") -> Dict[str, Any]:
        return {
            "count": 3,
            "apis": [
                {"name": "Mock Weather API", "visibility": "public", "endpoints": 5},
                {"name": "Mock Payment API", "visibility": "org", "endpoints": 12},
                {"name": "Mock Analytics API", "visibility": "private", "endpoints": 8},
            ]
        }
    
    def query(self, query_text: str) -> Dict[str, Any]:
        return {
            "result": {
                "message": f"Mock result for: {query_text}",
                "data": {"temperature": 72, "condition": "sunny"}
            },
            "api_used": "Mock Weather API",
            "execution_time_ms": 123,
            "cost": 0.001
        }
    
    def get_history(self, limit: int = 10) -> Dict[str, Any]:
        return {
            "count": 2,
            "queries": [
                {"query": "get weather in SF", "api": "Mock Weather", "timestamp": "2025-11-09T10:30:00Z"},
                {"query": "create charge $50", "api": "Mock Payment", "timestamp": "2025-11-09T09:15:00Z"},
            ]
        }
    
    def invite_member(self, email: str, role: str) -> Dict[str, Any]:
        return {"message": f"Invitation sent to {email} (MOCKED)"}
    
    def accept_invitation(self, token: str, email: str, otp: str) -> Dict[str, Any]:
        return {
            "api_key": "sk_outris_mock_xyz789",
            "org_id": "org_mock_123",
            "role": "member"
        }
    
    def list_team(self) -> Dict[str, Any]:
        return {
            "count": 3,
            "members": [
                {"email": "alice@acme.com", "role": "owner"},
                {"email": "bob@acme.com", "role": "admin"},
                {"email": "charlie@acme.com", "role": "member"},
            ]
        }
    
    def get_marketplace(self) -> Dict[str, Any]:
        return {
            "count": 5,
            "apis": [
                {"name": "OpenWeatherMap", "installs": 1234, "category": "Weather"},
                {"name": "SendGrid", "installs": 890, "category": "Email"},
                {"name": "Twilio", "installs": 756, "category": "SMS"},
                {"name": "Stripe Demo", "installs": 456, "category": "Payments"},
                {"name": "Google Maps", "installs": 2341, "category": "Maps"},
            ]
        }
    
    def install_from_marketplace(self, api_name: str) -> Dict[str, Any]:
        return {
            "message": f"{api_name} added to your org (MOCKED)",
            "api_id": "api_marketplace_123"
        }


class RealBackendClient:
    """Real HTTP client for deployed backend"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv(
            "OUTRIS_API_URL",
            "https://outris-api.railway.app"
        )
    
    def _request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with auth"""
        url = f"{self.base_url}{path}"
        
        # Add API key header if available
        api_key = get_api_key()
        if api_key:
            kwargs.setdefault('headers', {})
            kwargs['headers']['X-API-Key'] = api_key
        
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def signup(self, email: str, org_name: str) -> Dict[str, Any]:
        return self._request('POST', '/api/v1/auth/signup', json={
            "email": email,
            "org_name": org_name
        })
    
    def verify_otp(self, email: str, otp: str) -> Dict[str, Any]:
        return self._request('POST', '/api/v1/auth/verify-otp', json={
            "email": email,
            "otp": otp
        })
    
    def login(self, email: str) -> Dict[str, Any]:
        return self._request('POST', '/api/v1/auth/login', json={
            "email": email
        })
    
    def register_api(self, spec: Dict, name: str, visibility: str) -> Dict[str, Any]:
        return self._request('POST', '/api/v1/apis/register', json={
            "spec": spec,
            "name": name,
            "visibility": visibility
        })
    
    def add_secret(self, api_name: str, key_name: str, value: str) -> Dict[str, Any]:
        # First get API ID from name
        apis = self.list_apis(scope="org")
        api_id = next((a['api_id'] for a in apis['apis'] if a['name'] == api_name), None)
        
        if not api_id:
            raise ValueError(f"API '{api_name}' not found")
        
        return self._request('POST', f'/api/v1/apis/{api_id}/secrets', json={
            "key_name": key_name,
            "value": value
        })
    
    def list_apis(self, scope: str = "all") -> Dict[str, Any]:
        return self._request('GET', f'/api/v1/apis?scope={scope}')
    
    def query(self, query_text: str) -> Dict[str, Any]:
        return self._request('POST', '/api/v1/query', json={
            "query": query_text
        })
    
    def get_history(self, limit: int = 10) -> Dict[str, Any]:
        return self._request('GET', f'/api/v1/history?limit={limit}')
    
    def invite_member(self, email: str, role: str) -> Dict[str, Any]:
        return self._request('POST', '/api/v1/team/invite', json={
            "email": email,
            "role": role
        })
    
    def accept_invitation(self, token: str, email: str, otp: str) -> Dict[str, Any]:
        return self._request('POST', '/api/v1/team/accept', json={
            "token": token,
            "email": email,
            "otp": otp
        })
    
    def list_team(self) -> Dict[str, Any]:
        return self._request('GET', '/api/v1/team/members')
    
    def get_marketplace(self) -> Dict[str, Any]:
        return self._request('GET', '/api/v1/marketplace')
    
    def install_from_marketplace(self, api_name: str) -> Dict[str, Any]:
        return self._request('POST', '/api/v1/marketplace/install', json={
            "api_name": api_name
        })


def create_client(use_mock: bool = None) -> BackendClient:
    """
    Factory function to create appropriate client
    
    Use mock if:
    - Explicitly requested via use_mock=True
    - Environment variable OUTRIS_USE_MOCK is set
    - Backend not ready (development mode)
    """
    if use_mock is None:
        use_mock = os.getenv("OUTRIS_USE_MOCK", "true").lower() == "true"
    
    if use_mock:
        return MockBackendClient()
    else:
        return RealBackendClient()

"""
Input validation utilities
"""

import re
from typing import Optional

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_otp(otp: str) -> bool:
    """Validate OTP format (6 digits)"""
    return bool(re.match(r'^\d{6}$', otp))

def validate_api_key(key: str) -> bool:
    """Validate API key format"""
    return key.startswith('sk_outris_') and len(key) > 20

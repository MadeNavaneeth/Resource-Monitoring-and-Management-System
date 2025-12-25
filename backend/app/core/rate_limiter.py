"""
Simple in-memory rate limiter for FastAPI.
Limits requests per IP address.
"""
import time
from collections import defaultdict
from fastapi import Request, HTTPException, status

class RateLimiter:
    def __init__(self, requests_per_second: int = 10):
        self.requests_per_second = requests_per_second
        self.requests = defaultdict(list)
    
    def is_allowed(self, client_ip: str) -> bool:
        """Check if request is allowed based on rate limit."""
        now = time.time()
        window_start = now - 1.0  # 1 second window
        
        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if req_time > window_start
        ]
        
        # Check limit
        if len(self.requests[client_ip]) >= self.requests_per_second:
            return False
        
        # Record this request
        self.requests[client_ip].append(now)
        return True

# Global rate limiter instance - 100 req/sec to handle 1-second dashboard updates
rate_limiter = RateLimiter(requests_per_second=100)

async def rate_limit_middleware(request: Request, call_next):
    """Middleware to apply rate limiting."""
    client_ip = request.client.host if request.client else "unknown"
    
    # Skip rate limiting for non-API routes
    if not request.url.path.startswith("/api"):
        return await call_next(request)
    
    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please slow down."
        )
    
    return await call_next(request)

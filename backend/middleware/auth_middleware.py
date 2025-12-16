"""
JWT Authentication Middleware
Validates JWT tokens and enforces role-based access
"""

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.jwt_auth import verify_token
from typing import List, Optional

security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency to get current user from JWT token
    
    Usage:
        @router.get("/protected")
        async def protected_route(current_user = Depends(get_current_user)):
            return current_user
    """
    token = credentials.credentials
    try:
        payload = verify_token(token)
        return payload
    except HTTPException:
        raise


def require_role(allowed_roles: List[str]):
    """
    Dependency factory for role-based access control
    
    Usage:
        @router.get("/admin-only")
        async def admin_route(user = Depends(require_role(["admin"]))):
            return {"message": "Admin access granted"}
    """
    async def role_checker(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {allowed_roles}"
            )
        return current_user
    return role_checker


# Convenience dependencies
require_student = require_role(["student"])
require_teacher = require_role(["teacher"])
require_admin = require_role(["admin"])
require_teacher_or_admin = require_role(["teacher", "admin"])
























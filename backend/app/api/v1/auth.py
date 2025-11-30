"""
Authentication endpoints
MVP: Simple email/password auth with JWT
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr

router = APIRouter()


class UserCreate(BaseModel):
    """User registration request."""
    email: EmailStr
    password: str
    name: str


class UserLogin(BaseModel):
    """User login request."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """User info response."""
    id: str
    email: str
    name: str


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    """
    사용자 등록
    
    MVP에서는 간단한 이메일/비밀번호 등록.
    Phase 2에서 OAuth (Google, Kakao) 추가.
    """
    # TODO: Implement user registration with database
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="회원가입 기능 구현 예정"
    )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    사용자 로그인
    
    이메일/비밀번호로 JWT 토큰 발급.
    """
    # TODO: Implement login with password verification
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="로그인 기능 구현 예정"
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user():
    """
    현재 로그인한 사용자 정보
    """
    # TODO: Implement with JWT token verification
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="사용자 정보 조회 기능 구현 예정"
    )

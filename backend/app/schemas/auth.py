from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MeResponse(BaseModel):
    id: int
    email: str
    username: str | None
    first_name: str
    last_name: str
    phone: str | None
    role: str
    is_active: bool


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str | None = None
    password: str
    first_name: str
    last_name: str
    phone: str | None = None


class RegisterResponse(BaseModel):
    id: int
    email: str
    username: str | None
    first_name: str
    last_name: str
    phone: str | None
    role: str
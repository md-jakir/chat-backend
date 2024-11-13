from pydantic import BaseModel, EmailStr
from datetime import datetime

class AuthLoginBase(BaseModel):
    email: EmailStr
    password: str

class AuthRegisterBase(BaseModel):
    email: EmailStr
    name: str
    password: str
    phone: str

class AuthUserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    phone: str
    created_at: datetime
    updated_at: datetime

class RegisterUserResponse(BaseModel):
    status_code: int
    message: str
    data: AuthUserResponse

class AuthLoginResponse(BaseModel):
    user: AuthUserResponse
    message: str
    status_code: int
    access_token: str
    token_type: str

class AuthAdminResponse(BaseModel):
    admin: AuthUserResponse
    message: str
    status_code: int
    access_token: str
    token_type: str
    

class GoogleLoginDTO(BaseModel):
    token: str

class GoogleUserDTO(BaseModel):
    email: str
    given_name: str = None
    family_name: str = None
    name: str

class GoogleAuthUser(BaseModel):
    email: str
    name: str
    phone: str = None

class TokenResponse(BaseModel):
    user: GoogleAuthUser
    token: str



    class Config:
        from_attributes = True


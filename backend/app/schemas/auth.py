from typing import Optional
from pydantic import BaseModel, ConfigDict

class LoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: str
    role: str
    department: Optional[str] = None
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

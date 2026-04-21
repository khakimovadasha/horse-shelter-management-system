from pydantic import BaseModel


class UserRead(BaseModel):
    id: int
    email: str
    username: str | None
    first_name: str
    last_name: str
    phone: str | None
    is_active: bool
    role: str

class UpdateUserRoleRequest(BaseModel):
    role: str

class UpdateUserActiveRequest(BaseModel):
    is_active: bool
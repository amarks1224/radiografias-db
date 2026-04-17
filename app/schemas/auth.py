from pydantic import BaseModel, ConfigDict


class GoogleTokenRequest(BaseModel):
    id_token: str


class AuthUserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: AuthUserResponse
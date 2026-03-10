from sqlalchemy.orm import Session

from app.schemas.auth import TokenResponse, UserLoginRequest, UserRegisterRequest, UserResponse
from app.services.auth_service import login_user, register_user


def register(payload: UserRegisterRequest, db: Session) -> TokenResponse:
    user = register_user(db, payload)
    token, _ = login_user(db, UserLoginRequest(email=payload.email, password=payload.password))
    return TokenResponse(access_token=token, user=UserResponse.model_validate(user))


def login(payload: UserLoginRequest, db: Session) -> TokenResponse:
    token, user = login_user(db, payload)
    return TokenResponse(access_token=token, user=UserResponse.model_validate(user))

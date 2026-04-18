from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import GoogleTokenRequest, AuthResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

auth_service = AuthService()


@router.post("/google", response_model=AuthResponse)
def login_with_google(payload: GoogleTokenRequest, db: Session = Depends(get_db)):
    return auth_service.login_with_google(db, payload.id_token)
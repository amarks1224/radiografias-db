from fastapi import HTTPException, status
from google.auth.transport import requests
from google.oauth2 import id_token as google_id_token
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

    def login_with_google(self, db: Session, token: str):
        try:
            idinfo = google_id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.google_client_id
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de Google inválido"
            )

        email = idinfo.get("email")
        email_verified = idinfo.get("email_verified", False)
        google_sub = idinfo.get("sub")
        full_name = idinfo.get("name", "")

        if not email or not google_sub:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo obtener la información del usuario desde Google"
            )

        if not email_verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="El correo de Google no está verificado"
            )

        first_name, last_name = self._split_name(full_name)

        user = self.user_repository.get_by_google_sub(db, google_sub)

        if not user:
            user = self.user_repository.get_by_email(db, email)

        if not user:
            user = self.user_repository.create_google_user(
                db=db,
                first_name=first_name,
                last_name=last_name,
                email=email,
                google_sub=google_sub
            )
        else:
            user = self.user_repository.update_google_user(
                db=db,
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                google_sub=google_sub
            )

        access_token = create_access_token({
            "sub": str(user.id),
            "email": user.email
        })

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }

    def _split_name(self, full_name: str) -> tuple[str, str]:
        parts = full_name.strip().split()

        if not parts:
            return "Usuario", "Google"

        if len(parts) == 1:
            return parts[0], ""

        return parts[0], " ".join(parts[1:])
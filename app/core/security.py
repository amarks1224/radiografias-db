from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException, status
from jwt import PyJWTError, ExpiredSignatureError, InvalidTokenError

from app.core.config import settings
import jwt


def create_access_token(data: dict, expires_minutes: Optional[int] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or settings.jwt_expire_minutes
    )
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        return payload
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    
    
def create_signed_radiograph_token(
    user_id: int,
    radiograph_id: int,
    expires_minutes: Optional[int] = None
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or settings.signed_url_expire_minutes
    )

    payload = {
        "sub": str(user_id),
        "radiograph_id": radiograph_id,
        "type": "radiograph_access",
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.signed_url_secret,
        algorithm=settings.jwt_algorithm
    )


def decode_signed_radiograph_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.signed_url_secret,
            algorithms=[settings.jwt_algorithm]
        )

        if payload.get("type") != "radiograph_access":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tipo de token inválido"
            )

        return payload

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El enlace ha expirado"
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Enlace inválido"
        )
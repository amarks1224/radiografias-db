from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def get_all_users(self, db: Session):
        return self.repository.get_all(db)

    def get_user_by_id(self, db: Session, user_id: int):
        user = self.repository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return user

    def create_user(self, db: Session, user_data: UserCreate):
        existing_user = self.repository.get_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un usuario con ese correo"
            )
        return self.repository.create(db, user_data)

    def update_user(self, db: Session, user_id: int, user_data: UserUpdate):
        user = self.repository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        if user_data.email:
            existing_user = self.repository.get_by_email(db, user_data.email)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe otro usuario con ese correo"
                )

        return self.repository.update(db, user, user_data)

    def delete_user(self, db: Session, user_id: int):
        user = self.repository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        self.repository.delete(db, user)
        return {"message": "Usuario eliminado correctamente"}
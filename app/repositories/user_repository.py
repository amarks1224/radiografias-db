from datetime import datetime
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    def get_all(self, db: Session) -> list[User]:
        return db.query(User).all()

    def get_by_id(self, db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def get_by_google_sub(self, db: Session, google_sub: str) -> User | None:
        return db.query(User).filter(User.google_sub == google_sub).first()

    def create(self, db: Session, user_data: UserCreate) -> User:
        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def create_google_user(
        self,
        db: Session,
        first_name: str,
        last_name: str,
        email: str,
        google_sub: str
    ) -> User:
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            google_sub=google_sub
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(self, db: Session, user: User, user_data: UserUpdate) -> User:
        update_data = user_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(user, field, value)

        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user

    def update_google_user(
        self,
        db: Session,
        user: User,
        first_name: str,
        last_name: str,
        email: str,
        google_sub: str
    ) -> User:
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.google_sub = google_sub
        user.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(user)
        return user

    def delete(self, db: Session, user: User) -> None:
        db.delete(user)
        db.commit()
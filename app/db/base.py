# Clase base de la que heredarán todos los modelos de SQLAlchemy.
# Sirve para que SQLAlchemy reconozca las clases como tablas de la base de datos.
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
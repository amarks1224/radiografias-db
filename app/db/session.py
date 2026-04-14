# Configuración de la conexión a SQLite.
# Aquí se define el motor de la base de datos y la fábrica de sesiones.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./radiografias.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
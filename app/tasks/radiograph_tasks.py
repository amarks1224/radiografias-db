from datetime import datetime

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.radiograph import Radiograph


def hide_radiographs_daily():
    db: Session = SessionLocal()
    try:
        radiographs = db.query(Radiograph).filter(
            Radiograph.is_hidden == False,
            Radiograph.image_url.isnot(None)
        ).all()

        now = datetime.utcnow()

        for radiograph in radiographs:
            radiograph.is_hidden = True
            radiograph.hidden_at = now

        db.commit()
        print(f"Radiografías ocultadas: {len(radiographs)}")

    except Exception as e:
        db.rollback()
        print(f"Error ocultando radiografías: {e}")

    finally:
        db.close()
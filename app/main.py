from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

from app.tasks.radiograph_tasks import hide_radiographs_daily
from app.routers import patient_router, radiograph_router, user_router, auth_router

app = FastAPI(title="Radiografias API")

scheduler = BackgroundScheduler()

"""
scheduler.add_job(
    hide_radiographs_daily,
    "cron",
    hour=23,
    minute=59,
    id="hide_radiographs_daily",
    replace_existing=True
)
"""

scheduler.add_job(
    hide_radiographs_daily,
    "interval",
    minutes=1,
    id="hide_radiographs_daily",
    replace_existing=True
)

scheduler.start()


@app.get("/")
def root():
    return {"message": "API running"}


@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()


app.include_router(auth_router.router)
app.include_router(patient_router.router)
app.include_router(radiograph_router.router)
app.include_router(user_router.router)
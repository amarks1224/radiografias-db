from fastapi import FastAPI

from app.routers import patient_router, radiograph_router, user_router, auth_router

app = FastAPI(title="Radiografias API")


@app.get("/")
def root():
    return {"message": "API running"}

app.include_router(auth_router.router)
app.include_router(patient_router.router)
app.include_router(radiograph_router.router)
app.include_router(user_router.router)
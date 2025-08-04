from fastapi import FastAPI
from app.routes import auth, upload

app = FastAPI()
app.include_router(auth.router)
app.include_router(upload.router)

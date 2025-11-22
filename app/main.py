from fastapi import FastAPI
from .db import db, Base
from .routers import router
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "https://almera.es",  # Replace with your frontend domain
    "https://www.almera.es",
    "https://api.almera.es",
]

app = FastAPI(title="Almera URL Shortener Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=db.engine)

# register routers
app.include_router(router)

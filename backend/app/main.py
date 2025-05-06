from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import upload

app = FastAPI()

# 👇 Add this block to allow your React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)

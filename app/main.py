from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

# Supabase client
from app.supabase_client import supabase

# Routes
from app.routes import auth, candidates, voters

# Auth
from app.auth import get_current_user
from app.models import UserInDB

app = FastAPI(title="Voting Platform Backend")

# CORS Setup
origins = [
    "https://online-voting-platform-khaki.vercel.app",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:8000",
    "*", # Re-adding wildcard to fix "Error loading candidates" if origin varies
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(candidates.router)
app.include_router(voters.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Voting Platform API"}

@app.get("/me", response_model=UserInDB)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user
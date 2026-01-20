from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
from app.supabase_client import supabase

router = APIRouter()

class VoterInfo(BaseModel):
    name: str
    linkedin_profile_url: str

@router.get("/voters", response_model=List[VoterInfo])
async def get_voters():
    # Fetch users who have voted
    response = supabase.table("users").select("name, linkedin_profile_url").eq("has_voted", True).execute()
    users = response.data
    
    voters = []
    if users:
        for user in users:
            # Check against None to avoid crashes
            name = user.get("name") or "Unknown"
            profile = user.get("linkedin_profile_url") or ""
            voters.append(VoterInfo(name=name, linkedin_profile_url=profile))
        
    return voters

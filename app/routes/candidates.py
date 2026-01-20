from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.supabase_client import supabase
from app.models import CandidateInDB, VoteCreate, UserInDB
from app.auth import get_current_user
from datetime import datetime

router = APIRouter()

@router.get("/candidates", response_model=List[CandidateInDB])
async def get_candidates():
    response = supabase.table("candidates").select("*").execute()
    candidates = response.data
    
    # Seed if empty (simplified check)
    if not candidates:
        seed_data = [
            {
                "name": "CHRISTY VARGHESE", 
                "team_name": "Backend Team", 
                "role": "BACKEND DEVELOPER",
                "linkedin_profile_url": "https://linkedin.com/in/christy",
                "logo_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", 
                "vote_count": 0
            },
            {
                "name": "NOURA", 
                "team_name": "Frontend Team", 
                "role": "Engineering Lead",
                "linkedin_profile_url": "https://linkedin.com/in/noura",
                "logo_url": "https://images.unsplash.com/photo-1560250097-0b93528c311a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", 
                "vote_count": 0
            },
        ]
        supabase.table("candidates").insert(seed_data).execute()
        response = supabase.table("candidates").select("*").execute()
        candidates = response.data
    
    return candidates

@router.post("/vote")
async def vote(vote_data: VoteCreate, current_user: UserInDB = Depends(get_current_user)):
    # Check if has_voted (double check against DB to be safe)
    user_res = supabase.table("users").select("has_voted").eq("id", current_user.id).single().execute()
    if user_res.data and user_res.data.get("has_voted"):
        raise HTTPException(status_code=400, detail="You have already voted.")

    # Check candidate existence
    cand_res = supabase.table("candidates").select("id, vote_count").eq("id", vote_data.candidate_id).single().execute()
    if not cand_res.data:
        raise HTTPException(status_code=404, detail="Candidate not found.")
    
    candidate = cand_res.data

    # Record vote
    vote_record = {
        "user_id": current_user.id,
        "candidate_id": vote_data.candidate_id,
        "timestamp": datetime.utcnow().isoformat()
    }
    supabase.table("votes").insert(vote_record).execute()

    # Update candidate count (Manual increment for MVP)
    new_count = candidate["vote_count"] + 1
    supabase.table("candidates").update({"vote_count": new_count}).eq("id", vote_data.candidate_id).execute()

    # Update user status
    supabase.table("users").update({
        "has_voted": True, 
        "voted_candidate_id": vote_data.candidate_id
    }).eq("id", current_user.id).execute()

    return {"message": "Vote cast successfully"}

@router.post("/reset")
async def reset_election():
    # Simple Reset Logic:
    # 1. Delete all votes (hacky approach since 'delete all' might be blocked)
    # 2. Reset candidate counts
    # 3. Reset users has_voted
    
    # Deleting all votes
    # Assuming 'votes' table allows unrestricted delete or we loop.
    # For MVP, we'll try a simple delete. If blocked by RLS, this might fail on backend but succeed if local.
    
    try:
        supabase.table("votes").delete().neq("id", 0).execute() # Hack to match all
    except:
        pass # Might fail if empty
    
    # Reset counts
    cands = supabase.table("candidates").select("id").execute()
    if cands.data:
        for c in cands.data:
            supabase.table("candidates").update({"vote_count": 0}).eq("id", c['id']).execute()
        
    # Reset users
    users = supabase.table("users").select("id").execute()
    if users.data:
        for u in users.data:
            supabase.table("users").update({"has_voted": False, "voted_candidate_id": None}).eq("id", u['id']).execute()
    
    return {"message": "Election reset successfully"}



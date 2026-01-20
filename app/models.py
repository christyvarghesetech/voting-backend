from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    linkedin_profile_url: Optional[str] = None
    picture: Optional[str] = None

class UserCreate(UserBase):
    provider: str  # google or linkedin
    provider_id: str

class UserInDB(UserBase):
    id: Optional[str] = None  # Supabase UUID
    provider: str
    has_voted: bool = False
    voted_candidate_id: Optional[int] = None # Integer ID for candidates

    class Config:
        from_attributes = True

class CandidateBase(BaseModel):
    name: str
    team_name: str
    role: str
    linkedin_profile_url: Optional[str] = None
    logo_url: Optional[str] = None

class CandidateInDB(CandidateBase):
    id: int # Integer ID
    vote_count: int = 0

    class Config:
        from_attributes = True

class VoteCreate(BaseModel):
    candidate_id: int # Changed to int to match probable SQL schema

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

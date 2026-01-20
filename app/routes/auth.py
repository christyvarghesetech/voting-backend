from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
import httpx

from app.config import settings
from app.supabase_client import supabase
from app.models import UserInDB
from app.auth import create_access_token, get_current_user
from pydantic import BaseModel

router = APIRouter()

# --- Google OAuth ---
@router.get("/auth/google")
async def login_google():
    return RedirectResponse(
        f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    )

@router.get("/auth/callback/google")
async def callback_google(code: str):
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data.get("access_token")
        
        user_info_response = await client.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
        user_info = user_info_response.json()

    # Create or update user
    user_data = {
        "email": user_info.get("email"),
        "name": user_info.get("name"),
        "picture": user_info.get("picture"),
        "provider": "google",
        "provider_id": user_info.get("id"),
    }
    
    # Check if user exists
    user_res = supabase.table("users").select("*").eq("email", user_data["email"]).execute()
    existing_user = user_res.data[0] if user_res.data else None
    
    if existing_user:
        user_id = str(existing_user["id"])
        # Update info
        supabase.table("users").update(user_data).eq("id", user_id).execute()
    else:
        # Create new user
        new_user_data = {**user_data, "has_voted": False}
        res = supabase.table("users").insert(new_user_data).execute()
        user_id = str(res.data[0]["id"])

    # Create JWT
    jwt_token = create_access_token(data={"sub": user_id})
    # Redirect to frontend
    return RedirectResponse(f"{settings.FRONTEND_URL}/candidates.html?token={jwt_token}")


# --- LinkedIn OAuth ---
@router.get("/auth/linkedin")
async def login_linkedin():
    # Note: State should be random for security, omitting for brevity
    return RedirectResponse(
        f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={settings.LINKEDIN_CLIENT_ID}&redirect_uri={settings.LINKEDIN_REDIRECT_URI}&scope=openid%20profile%20email"
    )

@router.get("/auth/callback/linkedin")
async def callback_linkedin(code: str):
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "client_secret": settings.LINKEDIN_CLIENT_SECRET,
        "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data.get("access_token")
        
        # Get User Info
        user_info_response = await client.get("https://api.linkedin.com/v2/userinfo", headers={"Authorization": f"Bearer {access_token}"})
        user_info = user_info_response.json()

    # Prepare user data
    user_data = {
        "email": user_info.get("email"),
        "name": f"{user_info.get('given_name', '')} {user_info.get('family_name', '')}".strip(),
        "picture": user_info.get("picture"),
        "provider": "linkedin",
        "provider_id": user_info.get("sub"),
        "linkedin_profile_url": f"https://www.linkedin.com/in/{user_info.get('sub')}"
    }

    # Check/Create User
    user_res = supabase.table("users").select("*").eq("email", user_data["email"]).execute()
    existing_user = user_res.data[0] if user_res.data else None
    
    if existing_user:
        user_id = str(existing_user["id"])
        supabase.table("users").update(user_data).eq("id", user_id).execute()
    else:
        new_user_data = {**user_data, "has_voted": False}
        res = supabase.table("users").insert(new_user_data).execute()
        user_id = str(res.data[0]["id"])

    jwt_token = create_access_token(data={"sub": user_id})
    return RedirectResponse(f"{settings.FRONTEND_URL}/candidates.html?token={jwt_token}")


class UserUpdate(BaseModel):
    linkedin_profile_url: str

@router.put("/me")
async def update_me(user_update: UserUpdate, current_user: UserInDB = Depends(get_current_user)):
    supabase.table("users").update(
        {"linkedin_profile_url": user_update.linkedin_profile_url}
    ).eq("id", current_user.id).execute()
    return {"message": "Profile updated successfully"}

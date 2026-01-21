# Voting System Backend API 🗳️

A robust, production-ready FastAPI backend for handling secure election voting.

## 🚀 Features
- **FastAPI:** High-performance Python framework.
- **Supabase Integration:** PostgreSQL database with real-time capabilities.
- **OAuth 2.0:** Secure authentication via Google & LinkedIn.
- **Role-Based Access:** Distinction between Voters and Admins.
- **RESTful API:** Endpoints for users, candidates, votes, and results.

## 🛠️ Tech Stack
- **Language:** Python 3.9+
- **Framework:** FastAPI
- **Database:** Supabase (PostgreSQL)
- **Deployment:** Render / Vercel

## ⚙️ Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd backend
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory:
   ```env
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_anon_key
   GOOGLE_CLIENT_ID=your_google_id
   GOOGLE_CLIENT_SECRET=your_google_secret
   LINKEDIN_CLIENT_ID=your_linkedin_id
   LINKEDIN_CLIENT_SECRET=your_linkedin_secret
   FRONTEND_URL=http://localhost:5500  # Or your Vercel URL
   ```

5. **Run Locally:**
   ```bash
   uvicorn app.main:app --reload
   ```
   Access docs at: `http://localhost:8000/docs`

## 📦 Deployment (Render)
1. Push code to GitHub.
2. Connect repo to Render.
3. Set **Build Command:** `pip install -r requirements.txt`
4. Set **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port 10000`
5. Add all Environment Variables in the Render Dashboard.

## 🗄️ Database Reset
To reset the election (clear all votes) without deleting users:
```bash
python reset_db.py
```

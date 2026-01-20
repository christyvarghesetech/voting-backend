# Backend Setup and Testing Instructions

## Prerequisites
1. **Python 3.8+** installed.
2. **MongoDB** installed and running locally on port 27017.

## Setup
1. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup**:
   - Rename `.env.example` to `.env`.
   - Update `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `LINKEDIN_CLIENT_ID`, `LINKEDIN_CLIENT_SECRET` with your real keys from Google Cloud Console and LinkedIn Developer Portal.

## Running the Server
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.
Docs are at `http://localhost:8000/docs`.

## Testing the Flow
Since OAuth requires browser interaction and redirects to localhost, you can test it manually:

### 1. Authentication
- Open your browser and go to `http://localhost:8000/auth/google` (or linkedin).
- Complete the login.
- You should receive a JSON response with an `access_token`. Copy this token.

### 2. Authorization
- For subsequent requests, use the header: `Authorization: Bearer <your_access_token>`.
- In Swagger UI (`/docs`), click "Authorize" and paste the token.

### 3. Voting
- Get Candidates: `GET /candidates` -> Note a `_id` of a candidate.
- Vote: `POST /vote`
  ```json
  {
    "candidate_id": "<candidate_id_from_step_above>"
  }
  ```
- Response should be success.

### 4. Verify
- Try to Vote again -> Should fail (400 Bad Request).
- Get Voters: `GET /voters` -> Should see your name.

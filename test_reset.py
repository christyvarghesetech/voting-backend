import httpx
import asyncio

async def test_reset():
    try:
        async with httpx.AsyncClient() as client:
            print("Sending POST /reset request...")
            # Note: No auth required for reset currently (for demo simplicity)
            r = await client.post("your-backend.onrender.com/reset")
            print(f"Status Code: {r.status_code}")
            print(f"Response: {r.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_reset())

from app.supabase_client import supabase


def reset_db():
    print("Resetting Supabase DB...")

    print("Clearing votes...")
    supabase.table("votes").delete().neq("id", "").execute()

    print("Resetting users...")
    supabase.table("users").update({
        "voted": False
    }).neq("id", "").execute()

    print("Resetting candidates...")
    supabase.table("candidates").update({"votes": 0}).neq("id", "").execute()

    print("Supabase reset complete.")


if __name__ == "__main__":
    reset_db()
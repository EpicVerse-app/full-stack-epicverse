import asyncio
import asyncpg

# --- DATABASE CONFIG ---
DATABASE_URL = "postgresql://postgres:Kriyora%402026@34.93.247.219/epicverse-db"

async def main():
    print("[DB-PURGE] Starting Production User Data Wipe...")
    
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        # 1. Clear Chat History (Depends on Users)
        await conn.execute("TRUNCATE TABLE chat_history RESTART IDENTITY CASCADE")
        print("🗑️  Chat History Wiped.")
        
        # 2. Clear Users
        await conn.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE")
        print("🗑️  User Profiles Wiped.")
        
        # 3. Clear OTPs
        await conn.execute("TRUNCATE TABLE user_otps RESTART IDENTITY CASCADE")
        print("🗑️  Auth OTP Records Wiped.")
        
        await conn.close()
        print("✅ Production Database is now CLEAN (Invite Codes & Game Data preserved).")
        
    except Exception as e:
        print(f"❌ Database Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def check_columns():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        columns = await conn.fetch("SELECT column_name FROM information_schema.columns WHERE table_name = 'card_combos'")
        print("\n--- Columns in card_combos table ---")
        for col in columns:
            print(col['column_name'])
            
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(check_columns())

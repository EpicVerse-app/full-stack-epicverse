import os
import asyncpg
import openai
from app.core.config import settings
from dotenv import load_dotenv

load_dotenv()

client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
DATABASE_URL = os.getenv("DATABASE_URL")

# Backwards compatibility for main.py list_modes
KNOWLEDGE_BASE_CACHE = []

async def load_excel_data():
    """No longer used, using PostgreSQL directly."""
    pass

async def get_available_modes():
    """Fetches unique game modes from the PostgreSQL database."""
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        rows = await conn.fetch("SELECT DISTINCT gameplay_mode FROM card_combos WHERE gameplay_mode IS NOT NULL")
        return [row['gameplay_mode'] for row in rows]
    except Exception as e:
        print(f"Error fetching modes: {e}")
        return ["Mode 1", "Mode 2"] # Fallback
    finally:
        await conn.close()

async def query_postgres_database(mode: str, character: str, karma: str) -> str:
    """Queries the live PostgreSQL database for the specified combo in the given mode."""
    # Ensure mode name matches the format in the DB (e.g., "Mode 1")
    # Handle formats like "mode_1", "mode1", "Mode 1"
    formatted_mode = mode.replace("_", " ").strip()
    if formatted_mode.lower() == "mode1": formatted_mode = "Mode 1"
    elif formatted_mode.lower() == "mode2": formatted_mode = "Mode 2"
    else:
        # Generic "mode X" to "Mode X"
        import re
        match = re.match(r"mode\s*(\d+)", formatted_mode, re.IGNORECASE)
        if match:
            formatted_mode = f"Mode {match.group(1)}"
        else:
            formatted_mode = formatted_mode.title()
    
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        # Search by name OR by card number (Order Independent)
        query = '''
            SELECT combo_status, final_status, validation_reason 
            FROM card_combos 
            WHERE LOWER(gameplay_mode) = LOWER($1)
            AND (
                (
                    (LOWER(character) = LOWER($2) OR CAST(character_card_number AS TEXT) = $2)
                    AND (LOWER(virtue_karma) = LOWER($3) OR CAST(virtue_karma_card_number AS TEXT) = $3)
                )
                OR
                (
                    (LOWER(character) = LOWER($3) OR CAST(character_card_number AS TEXT) = $3)
                    AND (LOWER(virtue_karma) = LOWER($2) OR CAST(virtue_karma_card_number AS TEXT) = $2)
                )
            )
        '''
        
        row = await conn.fetchrow(query, formatted_mode, character, karma)
        
        if row:
            # We provide both combo status and final status to ensure the AI knows exactly what's in the DB
            return f"Combo Status: {row['combo_status']} (Final Status: {row['final_status']})\nValidation Reason: {row['validation_reason']}"
        else:
            return f"No matching combo found in {formatted_mode} for Character: {character} and Virtue: {karma}."
            
    except Exception as e:
        print(f"PostgreSQL Query Error: {e}")
        return f"Error retrieving data from database: {str(e)}"
    finally:
        await conn.close()

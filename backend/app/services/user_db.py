import os
import asyncpg
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

class UserRecord(BaseModel):
    firebase_id: str
    display_name: str
    email: str
    primary_language: str
    profile_picture: str | None = None

async def get_connection():
    return await asyncpg.connect(DATABASE_URL)

async def init_db():
    conn = await get_connection()
    try:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                firebase_id TEXT PRIMARY KEY,
                display_name TEXT,
                email TEXT,
                primary_language TEXT,
                profile_picture TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Simple migration: Check if profile_picture column exists
        column_exists = await conn.fetchval('''
            SELECT count(*)
            FROM information_schema.columns 
            WHERE table_name='users' AND column_name='profile_picture'
        ''')
        if not column_exists:
            print("Migrating database: Adding profile_picture column to users table")
            await conn.execute("ALTER TABLE users ADD COLUMN profile_picture TEXT")
            
    finally:
        await conn.close()

async def save_user(user: UserRecord):
    conn = await get_connection()
    try:
        await conn.execute('''
            INSERT INTO users (firebase_id, display_name, email, primary_language, profile_picture)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (firebase_id) 
            DO UPDATE SET 
                display_name = EXCLUDED.display_name,
                email = EXCLUDED.email,
                primary_language = EXCLUDED.primary_language,
                profile_picture = EXCLUDED.profile_picture
        ''', user.firebase_id, user.display_name, user.email, user.primary_language, user.profile_picture)
    finally:
        await conn.close()
    return True

async def get_user(firebase_id: str):
    conn = await get_connection()
    try:
        row = await conn.fetchrow('SELECT * FROM users WHERE firebase_id = $1', firebase_id)
        if row:
            return dict(row)
    finally:
        await conn.close()
    return None

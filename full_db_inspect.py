import os
import asyncio
import json
from notion_client import AsyncClient
from dotenv import load_dotenv

load_dotenv()

async def full_inspect():
    api_key = os.getenv("NOTION_API_KEY")
    database_id = os.getenv("NOTION_DATABASE_ID")
    
    print(f"Database ID: {database_id}\n")
    
    client = AsyncClient(auth=api_key)
    
    try:
        db = await client.databases.retrieve(database_id=database_id)
        
        print("=== FULL DATABASE RESPONSE ===")
        print(json.dumps(db, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.aclose()

if __name__ == "__main__":
    asyncio.run(full_inspect())

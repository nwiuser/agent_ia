import os
import asyncio
import json
from notion_client import AsyncClient
from dotenv import load_dotenv

load_dotenv()

async def verify_structure():
    api_key = os.getenv("NOTION_API_KEY")
    database_id = os.getenv("NOTION_DATABASE_ID")
    
    print(f"Checking Database ID: {database_id}")
    
    client = AsyncClient(auth=api_key)
    
    try:
        db = await client.databases.retrieve(database_id=database_id)
        properties = db.get("properties", {})
        
        print("\nFound Properties:")
        for name, prop in properties.items():
            print(f"- {name} ({prop['type']})")
            
        # Check for Date
        date_props = [k for k, v in properties.items() if v['type'] == 'date']
        if date_props:
            print(f"\n✅ Date property found: {date_props}")
        else:
            print("\n❌ No Date property found!")

        # Check for Title
        title_props = [k for k, v in properties.items() if v['type'] == 'title']
        if title_props:
            print(f"✅ Title property found: {title_props}")
        else:
            print("❌ No Title property found!")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.aclose()

if __name__ == "__main__":
    asyncio.run(verify_structure())

import os
import asyncio
import json
from notion_client import AsyncClient
from dotenv import load_dotenv

load_dotenv()

async def inspect_page():
    api_key = os.getenv("NOTION_API_KEY")
    page_id = "2b67554405268153991ed4d579cffe12"  # La dernière tâche créée
    
    client = AsyncClient(auth=api_key)
    
    try:
        page = await client.pages.retrieve(page_id=page_id)
        
        print("=== PAGE PROPERTIES ===")
        props = page.get('properties', {})
        
        for name, prop in props.items():
            print(f"\n{name}:")
            print(f"  Type: {prop.get('type')}")
            
            if prop.get('type') == 'title':
                titles = prop.get('title', [])
                if titles:
                    print(f"  Value: {titles[0].get('plain_text')}")
                    
            elif prop.get('type') == 'date':
                date_obj = prop.get('date')
                if date_obj:
                    print(f"  Value: {date_obj.get('start')}")
                else:
                    print("  Value: None")
                    
            elif prop.get('type') == 'select':
                select = prop.get('select')
                if select:
                    print(f"  Value: {select.get('name')}")
                    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.aclose()

if __name__ == "__main__":
    asyncio.run(inspect_page())

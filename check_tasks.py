import os
import asyncio
from notion_client import AsyncClient
from dotenv import load_dotenv

load_dotenv()

async def check_tasks():
    api_key = os.getenv("NOTION_API_KEY")
    database_id = os.getenv("NOTION_DATABASE_ID")
    
    client = AsyncClient(auth=api_key)
    
    try:
        # Récupérer les pages de la base de données
        db_info = await client.databases.retrieve(database_id=database_id)
        print(f"Database: {db_info.get('title', [{}])[0].get('plain_text', 'Unknown')}")
        print(f"Properties: {list(db_info.get('properties', {}).keys())}\n")
        
        # Rechercher les pages de cette base
        response = await client.search(filter={"property": "object", "value": "page"})
        
        # Filtrer uniquement les pages de notre base
        pages = [p for p in response['results'] if p.get('parent', {}).get('database_id') == database_id.replace('-', '')]
        
        print(f"Found {len(pages)} tasks:\n")
        
        for page in pages:
            props = page['properties']
            
            # Extraire le titre
            title = "Untitled"
            if 'Name' in props and props['Name']['title']:
                title = props['Name']['title'][0]['plain_text']
            
            # Extraire la date
            date = "No date"
            if 'Due Date' in props and props['Due Date']['date']:
                date = props['Due Date']['date']['start']
            
            print(f"✅ {title}")
            print(f"   Date: {date}\n")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.aclose()

if __name__ == "__main__":
    asyncio.run(check_tasks())

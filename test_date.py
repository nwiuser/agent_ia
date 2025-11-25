import os
import asyncio
from dotenv import load_dotenv
from actions.notion import get_notion_manager

load_dotenv()

async def test():
    manager = get_notion_manager()
    
    print("Testing task creation with date...")
    result = await manager.create_task(
        title="Test avec date",
        due_date="2025-11-26T14:30:00",
        priority="high",
        description="Test pour vérifier si la date s'affiche"
    )
    
    print(f"\nResult: {result}")
    await manager.close()

if __name__ == "__main__":
    asyncio.run(test())

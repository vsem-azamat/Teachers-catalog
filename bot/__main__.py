import os
import asyncio 

# Change current directory to bot/
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

# Run bot
from bot import main
asyncio.run(main())
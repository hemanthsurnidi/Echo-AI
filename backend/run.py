import uvicorn
import os
import sys

# Add backend root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import init_db

if __name__ == "__main__":
    print("Initializing SQLite Database...")
    init_db()
    
    print("Starting Echo AI Backend Server...")
    # Run server on port 8000
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

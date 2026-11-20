import sys
from pathlib import Path
import uvicorn

# Ensure the backend directory is in the Python search path
PROJECT_ROOT = Path(__file__).resolve().parent
BACKEND_DIR = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

if __name__ == "__main__":
    print("=" * 65)
    print("  🚀 SalesTrack AI - Sales Tracking System")
    print("  Frontend UI : http://127.0.0.1:8000")
    print("  API Docs    : http://127.0.0.1:8000/docs")
    print("=" * 65)
    
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

import uvicorn
from api.routes import app  # Import the app directly from routes

def create_app():
    return app

if __name__ == "__main__":
    uvicorn.run(
        "main:create_app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )
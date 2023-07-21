import uvicorn
from core.config import config

print("postgres", config.POSTGRES_URL)

if __name__ == "__main__":
    uvicorn.run(
        app="core.server:app",
        reload=True if config.ENVIRONMENT != "production" else False,
        workers=1,
    )

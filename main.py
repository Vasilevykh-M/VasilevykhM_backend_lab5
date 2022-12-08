import uvicorn
import os

from dotenv import load_dotenv

from app import create_app
from fastapi.middleware.cors import CORSMiddleware


load_dotenv(verbose=True, dotenv_path=".env.local")
load_dotenv(verbose=True, dotenv_path=".env")


if __name__ == '__main__':
    uvicorn.run("main:app", host=os.getenv("HOST", "localhost"), port=int(os.getenv("PORT", 5000)),
                log_level="info", reload=True, reload_dirs=["app"])
else:
    app = create_app()
    origins = [
        "http://localhost",
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

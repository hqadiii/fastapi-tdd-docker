from fastapi import FastAPI

from app.api import ping, summaries
from app.db import init_db


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router)
    application.include_router(summaries.router, prefix="/summaries", tags=["Summaries"])
    return application


app = create_application()

init_db(app)

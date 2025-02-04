from fastapi import FastAPI

from app.core import config
from app.jobs import scheduler
from app.router.api_v1.endpoints import api_router

app = FastAPI(title=config.PROJECT_NAME,
              openapi_url=f"{config.API_V1_PREFIX}/openapi.json",
              version=config.VERSION,
              debug=config.DEBUG)

app.include_router(api_router, prefix=config.API_V1_PREFIX)

scheduler.start()

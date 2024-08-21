from fastapi import FastAPI

from .controllers import routers

app = FastAPI()

for router in routers:
    app.include_router(router)

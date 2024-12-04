from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routes import points
from app.core.data_store import data_store

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown using the lifespan context manager.
    """
    await data_store.hydrate()
    try:
        yield
    finally:
        await data_store.save()

app = FastAPI(title="Fetch Rewards Backend Challenge", version="1.0.0", lifespan=lifespan)

app.include_router(
    points.router,
    tags=["Points"],
)
import asyncio
import aiofiles
import json
from app.models.points_models import StoreData

class JsonStore:
    """
    Simple JSON Store class that reads and writes to a JSON file.
    """
    def __init__(self, file_path="store.json"):
        self.file_path = file_path
        self.data = StoreData()
        self.lock = asyncio.Lock()

    async def hydrate(self):
        try:
            async with aiofiles.open(self.file_path, "r") as f:
                raw_data = await f.read()
                self.data = StoreData(**json.loads(raw_data))
        except FileNotFoundError:
            await self._save_locked()

    async def save(self):
        async with self.lock:
            await self._save_locked()

    async def _save_locked(self):
        async with aiofiles.open(self.file_path, "w") as f:
            await f.write(self.data.model_dump_json())

    async def get(self, key: str):
        async with self.lock:
            return getattr(self.data, key, None)

    async def set(self, key: str, value):
        async with self.lock:
            setattr(self.data, key, value)

    async def append_transaction(self, transaction: dict):
        async with self.lock:
            self.data.transactions.append(transaction)
            await self._save_locked()

data_store = JsonStore()
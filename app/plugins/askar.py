from fastapi import HTTPException
import json
from aries_askar import Store
from anoncreds import create_link_secret
from config import settings


class AskarController:
    def __init__(self):
        self.db = f"{settings.POSTGRES_URI}/anoncreds"
        self.key = Store.generate_raw_key(settings.SECRET_KEY)

    async def provision(self, recreate=False):
        await Store.provision(self.db, "raw", self.key, recreate=recreate)
        try:
            await self.store("link_secret", "default", create_link_secret())
        except:
            pass

    async def open(self):
        return await Store.open(self.db, "raw", self.key)

    async def fetch(self, categroy, data_key):
        store = await self.open()
        try:
            async with store.session() as session:
                data = await session.fetch(categroy, data_key)
            return json.loads(data.value)
        except:
            raise HTTPException(status_code=404, detail="Couldn't find the ressource")

    async def store(self, category, data_key, data):
        store = await self.open()
        try:
            async with store.session() as session:
                await session.insert(
                    category,
                    data_key,
                    json.dumps(data),
                    {"~plaintag": "a", "enctag": "b"},
                )
        except:
            raise HTTPException(status_code=400, detail="Couldn't store data")

    async def force_store(self, category, data_key, data):
        store = await self.open()
        try:
            async with store.session() as session:
                await session.insert(
                    category,
                    data_key,
                    json.dumps(data),
                    {"~plaintag": "a", "enctag": "b"},
                )
        except:
            try:
                async with store.session() as session:
                    await session.replace(
                        category,
                        data_key,
                        json.dumps(data),
                        {"~plaintag": "a", "enctag": "b"},
                    )
            except:
                raise HTTPException(status_code=400, detail="Couldn't store data")

    async def update(self, category, data_key, data):
        store = await self.open()
        try:
            async with store.session() as session:
                await session.replace(
                    category,
                    data_key,
                    json.dumps(data),
                    {"~plaintag": "a", "enctag": "b"},
                )
        except:
            try:
                async with store.session() as session:
                    await session.insert(
                        category,
                        data_key,
                        json.dumps(data),
                        {"~plaintag": "a", "enctag": "b"},
                    )
            except:
                raise HTTPException(status_code=400, detail="Couldn't update data")

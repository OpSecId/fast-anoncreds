import json
from aries_askar import Store, error
from anoncreds import create_link_secret
from config import settings
import uuid
import hashlib
from app.validations import ValidationException


class AskarController:
    def __init__(self, profile=str(uuid.NAMESPACE_URL)):
        self.db = settings.POSTGRES_URI
        self.key = Store.generate_raw_key(settings.SECRET_KEY)
        self.profile = profile

    async def provision(self, recreate=False):
        await Store.provision(
            self.db, "raw", self.key, recreate=recreate, profile=self.profile
        )
        try:
            await self.store(
                "link_secret", str(uuid.NAMESPACE_URL), create_link_secret()
            )
        except:
            pass

    async def list_profiles(self):
        store = await self.open()
        profiles = await Store.list_profiles(store)
        profiles.remove(str(uuid.NAMESPACE_URL))
        return profiles

    async def profile_exists(self):
        profiles = await self.list_profiles()
        if self.profile not in profiles:
            raise ValidationException(
                status_code=400, content={"message": "Profile not found"}
            )
        return True

    async def create_profile(self, client_id):
        profiles = await self.list_profiles()
        if client_id in profiles:
            raise ValidationException(
                status_code=400, content={"message": "Profile already exists"}
            )
        store = await self.open()
        await Store.create_profile(store, client_id)
        await AskarController(client_id).store(
            "link_secret", str(uuid.NAMESPACE_URL), create_link_secret()
        )

    async def remove_profile(self):
        store = await self.open()
        await Store.remove_profile(store, self.profile)

    async def remove(self):
        await Store.remove(self.db)

    async def open(self):
        return await Store.open(self.db, "raw", self.key, profile=self.profile)

    async def fetch(self, categroy, data_key):
        store = await self.open()
        try:
            async with store.session() as session:
                data = await session.fetch(categroy, data_key)
            return json.loads(data.value)
        except:
            raise ValidationException(
                status_code=404, content={"message": "No records found"}
            )

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
            raise ValidationException(
                status_code=404, content={"message": "Could not store record"}
            )

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
                raise ValidationException(
                    status_code=404, content={"message": "Could not store record"}
                )

    async def compare_hash(self, client_secret):
        secret_hash = await self.fetch("client", "hash")
        if secret_hash != hashlib.md5(client_secret.encode()).hexdigest():
            raise ValidationException(
                status_code=401, content={"message": "Invalid credentials"}
            )

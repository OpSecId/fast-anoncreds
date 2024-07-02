import uvicorn

from app.plugins.askar import AskarController
import asyncio

if __name__ == "__main__":
    asyncio.run(AskarController().provision(recreate=True))

    uvicorn.run("app.api:app", host="0.0.0.0", port=8000)

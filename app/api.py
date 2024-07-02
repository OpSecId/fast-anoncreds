from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from app.routers import main
from config import settings

app = FastAPI(
    title=settings.PROJECT_TITLE,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
    contact=settings.PROJECT_CONTACT,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter()

api_router.include_router(main.router)


@api_router.get("/server/status", include_in_schema=False)
async def status_check():
    return JSONResponse(status_code=200, content={"status": "ok"})


app.include_router(api_router)


@app.get("/.well-known/did.json", include_in_schema=False)
async def did_document():
    did_doc = {"@context": ["https://www.w3.org/ns/did/v1"], "id": settings.DID_WEB}
    return JSONResponse(status_code=200, content=did_doc)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index():
    return RedirectResponse(url=settings.DOCS)

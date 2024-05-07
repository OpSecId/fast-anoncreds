from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from app.routers import auth, clients, credentials, presentations, registry
from app.validations import ValidationException
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

api_router.include_router(auth.router, tags=["Auth"], prefix="/auth")
api_router.include_router(clients.router, tags=["Clients"], prefix="/clients")
api_router.include_router(
    credentials.router, tags=["Credentials"], prefix="/credentials"
)
api_router.include_router(
    presentations.router, tags=["Presentations"], prefix="/presentations"
)
api_router.include_router(registry.router, tags=["AnonCredsVDR"])


@api_router.get("/server/status", include_in_schema=False)
async def status_check():
    return JSONResponse(status_code=200, content={"status": "ok"})


app.include_router(api_router)
# app.include_router(api_router, prefix="/api/v1")


@app.get("/.well-known/did.json", include_in_schema=False)
async def did_document():
    did_doc = {
        "@context": [
            "https://www.w3.org/ns/did/v1",
            "https://w3id.org/security/multikey/v1",
        ],
        "id": settings.DID_WEB,
        "service": [
            {
                "type": ["AnonCredsWebVDR"],
                "id": f"{settings.DID_WEB}#AnonCredsWebVDR",
                "controller": settings.DID_WEB,
                "serviceEndpoint": f"{settings.HTTPS_BASE}/vdr",
            },
            {
                "type": ["OCABundles"],
                "id": f"{settings.DID_WEB}#OCABundles",
                "controller": settings.DID_WEB,
                "serviceEndpoint": f"{settings.HTTPS_BASE}/oca",
            },
        ],
    }
    return JSONResponse(status_code=200, content=did_doc)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")


@app.exception_handler(ValidationException)
async def validation_exception_handler(
    request: Request, exception: ValidationException
):
    return JSONResponse(
        status_code=exception.status_code,
        content=exception.content,
    )


@app.exception_handler(RequestValidationError)
async def custom_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()[0]
    error = {
        "message": errors["msg"],
        "type": errors["type"],
        "location": errors["loc"],
    }
    return JSONResponse(error, status_code=400)

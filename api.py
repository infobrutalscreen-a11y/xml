from fastapi import (
    FastAPI, UploadFile, File, Request,
    Header, HTTPException, Depends
)
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

import os
from convert import convert

# ---------------- APP ----------------

app = FastAPI(title="XML → YML Converter")
templates = Jinja2Templates(directory="templates")

# ---------------- API KEY ----------------

API_KEY = os.getenv("API_KEY", "supersecretkey123")

async def check_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

# ---------------- RATE LIMIT ----------------

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"}
    )

# ---------------- WEB ----------------

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# ---------------- API v1 FILE ----------------

@app.post("/api/v1/convert")
@limiter.limit("10/minute")
async def api_convert(
    request: Request,
    file: UploadFile = File(...),
    _: None = Depends(check_api_key)
):
    temp_input = "temp_input.xml"
    temp_output = "temp_output.yml"

    with open(temp_input, "wb") as f:
        f.write(await file.read())

    convert(temp_input, temp_output)

    return FileResponse(
        temp_output,
        media_type="application/x-yaml",
        filename="feed.yml"
    )

# ---------------- API v1 JSON ----------------

@app.post("/api/v1/convert/json")
@limiter.limit("10/minute")
async def api_convert_json(
    request: Request,
    file: UploadFile = File(...),
    _: None = Depends(check_api_key)
):
    temp_input = "temp_input.xml"
    temp_output = "temp_output.yml"

    with open(temp_input, "wb") as f:
        f.write(await file.read())

    convert(temp_input, temp_output)

    with open(temp_output, "r", encoding="utf-8") as f:
        content = f.read()

    return {
        "status": "ok",
        "format": "yml",
        "content": content
    }

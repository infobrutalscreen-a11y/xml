import os
import time
import logging
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Request, Header, HTTPException, Depends
from fastapi.responses import HTMLResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates

from formats.parser import parse_cars
from formats.factory import get_formatter


# -------------------- logging --------------------
logger = logging.getLogger("feed-converter")
logger.setLevel(logging.INFO)

if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(h)


# -------------------- app --------------------
app = FastAPI(title="Feed Converter API")
templates = Jinja2Templates(directory="templates")

API_KEY = os.getenv("API_KEY", "supersecretkey123")


def require_api_key(x_api_key: Optional[str] = Header(None)) -> str:
    # Всегда 403 (и если нет заголовка тоже)
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key


@app.middleware("http")
async def access_log_middleware(request: Request, call_next):
    start = time.time()
    try:
        response = await call_next(request)
    except Exception as e:
        duration_ms = int((time.time() - start) * 1000)
        client_ip = request.headers.get("x-real-ip") or (request.client.host if request.client else "-")
        logger.exception(
            'ip=%s method=%s path="%s" status=%s time_ms=%s error="%s"',
            client_ip, request.method, request.url.path, 500, duration_ms, str(e)
        )
        raise

    duration_ms = int((time.time() - start) * 1000)
    client_ip = request.headers.get("x-real-ip") or (request.client.host if request.client else "-")
    ua = request.headers.get("user-agent", "-")
    logger.info(
        'ip=%s method=%s path="%s" status=%s time_ms=%s ua="%s"',
        client_ip, request.method, request.url.path, response.status_code, duration_ms, ua
    )
    return response


# -------------------- routes --------------------
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/v1/convert")
async def convert_feed(
    request: Request,
    file: UploadFile = File(...),
    format: str = "yml",
    _: str = Depends(require_api_key),
):
    xml_bytes = await file.read()

    try:
        cars = parse_cars(xml_bytes)
        formatter = get_formatter(format)
        result = formatter.render(cars)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Convert error: {e}")

    # content-type + filename
    if format == "yml":
        content_type = "application/x-yaml"
        filename = "feed.yml"
    else:
        content_type = "application/xml"
        filename = f"feed.{format}.xml"

    return Response(
        content=result,
        media_type=content_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.post("/api/v1/convert/json")
async def convert_feed_json(
    request: Request,
    file: UploadFile = File(...),
    format: str = "yml",
    _: str = Depends(require_api_key),
):
    try:
        xml_bytes = await file.read()
        cars = parse_cars(xml_bytes)
        formatter = get_formatter(format)
        result = formatter.render(cars)

        return {
            "status": "ok",
            "format": format,
            "items": len(cars),
            "content": result,
        }
    except ValueError as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})
    except Exception as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": f"Convert error: {e}"})

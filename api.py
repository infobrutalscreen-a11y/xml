import os
from fastapi import FastAPI, UploadFile, File, Request, Header, HTTPException, Form
from fastapi.responses import HTMLResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.responses import PlainTextResponse

from formats.parser import parse_cars, parse_bytes_by_format
from formats.factory import get_formatter
from formats.vk.vk_factory import get_vk_formatter


API_KEY = os.getenv("API_KEY", "supersecretkey123")
REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")

templates = Jinja2Templates(directory="templates")


def api_key_or_ip(request: Request) -> str:
    """
    Ключ для лимитов API: если есть X-API-Key — лимитируем по нему,
    иначе — по IP.
    """
    key = request.headers.get("X-API-Key")
    if key:
        return f"key:{key}"
    return f"ip:{get_remote_address(request)}"


limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=REDIS_URL,
)

app = FastAPI(title="Feed Converter API")
app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    # Единый ответ 429
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"}
    )


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    return {"status": "ok"}


def _build_download_response(result: str, format: str) -> Response:
    content_type = "application/xml"
    filename = f"feed.{format}.xml"

    if format == "yml":
        filename = "feed.yml"
        content_type = "application/x-yaml"

    return Response(
        content=result,
        media_type=content_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


# ---------------------------
# VK specific response helper
# ---------------------------

def _build_vk_download_response(result: str, output_format: str, category: str) -> Response:
    fmt = (output_format or "").lower()
    filename = f"{category}_feed.{fmt}"
    if fmt == "csv":
        content_type = "text/csv"
    elif fmt == "tsv":
        content_type = "text/tab-separated-values"
    elif fmt == "xml":
        content_type = "application/xml"
    elif fmt == "yml" or fmt == "yaml":
        filename = f"{category}_feed.yml"
        content_type = "application/x-yaml"
    else:
        content_type = "application/octet-stream"

    return Response(
        content=result,
        media_type=content_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


# ---------------------------
# WEB (без ключа)
# ---------------------------
@app.post("/web/convert")
@limiter.limit("2/second")  # лимит на веб по IP
async def web_convert_feed(
    request: Request,
    file: UploadFile = File(...),
    format: str = "yml",
):
    xml_bytes = await file.read()
    cars = parse_cars(xml_bytes)
    formatter = get_formatter(format)
    result = formatter.render(cars)
    return _build_download_response(result, format)


# ---------------------------
# API (с ключом)
# ---------------------------
@app.post("/api/v1/convert")
@limiter.limit("60/minute", key_func=api_key_or_ip)  # лимит на API по ключу
async def api_convert_feed(
    request: Request,
    file: UploadFile = File(...),
    format: str = "yml",
    x_api_key: str = Header(...),
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    xml_bytes = await file.read()
    cars = parse_cars(xml_bytes)
    formatter = get_formatter(format)
    result = formatter.render(cars)
    return _build_download_response(result, format)


@app.post("/api/v1/convert/json")
@limiter.limit("60/minute", key_func=api_key_or_ip)
async def api_convert_feed_json(
    request: Request,
    file: UploadFile = File(...),
    format: str = "yml",
    x_api_key: str = Header(...),
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    try:
        xml_bytes = await file.read()
        cars = parse_cars(xml_bytes)
        formatter = get_formatter(format)
        result = formatter.render(cars)

        return {
            "status": "ok",
            "format": format,
            "items": len(cars),
            "content": result
        }

    except Exception as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})


# ---------------------------
# VK endpoints (separate endpoint for clarity and easier scaling)
# ---------------------------
@app.post("/api/v1/convert/vk")
@limiter.limit("60/minute", key_func=api_key_or_ip)
async def api_convert_vk(
    request: Request,
    file: UploadFile = File(...),
    vk_category: str = Form("goods"),
    output_format: str = Form("csv"),
    input_format: str | None = Form(None),
    x_api_key: str = Header(...),
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    try:
        data_bytes = await file.read()
        rows = parse_bytes_by_format(data_bytes, input_format or "")

        cat = (vk_category or "goods").lower().strip()
        fmt = (output_format or "csv").lower().strip()

        formatter = get_vk_formatter(cat)
        result = formatter(rows, output_format=fmt)

        return _build_vk_download_response(result, fmt, cat)

    except Exception as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})


@app.post("/api/v1/convert/vk/json")
@limiter.limit("60/minute", key_func=api_key_or_ip)
async def api_convert_vk_json(
    request: Request,
    file: UploadFile = File(...),
    vk_category: str = Form("goods"),
    output_format: str = Form("csv"),
    input_format: str | None = Form(None),
    x_api_key: str = Header(...),
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    try:
        data_bytes = await file.read()
        rows = parse_bytes_by_format(data_bytes, input_format or "")

        cat = (vk_category or "goods").lower().strip()
        fmt = (output_format or "csv").lower().strip()

        formatter = get_vk_formatter(cat)
        result = formatter(rows, output_format=fmt)

        return {"status": "ok", "category": cat, "format": fmt, "items": len(rows), "content": result}

    except Exception as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})

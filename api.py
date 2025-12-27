import os
from fastapi import FastAPI, UploadFile, File, Request, Header, HTTPException, Depends
from fastapi.responses import HTMLResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates

from formats.parser import parse_cars
from formats.factory import get_formatter

app = FastAPI(title="Feed Converter API")
templates = Jinja2Templates(directory="templates")

API_KEY = os.getenv("API_KEY", "supersecretkey123")


def require_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    return {"status": "ok"}


# ---------- WEB (без ключа) ----------
@app.post("/convert")
async def web_convert(
    file: UploadFile = File(...),
    format: str = "yml",
):
    xml_bytes = await file.read()
    cars = parse_cars(xml_bytes)
    formatter = get_formatter(format)
    result = formatter.render(cars)

    content_type = "application/xml"
    filename = f"feed.{format}.xml"
    if format == "yml":
        filename = "feed.yml"
        content_type = "application/x-yaml"

    return Response(
        content=result,
        media_type=content_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ---------- API v1 (с ключом) ----------
@app.post("/api/v1/convert", dependencies=[Depends(require_api_key)])
async def api_convert(
    file: UploadFile = File(...),
    format: str = "yml",
):
    xml_bytes = await file.read()
    cars = parse_cars(xml_bytes)
    formatter = get_formatter(format)
    result = formatter.render(cars)

    content_type = "application/xml"
    filename = f"feed.{format}.xml"
    if format == "yml":
        filename = "feed.yml"
        content_type = "application/x-yaml"

    return Response(
        content=result,
        media_type=content_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.post("/api/v1/convert/json", dependencies=[Depends(require_api_key)])
async def api_convert_json(
    file: UploadFile = File(...),
    format: str = "yml",
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
    except Exception as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})

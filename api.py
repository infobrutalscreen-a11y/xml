import os
from fastapi import FastAPI, UploadFile, File, Request, Header, HTTPException
from fastapi.responses import HTMLResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates

from formats.parser import parse_cars
from formats.factory import get_formatter


app = FastAPI(title="Feed Converter API")
templates = Jinja2Templates(directory="templates")

API_KEY = os.getenv("API_KEY", "supersecretkey123")


async def check_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/v1/convert")
async def convert_feed(
    file: UploadFile = File(...),
    format: str = "yml",
    x_api_key: str = Header(...)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

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
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@app.post("/api/v1/convert/json")
async def convert_feed_json(
    file: UploadFile = File(...),
    format: str = "yml",
    x_api_key: str = Header(...)
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

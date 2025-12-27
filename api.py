import os
from fastapi import FastAPI, UploadFile, File, Request, Header, HTTPException, Depends, Query
from fastapi.responses import HTMLResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates

from formats.parser import parse_cars
from formats.factory import get_formatter, list_formats

app = FastAPI(title="Feed Converter API")
templates = Jinja2Templates(directory="templates")

API_KEY = os.getenv("API_KEY", "supersecretkey123")


def require_api_key(x_api_key: str = Header(None)):
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # страницу можно отдавать без ключа — ключ вводят в форме
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/api/v1/formats")
async def formats(_: None = Depends(require_api_key)):
    # список форматов защищаем ключом, чтобы не светить наружу
    return {"formats": list_formats()}


@app.post("/api/v1/convert")
async def convert_feed(
    file: UploadFile = File(...),
    format: str = Query("yml"),
    _: None = Depends(require_api_key),
):
    try:
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
    except ValueError as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})
    except Exception as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})


@app.post("/api/v1/convert/json")
async def convert_feed_json(
    file: UploadFile = File(...),
    format: str = Query("yml"),
    _: None = Depends(require_api_key),
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
            "content": result
        }
    except ValueError as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})
    except Exception as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})

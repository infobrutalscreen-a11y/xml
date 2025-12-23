import os
from fastapi import FastAPI, UploadFile, File, Request, Depends, Header, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from convert import convert

app = FastAPI(title="XML → YML Converter")

API_KEY = os.getenv("API_KEY")

templates = Jinja2Templates(directory="templates")


# ---------- API KEY ----------

def check_api_key(x_api_key: str = Header(...)):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API_KEY not set")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")


# ---------- WEB ----------

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ---------- API v1: файл ----------

@app.post("/api/v1/convert", dependencies=[Depends(check_api_key)])
async def api_convert(file: UploadFile = File(...)):
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


# ---------- API v1: JSON ----------

@app.post("/api/v1/convert/json", dependencies=[Depends(check_api_key)])
async def api_convert_json(file: UploadFile = File(...)):
    try:
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

    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": str(e)}
        )

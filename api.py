from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from convert import convert

app = FastAPI(title="XML → YML Converter")

templates = Jinja2Templates(directory="templates")


# ---------- WEB (форма) ----------

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# ---------- API v1 (файл YML) ----------

@app.post("/api/v1/convert")
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


# ---------- API v1 (JSON) ----------

@app.post("/api/v1/convert/json")
async def api_convert_json(file: UploadFile = File(...)):
    try:
        temp_input = "temp_input.xml"
        temp_output = "temp_output.yml"

        with open(temp_input, "wb") as f:
            f.write(await file.read())

        convert(temp_input, temp_output)

        with open(temp_output, "r", encoding="utf-8") as f:
            yml_data = f.read()

        return {
            "status": "ok",
            "format": "yml",
            "content": yml_data
        }

    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": str(e)}
        )

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import shutil
from convert import convert

app = FastAPI(title="XML → YML Converter")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


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


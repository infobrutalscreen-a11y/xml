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


@app.post("/convert")
async def convert_file(file: UploadFile = File(...)):
    temp_input_path = "temp_input.xml"
    temp_output_path = "temp_output.yml"

    with open(temp_input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        convert(temp_input_path, temp_output_path)
    except Exception as e:
        return {"error": str(e)}

    return FileResponse(
        temp_output_path,
        media_type="application/x-yaml",
        filename="output.yml"
    )

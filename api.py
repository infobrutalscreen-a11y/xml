from fastapi import FastAPI, UploadFile, File, Header, HTTPException, Request
from fastapi.responses import Response, HTMLResponse
from pathlib import Path
import time
import logging

from convert import convert_xml_to_yml

BASE_DIR = Path(__file__).parent
LOG_FILE = BASE_DIR / "access.log"

API_KEY = "supersecretkey123"

# ---------- ЛОГГЕР ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("api")

# ---------- APP ----------
app = FastAPI()


# ---------- HEALTH ----------
@app.get("/health")
def health():
    return {"status": "ok"}


# ---------- HTML ----------
@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <html>
        <body>
            <h2>XML → YML</h2>
            <form action="/api/v1/convert" method="post" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <button type="submit">Convert</button>
            </form>
        </body>
    </html>
    """


# ---------- API ----------
@app.post("/api/v1/convert")
async def api_convert(
    request: Request,
    file: UploadFile = File(...),
    x_api_key: str | None = Header(default=None)
):
    start = time.time()
    client_ip = request.client.host if request.client else "unknown"

    if x_api_key != API_KEY:
        logger.warning(f"{client_ip} | 403 | invalid api key")
        raise HTTPException(status_code=403, detail="Invalid API key")

    if not file.filename.endswith(".xml"):
        logger.warning(f"{client_ip} | 400 | bad file {file.filename}")
        raise HTTPException(status_code=400, detail="Only XML allowed")

    try:
        xml_data = await file.read()
        yml = convert_xml_to_yml(xml_data)

        duration = round(time.time() - start, 3)
        logger.info(f"{client_ip} | 200 | {file.filename} | {duration}s")

        return Response(
            content=yml,
            media_type="application/xml"
        )

    except Exception as e:
        logger.error(f"{client_ip} | 500 | {str(e)}")
        raise HTTPException(status_code=500, detail="Internal error")

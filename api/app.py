import io
import os

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image

from api.inference import MODEL_KEYS, MODEL_LABELS, get_registry
from api.middleware import RequestLoggingMiddleware
from logger import get_logger

app = FastAPI(title="Alzheimer MRI API", version="1.0.0")
logger = get_logger("api", "inference.log")

app.add_middleware(RequestLoggingMiddleware)

# Serve static files from frontend build
app.mount("/static", StaticFiles(directory="../alz-frontend-main/dist", html=True), name="static")

@app.get("/")
def read_root():
    return {"message": "Welcome to Alzheimer MRI API"}

@app.get("/app")
def serve_frontend():
    # Redirect or serve index.html
    from fastapi.responses import FileResponse
    return FileResponse("../alz-frontend-main/dist/index.html")


@app.on_event("startup")
def _log_startup():
    logger.info("API startup")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/models")
def list_models():
    return {"models": MODEL_LABELS}


@app.post("/analyse_mri")
async def analyse_mri(
    file: UploadFile = File(...),
    model_version: str = Form("SNNCap V2.0"),
):
    if model_version not in MODEL_KEYS:
        logger.warning("Unknown model version requested: %s", model_version)
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Unknown model_version",
                "allowed": MODEL_LABELS,
            },
        )

    try:
        raw = await file.read()
        img = Image.open(io.BytesIO(raw)).convert("L")
    except Exception as exc:
        logger.warning("Invalid image upload", exc_info=exc)
        raise HTTPException(status_code=400, detail="Invalid image") from exc

    registry = get_registry()
    result = registry.predict(img, model_version)
    logger.info("Prediction complete for %s", model_version)
    return JSONResponse(content=result)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api.app:app", host="0.0.0.0", port=int(os.getenv("PORT", 5000)), reload=False)

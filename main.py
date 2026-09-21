from __future__ import annotations

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.config import APP_TITLE
from app.services.ai_reader import generate_fortune
from app.services.astrology import build_astrology_report
from app.services.image_analysis import analyze_uploaded_image

app = FastAPI(title=APP_TITLE)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "app": APP_TITLE}


@app.post("/api/fortune")
async def read_fortune(
    file: UploadFile | None = File(default=None),
    name: str = Form(""),
    birth_date: str = Form(""),
    birth_time: str = Form(""),
    city: str = Form(""),
    tone: str = Form("warm"),
):
    has_birth_data = bool(name.strip() or birth_date.strip() or birth_time.strip() or city.strip())
    has_image = file is not None and getattr(file, "filename", "") not in (None, "")

    if not has_birth_data and not has_image:
        return JSONResponse(
            {"detail": "En az bir fal kaynağı seçmelisiniz: doğum bilgileri veya kahve fincanı görseli."},
            status_code=400,
        )

    image_analysis = analyze_uploaded_image(file if has_image else None)
    chart = build_astrology_report({
        "name": name,
        "birth_date": birth_date,
        "birth_time": birth_time,
        "city": city,
    })
    fortune = await generate_fortune(image_analysis, chart, tone=tone)

    return JSONResponse({
        "name": name,
        "has_birth_data": has_birth_data,
        "has_image": has_image,
        "image_analysis": image_analysis,
        "chart": chart,
        "fortune": fortune,
    })


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

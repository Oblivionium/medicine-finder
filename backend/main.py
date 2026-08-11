from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.search import search_medicines
from src.predict import (
    predict_price,
    predict_medicine_price
)
from src.alternatives import find_alternatives


BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


app = FastAPI(
    title="Medicine Price Finder",
    description="Medicine price prediction and alternative finder",
    version="1.0.0"
)


app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)


class PredictionRequest(BaseModel):
    dosage_form: str
    pack_size: float | None
    pack_unit: str | None
    primary_ingredient: str
    primary_strength: str | None
    therapeutic_class: str
    num_active_ingredients: int


@app.get("/")
def home():
    return FileResponse(
        FRONTEND_DIR / "index.html"
    )


@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.get("/api/search")
def search(query: str):
    return {
        "results": search_medicines(query)
    }

@app.post("/api/predict")
def predict(request: PredictionRequest):
    price = predict_price(
        dosage_form=request.dosage_form,
        pack_size=request.pack_size,
        pack_unit=request.pack_unit,
        primary_ingredient=request.primary_ingredient,
        primary_strength=request.primary_strength,
        therapeutic_class=request.therapeutic_class,
        num_active_ingredients=request.num_active_ingredients
    )

    return {
        "predicted_price": price
    }

@app.get("/api/predict/{medicine_name}")
def predict_medicine(medicine_name: str):
    price = predict_medicine_price(
        medicine_name
    )

    if price is None:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found"
        )

    return {
        "medicine": medicine_name,
        "predicted_price": price
    }

@app.get("/api/alternatives/{medicine_name}")
def alternatives(medicine_name: str):
    result = find_alternatives(medicine_name)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found"
        )

    return {
        "alternatives": result.to_dict(
            orient="records"
        )
    }
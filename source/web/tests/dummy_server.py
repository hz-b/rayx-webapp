"""Small FastAPI stand-in for the trace API during frontend development.

Run from the repository root with:
    uv run python source/web/tests/dummy_server.py
"""

from math import cos, exp, pi, sin

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI(title="Dummy RAYX API")

EnergyEV = Annotated[float, Field(ge=0, le=1000)]


class GraphSettings(BaseModel):
    eV: tuple[EnergyEV, EnergyEV]


class MirrorSettings(BaseModel):
    angle: float = Field(ge=-360, le=360)
    material: str = ""
    density: float = Field(default=-1, ge=-1, le=100)
    roughness: float = Field(default=1, ge=0, le=1)
    linearPol_0: float = Field(default=0, ge=-1, le=1)
    linearPol_45: float = Field(default=0, ge=-1, le=1)
    circularPol: float = Field(default=0, ge=-1, le=1)


class TraceRequest(BaseModel):
    graphSettings: GraphSettings
    mirrorSettings: MirrorSettings


class TraceResponse(BaseModel):
    message: str
    dataX: list[float]
    dataY: list[float]
    material: str
    density: float
    angle: float


# The frontend dev server runs on a separate port. Keep this permissive for
# local development; narrow the allowed origins if this server is deployed.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return "Hello from the dummy"


@app.get("/health")
def health() -> dict[str, str]:
    """Simple liveness check."""
    return {"status": "ok"}


@app.post("/api/reflectivity", response_model=TraceResponse)
def trace(request: TraceRequest) -> TraceResponse:
    """Return a deterministic mock reflectivity curve for the submitted settings."""
    energy_start, energy_end = request.graphSettings.eV
    if energy_start > energy_end:
        raise HTTPException(
            status_code=422, detail="Energy range start must not exceed end."
        )
    sample_count = 101
    if energy_start == energy_end:
        data_x = [energy_start]
    else:
        step = (energy_end - energy_start) / (sample_count - 1)
        data_x = [energy_start + index * step for index in range(sample_count)]

    angle_factor = abs(cos(request.mirrorSettings.angle * pi / 180))
    material_shift = sum(ord(char) for char in request.mirrorSettings.material) % 19
    density_factor = (
        1.0
        if request.mirrorSettings.density < 0
        else 1 / (1 + request.mirrorSettings.density * 0.01)
    )
    data_y = []
    for energy in data_x:
        center = (energy_start + energy_end) / 2 + material_shift
        envelope = 0.12 + 0.68 * exp(
            -(((energy - center) / max(1, (energy_end - energy_start) / 3)) ** 2)
        )
        interference = 0.08 * (sin(energy * 0.22) + 0.35 * sin(energy * 0.71))
        value = (envelope + interference) * angle_factor * density_factor
        data_y.append(max(0.0, min(1.0, value)))

    return TraceResponse(
        message="Dummy trace generated.",
        dataX=data_x,
        dataY=data_y,
        material=request.mirrorSettings.material or "Unknown",
        density=request.mirrorSettings.density,
        angle=request.mirrorSettings.angle,
    )

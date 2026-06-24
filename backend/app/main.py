from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure logging for LLM module
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s %(message)s")
logging.getLogger("xczs.llm").setLevel(logging.INFO)

from app.database import engine, Base
from app.models import teaching, knowledge, audit, user  # noqa: ensure all models loaded
from app.routers import courses, classes_, data_import
from app.routers.analysis_routes import router as analysis_router
from app.routers.comparison_routes import router as comparison_router
from app.routers.modes import router as modes_router
from app.routers.v2_routes import router as v2_router
from app.routers.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="学程智枢 API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(courses.router)
app.include_router(classes_.router)
app.include_router(data_import.router)
app.include_router(analysis_router)
app.include_router(comparison_router)
app.include_router(modes_router)
app.include_router(v2_router)
app.include_router(auth_router)


@app.get("/api/health")
def health():
    from app.services.llm import is_configured
    return {"status": "ok", "llm_configured": is_configured()}

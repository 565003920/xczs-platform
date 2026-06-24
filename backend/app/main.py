from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import courses, classes_, data_import
from app.routers.analysis_routes import router as analysis_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="学程智枢 API", version="1.0.0")

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


@app.get("/api/health")
def health():
    return {"status": "ok"}

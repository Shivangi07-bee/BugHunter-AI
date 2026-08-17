from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router
from .report_routes import router as report_router
from app.target_routes import router as target_router

app = FastAPI(
    title="BugHunter AI",
    version="1.0"
)

# -------------------------------
# CORS
# -------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(report_router)
app.include_router(target_router)

@app.get("/")
def home():
    return {
        "message": "BugHunter AI Running"
    }
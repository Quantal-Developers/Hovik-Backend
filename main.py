from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.batch_router import router as batch_router

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default port
        "http://localhost:3000",  # React default port
        "http://localhost:5174",  # Alternative Vite port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(batch_router, prefix="/api")

# Root route
@app.get("/")
def root():
    return {"message": "Batch Lookup API is running!"}

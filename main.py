from fastapi import FastAPI
from routers.batch_router import router as batch_router

app = FastAPI()

# Register Routers
app.include_router(batch_router, prefix="/api")

# Root route
@app.get("/")
def root():
    return {"message": "Batch Lookup API is running!"}

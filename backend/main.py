from fastapi import FastAPI

from routes.investigation_routes import router as investigation_router



app = FastAPI(
    title="RECOVERA API",
    version="1.0"
)



app.include_router(
    investigation_router
)



@app.get("/")
def home():

    return {
        "message":
        "RECOVERA Agent Running"
    }
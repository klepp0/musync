from fastapi import FastAPI

from .routes import tracks

app = FastAPI()

app.include_router(tracks.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the musync API"}

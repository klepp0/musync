import uvicorn
from fastapi import FastAPI

from .routes import playlists, sync, tracks

app = FastAPI()

app.include_router(tracks.router)
app.include_router(playlists.router)
app.include_router(sync.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the musync API"}


if __name__ == "__main__":
    uvicorn.run(router, host="0.0.0.0", port=8001)

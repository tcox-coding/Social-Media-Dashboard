from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import fastapi.security.api_key as api_key
import routes.apis.spotify as spotify_router
app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=['*'],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# Routes
app.include_router(spotify_router.router)

if __name__ == "__main__":
  import uvicorn
  uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
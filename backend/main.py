from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from serpapi import GoogleSearch
import os

app = FastAPI()

origins_raw = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
origins = [origin.strip().rstrip("/") for origin in origins_raw.split(",")]

# Allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SearchRequest(BaseModel):
    query: str


@app.get("/")
async def root():
    return {"message": "Server is running perfectly!"}


@app.post("/api/search")
async def search(request: SearchRequest):
    # API key should be in environment variables for security
    params = {
        "engine": "google",
        "q": request.query,
        "api_key": os.getenv("SERPAPI_KEY")
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    # Extract only organic results
    organic_results = results.get("organic_results", [])

    if not organic_results:
        raise HTTPException(status_code=404, detail="No results found")

    return {"results": organic_results}

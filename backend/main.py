from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from serpapi import GoogleSearch
import os

app = FastAPI()

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

# Allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Log incoming request origin to see what we are dealing with
    origin = request.headers.get("origin")
    print(f"Request from origin: {origin}")
    response = await call_next(request)
    return response


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

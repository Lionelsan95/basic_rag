from fastapi import FastAPI
from api.routes import crawl_routes, query_routes

app = FastAPI(title="RAG API", description="Crawling and Querying API", version="1.0.0")

# Include routes
app.include_router(crawl_routes.router, prefix="/api/v1")
app.include_router(query_routes.router, prefix="/api/v1")

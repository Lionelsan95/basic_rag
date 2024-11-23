from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from pipelines.rag_pipeline import crawl_and_index_pipeline, run_rag_pipeline
import logging

router = APIRouter()

# Input models
class ScrapeRequest(BaseModel):
    url: HttpUrl

class RAGRequest(BaseModel):
    user_name: str
    url: HttpUrl
    question: str

@router.post("/scrape")
async def scrape_and_index(input_data: ScrapeRequest):
    """
    Trigger the crawling and indexing process for a given URL.
    """
    try:
        response = crawl_and_index_pipeline(str(input_data.url))
        return {"message": response}
    except Exception as e:
        logging.error(f"Error during scraping: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/rag")
async def handle_rag_request(input_data: RAGRequest):
    """
    Handle RAG requests: query stored data and process the question.
    """
    try:
        response = run_rag_pipeline(str(input_data.url), input_data.question)
        return {
            "user_name": input_data.user_name,
            "question": input_data.question,
            "answer": response,
        }
    except Exception as e:
        logging.error(f"Error during RAG processing: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred during processing.")

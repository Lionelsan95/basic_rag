from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from pipelines.crawl_pipeline import (
    crawl_and_index_pipeline,
    async_crawl_and_index_pipeline,
)
from celery.result import AsyncResult

router = APIRouter()


class CrawlRequest(BaseModel):
    url: HttpUrl


@router.post("/crawl/sync")
async def trigger_sync_crawl(input_data: CrawlRequest):
    """
    Trigger a synchronous crawling and indexing process for a given URL.
    """
    try:
        # Directly call the synchronous crawl pipeline
        response = crawl_and_index_pipeline(str(input_data.url))
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/crawl/async")
async def trigger_async_crawl(input_data: CrawlRequest):
    """
    Trigger an asynchronous crawling and indexing process for a given URL.
    """
    try:
        # Start the asynchronous Celery task
        task = async_crawl_and_index_pipeline.delay(str(input_data.url))
        return {"message": "Crawling started.", "task_id": task.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/crawl/status/{task_id}")
async def get_crawl_status(task_id: str):
    """
    Check the status of a crawling task.
    """
    try:
        result = AsyncResult(task_id)
        if result.state == "PENDING":
            return {"status": "Pending"}
        elif result.state == "SUCCESS":
            return {"status": "Completed", "result": result.result}
        elif result.state == "FAILURE":
            return {"status": "Failed", "error": str(result.info)}
        else:
            return {"status": result.state}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

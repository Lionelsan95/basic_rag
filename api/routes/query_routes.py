from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pipelines.query_pipeline import run_query_pipeline

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
async def handle_query(input_data: QueryRequest):
    """
    Handle user questions by querying stored data and generating answers.
    """
    try:
        response = run_query_pipeline(input_data.question)
        return {"question": input_data.question, "answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

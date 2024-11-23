from services.chromadb_service import retrieve_context
import logging

def get_relevant_context(query: str) -> str:
    """
    Retrieve relevant context for a given query.
    
    Args:
        query (str): The query to search for.
    
    Returns:
        str: Retrieved context.
    """
    try:
        logging.info(f"Retrieving context for query: {query}")
        results = retrieve_context(query)
        context = " ".join([doc.page_content for doc in results])
        return context
    except Exception as e:
        logging.error(f"Error retrieving context: {e}", exc_info=True)
        raise

import logging
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from utils.common import format_retrieved_documents
from services.chromadb_service import get_relevant_documents
from langchain_core.output_parsers import StrOutputParser

# Initialize the LLM
llm = ChatOllama(model="llama3.2")


def query_llm_with_retriever(question: str) -> str:
    """
    Query the LLM by retrieving context from ChromaDB, formatting the retrieved documents,
    and passing the formatted context to the LLM.

    Args:
        question (str): The user's question.

    Returns:
        str: The LLM's response.
    """
    try:
        logging.info("Retrieving context for the LLM.")
        
        # Retrieve relevant documents from the retriever
        retrieved_docs = get_relevant_documents(question)
        if not retrieved_docs:
            logging.warning("No relevant documents retrieved. Returning default message.")
            return "I'm sorry, I couldn't find any relevant information for your question."

        # Format the retrieved documents
        formatted_context = format_retrieved_documents(retrieved_docs)

        # Create the prompt template
        logging.info("Preparing prompt for the LLM.")
        prompt_template = PromptTemplate.from_template(
            "You are an AI assistant. Use the following context to answer the question:\n\n"
            "Context: {context}\n\n"
            "Question: {question}\n\n"
            "Answer:"
        )

        # Create a RunnableSequence
        chain = prompt_template | llm | StrOutputParser()

        # Query the LLM with the formatted context and question
        response = chain.invoke({"context": formatted_context, "question": question})
        logging.info("LLM response received.")
        return response
    except Exception as e:
        logging.error(f"Error querying the LLM: {e}", exc_info=True)
        raise

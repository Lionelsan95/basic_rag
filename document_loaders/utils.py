# Convert loaded documents into strings by concatenating their content
# and ignoring metadata
def html_format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

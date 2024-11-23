
# Basic RAG (Retrieval-Augmented Generation) System

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline, enabling users to:
- **Crawl and index websites** into a vector database (ChromaDB).
- **Query the system** to retrieve context from the database and generate answers using a Large Language Model (LLM).

The project supports both **CLI** and **API** interactions. Crawling can be performed synchronously or asynchronously via a Celery-based background task system.

---

## Features

1. **Crawling and Indexing**:
   - Crawl web pages and store their content into ChromaDB.
   - Supports synchronous and asynchronous crawling.

2. **Querying**:
   - Retrieve indexed data from ChromaDB and use LLMs to answer user questions.

3. **Task Tracking**:
   - Check the status of asynchronous crawling tasks.

---

## Project Structure

```plaintext
basic_rag/
├── api/
│   ├── routes/
│   │   ├── crawl_routes.py        # Endpoints for crawling and status tracking
│   │   ├── query_routes.py        # Endpoints for querying
│   ├── app.py                     # FastAPI application setup
├── pipelines/
│   ├── crawl_pipeline.py          # Crawling and indexing pipeline (sync & async)
│   ├── query_pipeline.py          # Querying pipeline
├── services/
│   ├── chromadb_service.py        # Interactions with ChromaDB
│   ├── document_loader.py         # Web scraping logic
│   ├── redis_service.py           # URL tracking in Redis
├── utils/
│   ├── logging_config.py          # Logging configuration
│   ├── validators.py              # Input validators
├── main.py                        # CLI entry point
├── celery_app.py                  # Celery configuration
├── tests/                         # Unit tests
├── Pipfile                        # Dependency management
└── README.md                      # Project documentation
```

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/basic-rag.git
cd basic-rag
```

### 2. Install Dependencies
Ensure you have Python and `pipenv` installed. Then, run:
```bash
make install
```

### 3. Install Redis
Install Redis via your package manager or run it using Docker:
```bash
docker run -d --name redis -p 6379:6379 redis
```

---

## Usage

### 1. Start the API Server
Run the FastAPI server:
```bash
make run
```

Access the Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 2. Use the CLI
Start the CLI:
```bash
python main.py
```

Follow the interactive prompts to crawl websites or query the system.

### 3. Start Celery Workers
To enable asynchronous crawling, start a Celery worker:
```bash
make worker
```

---

## API Endpoints

### Crawling
#### Sync Crawling
- **POST** `/api/v1/crawl/sync`
- **Body**:
  ```json
  {
      "url": "https://example.com"
  }
  ```
- **Response**:
  ```json
  {
      "message": "URL 'https://example.com' successfully processed and indexed."
  }
  ```

#### Async Crawling
- **POST** `/api/v1/crawl/async`
- **Body**:
  ```json
  {
      "url": "https://example.com"
  }
  ```
- **Response**:
  ```json
  {
      "message": "Crawling started.",
      "task_id": "d13b3d28-e48e-11ec-9d64-0242ac120002"
  }
  ```

#### Check Crawling Status
- **GET** `/api/v1/crawl/status/{task_id}`
- **Response**:
  ```json
  {
      "status": "Pending"
  }
  ```

### Querying
- **POST** `/api/v1/query`
- **Body**:
  ```json
  {
      "question": "What is this website about?"
  }
  ```
- **Response**:
  ```json
  {
      "question": "What is this website about?",
      "answer": "This website provides information about ..."
  }
  ```

---

## Testing

### Run Unit Tests
Run the tests using `pytest`:
```bash
make test
```

### API Testing
Use tools like `curl`, **Postman**, or the **Swagger UI** for testing API endpoints.

---

## Makefile Usage

The project includes a `Makefile` to streamline common tasks:

1. **Install Dependencies**:
   ```bash
   make install
   ```

2. **Run the API Server**:
   ```bash
   make run
   ```

3. **Start a Celery Worker**:
   ```bash
   make worker
   ```

4. **Run Tests**:
   ```bash
   make test
   ```

5. **Lint the Code**:
   ```bash
   make lint
   ```

6. **Format the Code**:
   ```bash
   make format
   ```

7. **Clean Up**:
   ```bash
   make clean
   ```

---

## Future Enhancements

1. **Autoscaling Workers**:
   - Use Kubernetes to scale Celery workers dynamically.

2. **Task Expiry**:
   - Configure task timeouts to avoid stale or forgotten jobs.

3. **Enhanced Querying**:
   - Support multi-turn conversations with session context.

4. **UI Integration**:
   - Build a frontend for better user experience.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

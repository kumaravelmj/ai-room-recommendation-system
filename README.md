# AI Room Recommendation System

A FastAPI-based room recommendation backend that ingests room descriptions, creates semantic chunks and AWS Bedrock embeddings, stores them in PostgreSQL with pgvector, and retrieves relevant context to generate grounded recommendations with an AWS Bedrock language model.

## Features

- Knowledge-base ingestion from room text
- Semantic chunking and embedding generation
- PostgreSQL + pgvector similarity search
- Context-grounded LLM responses in JSON
- Layered controller, service, repository, and utility modules
- Environment-based configuration

## Requirements

- Python 3.10+
- PostgreSQL with the `vector` extension available
- AWS credentials with permission to invoke the selected Bedrock embedding and LLM models
- Model access enabled in the selected AWS region

## Local setup

Run commands from the repository root.

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a local `.env` file from the template:

   ```bash
   cp .env.example .env
   ```

   On Windows PowerShell, use `Copy-Item .env.example .env`.

4. Fill in the PostgreSQL settings and verify `EMBEDDING_MODEL_ID` and `LLM_MODEL_ID` for your AWS account. Do not commit `.env` or AWS credentials. The app uses the standard AWS credential chain when static keys are not configured.

5. Ensure PostgreSQL is running and the database in `DB_NAME` exists. The project creates its table at startup; the `vector` extension must be installed/enabled for pgvector to work.

6. Start the API from the repository root:

   ```bash
   cd src
   python app.py
   ```

   Or from the root:

   ```bash
   uvicorn app:app --app-dir src --host 0.0.0.0 --port 3000
   ```

7. Open `http://localhost:3000/docs`.

## API endpoints

- `POST /training/api/create-knowledgebase` — ingests text and stores semantic chunks and embeddings.
- `POST /training/api/search-room` — embeds a query, retrieves relevant context, and asks the configured Bedrock model for a grounded answer.

Example ingestion request:

```json
{
  "content": "Room A seats 10 people and includes a projector and whiteboard."
}
```

Example search request:

```json
{
  "query": "Find a room for 10 people with a projector."
}
```

## Important limitations and security

- This is a demonstration project, not a booking or availability system. It recommends only from information supplied to its knowledge base.
- Similarity thresholds and embedding dimensions should be validated against your actual corpus and model. The database vector column is currently configured for 1024 dimensions; use an embedding model that produces that dimension or update the schema and migrate the database.
- Verify the selected Bedrock LLM's request/response format. Bedrock model APIs can differ by provider and model.
- The API does not implement authentication or authorization. Add these before exposing it publicly.
- Use real AWS credentials only in local environment variables, an AWS profile, or an IAM role. Never commit credentials.
- Database table creation at startup is suitable for a demo; use controlled migrations for production.

# Olance Agent API

This project provides a Flask-based API for managing tasks, task runs, and logs, with data stored in Google Cloud Datastore.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up your `.env` file with required environment variables (e.g., `GOOGLE_APPLICATION_CREDENTIALS`).
3. Start the Flask app:
   ```bash
   python main.py
   ```

## API Endpoints & Example Usage

### Register a Task

Creates a new task in Datastore.

```bash
curl -X POST http://localhost:3000/api/task/register \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "task123",
    "description": "Example task",
    "url": "https://example.com"
  }'
```

### Get Task Details (with runs and logs)

Retrieves a task and its associated runs and logs.

```bash
curl -X GET http://localhost:3000/api/task/task123
```

## Environment Variables

- `GOOGLE_APPLICATION_CREDENTIALS`: Path to your Google Cloud service account JSON file.
- Any other variables required for your environment can be set in `.env`.

## Notes

- TaskRun and TaskLog entities must be created via Datastore or additional endpoints (not shown here).
- All API responses are in JSON format.

---

For further details, see the code in `api/routes/task.py` and `api/models.py`.

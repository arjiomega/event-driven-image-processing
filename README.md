# Event-Driven Image Processing Service

An image processing pipeline that reacts to file uploads via object storage events rather than direct API calls — upload an image, and a chain of decoupled services picks it up, processes it, and makes the result available, with no service directly calling another.

## Why event-driven?

The simplest version of this project would have the backend call .delay() on a Celery task right after the upload completes. That works fine at this traffic scale — and it would have been less code.

Instead, this project triggers processing from a MinIO bucket notification: the client uploads directly to object storage via a presigned URL, MinIO detects the new object and publishes an AMQP event, and a separate consumer service turns that event into a Celery task. The backend that issued the upload URL is never in the loop again after that point.

This was a deliberate choice to practice a decoupled, storage-triggered architecture — not because it was the "correct" choice for this specific traffic pattern.


## Architecture
![Architecture Image](./Event-Driven%20Image%20Processing%20Service%20Architecture.png)

## Running the project

**Full stack, including the containerized frontend:**
```bash
docker compose --profile include_frontend up -d --build
```

**Backend services only** — if you'd rather run the frontend yourself (e.g. `npm run dev` for hot reload during development), add the required env var to `.env` first, then:
```bash
docker compose up -d --build
```

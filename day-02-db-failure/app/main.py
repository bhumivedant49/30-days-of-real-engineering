import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pymongo.errors import ConnectionFailure

from app.database import client, tasks_collection
from app.models import Task

app = FastAPI()
logger = logging.getLogger("uvicorn.error")


@app.exception_handler(ConnectionFailure)
async def db_unavailable_handler(request: Request, exc: ConnectionFailure):
    logger.error(
        "MongoDB unavailable on %s %s (%s)",
        request.method, request.url.path, type(exc).__name__,
    )
    return JSONResponse(
        status_code=503,
        content={"detail": "Database temporarily unavailable"},
        headers={"Retry-After": "5"},
    )


@app.get("/")
def root():
    return {"message": "Day 2 API is running"}


@app.get("/health")
def health():
    try:
        client.admin.command("ping")
        return {"status": "ok", "database": "up"}
    except ConnectionFailure:
        return JSONResponse(
            status_code=503,
            content={"status": "degraded", "database": "down"},
        )


@app.post("/tasks")
def create_task(task: Task):
    task_data = task.model_dump()

    result = tasks_collection.insert_one(task_data)

    return {
        "message": "Task created successfully",
        "task_id": str(result.inserted_id)
    }


@app.get("/tasks")
def get_tasks():
    tasks = list(tasks_collection.find({}, {"_id": 0}))  # Exclude the _id field from the response

    return tasksfrom fastapi import FastAPI
from app.database import tasks_collection
from app.models import Task

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Day 1 API is running"}


@app.post("/tasks")
def create_task(task: Task):
    task_data = task.model_dump()

    result = tasks_collection.insert_one(task_data)

    return {
        "message": "Task created successfully",
        "task_id": str(result.inserted_id)
    }

@app.get("/tasks")
def get_tasks():
    tasks = list(tasks_collection.find({}, {"_id": 0}))  # Exclude the _id field from the response
    
    return tasks
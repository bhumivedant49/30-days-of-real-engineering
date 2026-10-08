from fastapi import FastAPI
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
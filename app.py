from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import psycopg
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found. Check your .env file.")

app = FastAPI()


# Database connection
def get_db():
    return psycopg.connect(os.getenv("DATABASE_URL"))


# Create the tasks table
def create_table():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                task TEXT NOT NULL,
                completed INTEGER DEFAULT 0
            )
        """)


create_table()


# Frontend routes
@app.get("/")
def home():
    return FileResponse("index.html")


@app.get("/style.css")
def style():
    return FileResponse("style.css")


@app.get("/script.js")
def script():
    return FileResponse("script.js")


# Get all tasks
@app.get("/tasks")
def get_tasks():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT id, task, completed FROM tasks ORDER BY id"
        ).fetchall()

    return {
        "tasks": [
            {"id": row[0], "task": row[1], "completed": row[2]}
            for row in rows
        ]
    }


# Request model for adding a task
class Task(BaseModel):
    task: str


# Add a task
@app.post("/tasks")
def add_task(task: Task):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO tasks (task) VALUES (%s)",
            (task.task,)
        )

    return {"message": "Task added successfully"}


# Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    with get_db() as conn:
        conn.execute(
            "DELETE FROM tasks WHERE id = %s",
            (task_id,)
        )

    return {"message": "Task deleted successfully"}


# Request model for updating task status
class TaskStatus(BaseModel):
    completed: int


# Update task completion status
@app.put("/tasks/{task_id}")
def complete_task(task_id: int, status: TaskStatus):
    with get_db() as conn:
        conn.execute(
            "UPDATE tasks SET completed = %s WHERE id = %s",
            (status.completed, task_id)
        )

    return {"message": "Task status updated successfully"}
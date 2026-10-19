from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from fastapi.responses import FileResponse

app = FastAPI()


def get_db():
    conn = sqlite3.connect("database.db")
    return conn


def create_table():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


create_table()


@app.get("/")
def home():
    return FileResponse("index.html")


@app.get("/style.css")
def style():
    return FileResponse("style.css")


@app.get("/script.js")
def script():
    return FileResponse("script.js")


@app.get("/tasks")
def get_tasks():
    conn = get_db()

    cursor = conn.execute("SELECT id, task, completed FROM tasks")
    rows = cursor.fetchall()

    conn.close()

    return {
        "tasks": [
            {
                "id": row[0],
                "task": row[1],
                "completed": row[2]
            }
            for row in rows
        ]
    }


class Task(BaseModel):
    task: str


@app.post("/tasks")
def add_task(task: Task):
    conn = get_db()

    conn.execute(
        "INSERT INTO tasks (task) VALUES (?)",
        (task.task,)
    )

    conn.commit()
    conn.close()

    return {"message": "Task added successfully"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_db()

    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()

    return {"message": "Task deleted successfully"}


class TaskStatus(BaseModel):
    completed: int


@app.put("/tasks/{task_id}")
def complete_task(task_id: int, status: TaskStatus):
    conn = get_db()

    conn.execute(
        "UPDATE tasks SET completed = ? WHERE id = ?",
        (status.completed, task_id)
    )

    conn.commit()
    conn.close()

    return {"message": "Task status updated successfully"}
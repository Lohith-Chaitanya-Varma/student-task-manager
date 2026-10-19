const taskInput = document.getElementById("taskInput");
const addTaskBtn = document.getElementById("addTaskBtn");
const taskList = document.getElementById("taskList");

// ADD TASK
addTaskBtn.addEventListener("click", async function () {
    const taskText = taskInput.value.trim();

    if (taskText === "") {
        alert("Please enter a task!");
        return;
    }

    const response = await fetch("/tasks", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ task: taskText })
    });

    const data = await response.json();
    console.log("POST response:", data);

    taskInput.value = "";

    await loadTasks();
});

// LOAD TASKS
async function loadTasks() {
    const response = await fetch("/tasks");
    const data = await response.json();

    console.log("GET response:", data);

    // Clear the old list to prevent duplicate tasks
    taskList.innerHTML = "";

    data.tasks.forEach(function (task) {
        taskList.innerHTML += `
            <p>
                <input
                    type="checkbox"
                    ${task.completed === 1 ? "checked" : ""}
                    onchange="completeTask(${task.id}, this.checked)"
                >
                <span style="${task.completed === 1 ? "text-decoration: line-through;" : ""}">
                    ${task.task}
                </span>
                <button onclick="deleteTask(${task.id})">Delete</button>
            </p>
        `;
    });
}

// DELETE TASK
async function deleteTask(taskId) {
    await fetch(`/tasks/${taskId}`, {
        method: "DELETE"
    });

    await loadTasks();
}

// MARK TASK AS COMPLETED OR INCOMPLETE
async function completeTask(taskId, isCompleted) {
    const response = await fetch(`/tasks/${taskId}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            completed: isCompleted ? 1 : 0
        })
    });

    const data = await response.json();
    console.log("Task status updated:", data);

    await loadTasks();
}

// LOAD TASKS WHEN THE PAGE OPENS
loadTasks();
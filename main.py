from fastapi import FastAPI, HTTPException

app = FastAPI()

# "מסד נתונים" בזיכרון
tasks = []
counter = 1

@app.get("/tasks")
def get_tasks(priority=None):
    if priority is None:
        return tasks
    if not str(priority).isdigit():
        raise HTTPException(status_code=400, detail="Error - priority must be an integer number")
    
    priority = int(priority)
    if priority not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="Error - priority must be an integer between 1 and 3")

    new_tasks = []
    for task in tasks:
        if task["priority"] == priority:
            new_tasks.append(task)
    
    return new_tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks")
def add_task(task: dict):
    global counter
    user_priority = task.get("priority")
    if user_priority is None:
        user_priority = 2
    else:
        if not type(user_priority) == int or user_priority not in [1, 2, 3]:
            raise HTTPException (status_code=400,detail=" Error - priority must be an integer between 1 and 3")
    new_task = {
        "id": counter,
        "title": task.get("title"),
        "owner": task.get("owner"),
        "priority": user_priority
    }
    tasks.append(new_task)
    counter += 1
    return new_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
from fastapi import FastAPI, HTTPException

app = FastAPI()

todos = {}
id_counter = 1

@app.get("/todos")
def get_todos():
    return [{"id": str(id), "content": content} for id, content in todos.items()]

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"id": todo_id, "content": todos[todo_id]}

@app.post("/todos")
def create_todo(input: dict):
    global id_counter
    todo_id = id_counter
    todos[todo_id] = input.get("content", "")
    id_counter += 1
    return {"id": todo_id, "content": todos[todo_id]}

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, input: dict):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos[todo_id] = input.get("content", "")
    return {"id": todo_id, "content": todos[todo_id]}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[todo_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
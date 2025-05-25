from contextlib import asynccontextmanager
from typing import List, Annotated, AsyncGenerator

from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select

from dto import TodoCreate, TodoResponse, TodoUpdate

sqlite_file_name = 'data.db'
connect_url = f'sqlite:///{sqlite_file_name}'
engine = create_engine(connect_url, connect_args={"check_same_thread": False})

class TodoModel(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    content: str

def get_session():
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    SQLModel.metadata.create_all(engine)
    yield

SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI(lifespan=lifespan)

@app.get("/todos", response_model=List[TodoResponse])
def get_todos(session: SessionDep):
    statement = select(TodoModel)
    todos = session.exec(statement).all()
    return todos

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, session: SessionDep):
    statement = select(TodoModel).where(TodoModel.id == todo_id)
    todo = session.exec(statement).first()

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo

@app.post("/todos", response_model=TodoResponse)
def create_todo(dto: TodoCreate, session: SessionDep):
    new_todo = TodoModel(content=dto.content)
    session.add(new_todo)
    session.commit()
    return new_todo

@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, dto: TodoUpdate, session: SessionDep):
    statement = select(TodoModel).where(TodoModel.id == todo_id)
    todo = session.exec(statement).first()

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo.content = dto.content

    session.add(todo)
    session.commit()
    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, session: SessionDep):
    statement = select(TodoModel).where(TodoModel.id == todo_id)
    todo = session.exec(statement).first()

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    session.delete(todo)
    session.commit()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
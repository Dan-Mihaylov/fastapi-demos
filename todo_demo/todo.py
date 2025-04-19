from datetime import datetime, date, timezone
from typing import Any, Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from uuid import uuid4
import uvicorn


app = FastAPI()
todos = {}


class Todo(BaseModel):
    id: str = Field(default_factory=lambda: uuid4())
    title: str = Field(...)
    date: date
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed: bool = False


    @field_validator('date')
    @classmethod
    def date_must_be_greater_than_now(cls, value: Any):
        now = datetime.now().date()
        if value < now:
            raise ValueError("Date cannot be less than now")
        return value


class UpdateTodo(BaseModel):
    completed: bool


todo = Todo(
    id="f145f67a-2c4d-4f0f-bc49-ad074ef73cf1",
    title="Wash the dishes",
    date=date.today(),
    created_at=datetime.now(timezone.utc),
    completed=False
)
todos[todo.id] = todo


@app.get('/todos')
def get_todos(
    sort_by: Literal['title', 'date', 'created_at'] = 'created_at',
    descending: bool = False
):

    sorted_todos = sorted(todos.items(), key=lambda item: getattr(item[1], sort_by), reverse=descending)
    return sorted_todos


@app.get('/todos/{_id}')
def get_todo(_id: str):
    not_found_message = {'msg': 'Todo with that ID does not exist'}

    if _id in todos:
        return todos[_id]

    return not_found_message


@app.post('/todos')
def create_todo(todo: Todo):
    new_id = uuid4()
    todo.id = new_id
    todos[str(new_id)] = todo
    return todo


@app.put('/todos/{_id}')
def update_todo(_id: str, update_data: UpdateTodo):
    not_found_message = {'msg': 'Todo with that ID does not exist'}

    if _id in todos:
        todos[_id].completed = update_data.completed
        return todos[_id]

    return not_found_message


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)


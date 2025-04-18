from datetime import datetime, date
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator, validator
from uuid import uuid4
import uvicorn


app = FastAPI()
todos = []


class Todo(BaseModel):
    id: str = Field(default_factory=lambda: uuid4())
    title: str = Field(...)
    date: date
    completed: bool = False


    @field_validator('date')
    @classmethod
    def date_must_be_greater_than_now(cls, value: Any):
        now = datetime.now().date()
        if value < now:
            raise ValueError("Date cannot be less than now")
        return value


@app.get('/todos')
def get_todos():
    return todos


@app.post('/todos')
def create_todo(todo: Todo):
    new_id = uuid4()
    todo.id = new_id
    todos.append(todo)
    return todo


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)


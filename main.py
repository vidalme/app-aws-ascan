import sys
def handler(event, context):
    return 'Hello from AWS Lambda using Python' + sys.version + '!'
    
from enum import IntEnum
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from mangum import Mangum
import boto3
from boto3.dynamodb.conditions import Key
import os

app = FastAPI()
handler = Mangum(app, lifespan="off")
class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1

class TodoBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=50, description="Título da tarefa")
    done: bool = Field(default=False, description="Tarefa concluída ou não")
    priority: Priority = Field(default=Priority.LOW, description="Prioridade da tarefa")

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int = Field(..., description="Identificador da tarefa")

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=50, description="Título da tarefa")
    done: Optional[bool] = Field(None, description="Tarefa concluída ou não")
    priority: Optional[Priority] = Field(None, description="Prioridade da tarefa")


all_todos = [
    Todo(id=1, title="Fazer compras", done=False, priority=Priority.HIGH),
    Todo(id=2, title="Estudar FastAPI", done=False, priority=Priority.MEDIUM),
    Todo(id=3, title="Estudar Python", done=False, priority=Priority.MEDIUM),
    Todo(id=4, title="Estudar Django", done=False, priority=Priority.HIGH),
    Todo(id=5, title="Estudar Flask", done=False, priority=Priority.LOW),
]

dynamodb = boto3.resource("dynamodb")

#DYNAMO_TABLE_NAME environment variable set by lambda IaC
table = dynamodb.Table(os.environ["DYNAMO_TABLE_NAME"])

@app.get("/" , response_model=List[Todo])
def read_root():
    response = table.scan()
    return response["Items"]


@app.get('/todos/{id}', response_model=Todo)
def get_todo( id: int ):
    response = table.get_item(Key={"id": id})
    if "Item" in response:
        return {
            "id": response["Item"]["id"],
            "title": response["Item"]["title"],
            "done": response["Item"]["done"],
            "priority": response["Item"]["priority"]
        }
    else:
        return "Task not found"

# function that loops through all the todos and returns the todo with the highest id
def get_highest_id():
    all_todos = table.scan()["Items"]
    highest = 0
    for todo in all_todos:
        if todo["id"] > highest:
            highest = todo["id"]
    return highest+1 


@app.post('/todos', response_model=List[Todo])
def create_todo(todo: TodoCreate):

    new_todo = Todo(
        id=get_highest_id(),
        title=todo.title,
        done=todo.done,
        priority=todo.priority
    )

    table.put_item(Item=new_todo.model_dump())
    return table.scan()["Items"]

@app.put('/todos/{id}', response_model=Todo)
def update_todo( id: int, update_todo: TodoUpdate):

    response = table.get_item(Key={"id": id})

    response["id"] = id

    if update_todo.title is not None:
        response["title"] = update_todo.title
    if update_todo.done is not None:
        response["done"] = update_todo.done
    if update_todo.priority is not None:
        response["priority"] = update_todo.priority

    table.put_item(Item=response)
    return response
        
    # raise HTTPException(status_code=404, detail="Todo não encontrado")

@app.delete('/todos/{id}')
def delete_todo( id: int ):
    table.delete_item(Key={"id": id})
    return table.scan()["Items"]
    # raise HTTPException(status_code=404, detail="Todo não encontrado")


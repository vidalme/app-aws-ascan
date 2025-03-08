import sys
def handler(event, context):
    return 'Hello from AWS Lambda using Python' + sys.version + '!'
    
# from enum import IntEnum
# from typing import Optional, List
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, Field
# from mangum import Mangum
# import boto3
# from boto3.dynamodb.conditions import Key

# api = FastAPI()
# handler = Mangum(api)

# class Priority(IntEnum):
#     LOW = 3
#     MEDIUM = 2
#     HIGH = 1

# class TodoBase(BaseModel):
#     title: str = Field(..., min_length=3, max_length=50, description="Título da tarefa")
#     done: bool = Field(default=False, description="Tarefa concluída ou não")
#     priority: Priority = Field(default=Priority.LOW, description="Prioridade da tarefa")

# class TodoCreate(TodoBase):
#     pass

# class Todo(TodoBase):
#     id: int = Field(..., description="Identificador da tarefa")

# class TodoUpdate(BaseModel):
#     title: Optional[str] = Field(None, min_length=3, max_length=50, description="Título da tarefa")
#     done: Optional[bool] = Field(None, description="Tarefa concluída ou não")
#     priority: Optional[Priority] = Field(None, description="Prioridade da tarefa")

# all_todos = [
#     Todo(id=1, title="Fazer compras", done=False, priority=Priority.HIGH),
#     Todo(id=2, title="Estudar FastAPI", done=False, priority=Priority.MEDIUM),
#     Todo(id=3, title="Estudar Python", done=False, priority=Priority.MEDIUM),
#     Todo(id=4, title="Estudar Django", done=False, priority=Priority.HIGH),
#     Todo(id=5, title="Estudar Flask", done=False, priority=Priority.LOW),
# ]


# @api.get("/")
# def index():
#     return { "message": "Olá ascanianos"}

# @api.get('/todos',response_model=List[Todo])
# def get_todos():
#     return all_todos

# @api.get('/todos/{todo_id}', response_model=Todo)
# def get_todo( todo_id: int ):
#     for todo in all_todos:
#         if todo.todo_id == todo_id:
#             return todo
        
# @api.post('/todos', response_model=List[Todo])
# def create_todo(todo: TodoCreate):

#     new_todo_id = max( todo.id for todo in all_todos ) + 1 

#     new_todo = Todo(
#         id=new_todo_id,
#         title=todo.title,
#         done=todo.done,
#         priority=todo.priority
#     )

#     all_todos.append(new_todo)
#     return all_todos

# @api.put('/todos/{id}', response_model=Todo)
# def update_todo( id: int, update_todo: TodoUpdate):
#     for todo in all_todos:
#         if todo.id == id:
#             if update_todo.title is not None:
#                 todo.title = update_todo.title
#             if update_todo.done is not None:
#                 todo.done = update_todo.done
#             if update_todo.priority is not None:
#                 todo.priority = update_todo.priority
#             return todo
#     raise HTTPException(status_code=404, detail="Todo não encontrado")

# @api.delete('/todos/{id}')
# def delete_todo( id: int ):
#     for todo in all_todos:
#         if todo.id == id:
#             all_todos.remove(todo)
#             return all_todos
#     raise HTTPException(status_code=404, detail="Todo não encontrado")
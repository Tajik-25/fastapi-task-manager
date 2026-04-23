from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field,field_validator,model_validator
from typing import Optional
app = FastAPI()
tasks = []
current_id = 1
class Task(BaseModel):
    title: str
    description:Optional[str] = None
    priority:int = Field(gt=0)
    completed:bool= False
    due_days:Optional[int]= None
    @field_validator("title")
    def title_len(cls,value):
        if len(value) < 3:
            raise ValueError("title cant be less than 3 letters")
        return value
    @field_validator("priority")
    def check_priority(cls,value):
        if value > 5:
            raise ValueError("this task is not priortised now")
        return value
    @model_validator(mode="after")
    def check_due_days(self):
        if self.completed and self.due_days not in (0,None):
            raise ValueError("task cannot have due dates once completed")
        return self
class TaskResponse(BaseModel):
    id:int
    title:str
    priority:int
    completed:bool
    status:str
class Update(BaseModel):
    title:Optional[str]= None
    description:Optional[str] = None
    priority:Optional[int] = None
    completed:Optional[bool]=None
    due_days:Optional[int] = None
@app.post("/tasks",response_model=TaskResponse,status_code=201)
def create_task(task:Task):
    global current_id
    task_data = task.dict()
    status = "done" if task_data["completed"] else "pending"
    task_data["status"] = status
    task_data["id"] = current_id
    current_id += 1
    tasks.append(task_data)
    return task_data
@app.get("/tasks",response_model=list[TaskResponse])
def all_tasks():
    return tasks
@app.get("/tasks/{task_id}",response_model=TaskResponse)
def get_task(task_id:int):
    for task in tasks:
        if task["id"] == task_id:
            status = "done" if task["completed"] else "pending"
            task["status"] = status
            return task
    raise HTTPException(status_code=404,detail="task not found")
@app.put("/tasks/{task_id}",response_model=TaskResponse)
def update_task(task_id:int,update:Update):
    for task in tasks:
        if task["id"] == task_id:
            if update.title is not None:
                task["title"] = update.title
            if update.description is not None:
                task["description"] = update.description
            if update.priority is not None:
                task["priority"] = update.priority
            if update.completed is not None:
                task["completed"] = update.completed
            if update.due_days is not None:
                task["due_days"] = update.due_days
            status = "done" if task["completed"] else "pending"
            task["status"] = status
            if task["completed"] and task["due_days"] > 0:
                raise ValueError("due days cant be greater then 0 if task completed")
            return task
        raise HTTPException(status_code=404,detail="task not found")
@app.delete("/tasks/{task_id}")
def delete_task(task_id:int):
    for i,task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return {"message":"task deleted"}
    raise HTTPException(status_code=404,detail="task not found")
    
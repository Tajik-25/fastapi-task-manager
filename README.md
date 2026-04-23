# FastAPI Task Manager API
A REST API for managing tasks built with fastapi and pydnatic
## Features 
-Full CRUD operations for task management
-pydantic validation with Field,field validators and Model Validators
-Response models for clean output
-Proper HTTP status codes and error handling
-Task status tracking (done/pending)
-Due dates validation logic
## Endpoints
-POST /tasks - create a task
-GET /tasks -get all tasks
-GET /tasks/{id} - get single task
-PUT /tasks/{id} - update a task
-DELETE /tasks/{id} - delete a task
## Tech stacks
-python
-FastAPI
-Pydantic
## How to run
1.Clone the repo
2.Install dependencies:pip install -r requirements.txt
3.Run: uvicorn main:app --reload
4.Open: http: //127.0.0.1:8000/docs
## In progress
-PostgreSQL database integration
-JWT Authentication

from fastapi import FastAPI,Query,HTTPException,Path
from service.task import get_tasks,search_similar_tasks,priority_listing,add_task,delete_task,change_task
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For local testing; narrow down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from schema.task import Task,TaskUpdate
from datetime import datetime
@app.get("/")
def root():
    return {"message":"Welcome to the TODO Website"}




@app.get("/tasks/search")
def list_tasks(name : str = Query(...,min_length=1,max_length=40,description="Keyword of the tasks for searching")):
    return search_similar_tasks(name)

@app.get("/tasks/{id}")
def get_tasks_based_of_id(id : int):
    return get_tasks(id)

@app.get("/tasks")
def priority_based_listing(priority : str = Query(...,min_length=3,max_length=6,description="High/Low/Medium priority")):
    return priority_listing(priority)

@app.post("/tasks",status_code=201)
def create_task(task : Task ):
    try:
        task_data=task.model_dump(mode="json")
        task_data["created_at"] = datetime.utcnow().isoformat()
        return add_task(task_data)
    except ValueError as e:
        raise HTTPException(status_code=404,detail="Error at Create task")


@app.delete("/tasks/{task_id}")
def remove_task(task_id : int = Path(...,gt=0)):
    try:
        return delete_task(task_id)

    except:
        return {"error in deletion"}

@app.put("/tasks/{task_id}")
def update_task(task_id : int , update_data : TaskUpdate ) :
    try:
        return change_task(task_id,update_data.model_dump(mode="json",exclude_unset=True))
    except ValueError:
        raise HTTPException(status_code=400,detail="Required task to update not found")
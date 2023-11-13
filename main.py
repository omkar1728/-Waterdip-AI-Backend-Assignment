from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from models import Task
app = FastAPI()

tasks_db = []
task_id_counter = 1


@app.post("/v1/tasks/")
async def create_task(req: Request):
    global task_id_counter
    global tasks_db
    data = await req.json()
    new_title = data.get("title")
    new_task = Task(title= new_title, id = task_id_counter)
    task_id_counter += 1
    tasks_db.append(new_task)
    return JSONResponse(content= {"id" : new_task.id}, status_code= 201)


@app.get("/v1/tasks/")
def list_tasks():
    
    return {"tasks" : tasks_db}



@app.get("/v1/tasks/{task_id}")
async def get_task(task_id: int):
    task = None
    for i in tasks_db:
        if i.id == task_id:
            task = i
    if task is None:
        return JSONResponse(content= {"error" : "There is no task at that id"}, status_code= 404)
    return JSONResponse(content= task.dict(), status_code= 200)


@app.delete("/v1/tasks/{task_id}")
async def delete_task(task_id: int):
    for i in tasks_db:
        if i.id == task_id:
            tasks_db.remove(i)
    return JSONResponse(content= None,  status_code= 204)


@app.put("/v1/tasks/{task_id}")
async def edit_task(req: Request, task_id : int):
    data = await req.json()
    new_title = data.get("title")
    new_completion = data.get("is_completed")
    task = None
    for i in tasks_db:
        if i.id == task_id:
            i.title = new_title
            i.is_completed = new_completion
            task = i
            break
    if task == None:
        return JSONResponse(content= {"error": "There is no task at that id"},  status_code= 404)

    return JSONResponse(content= None,  status_code= 204)


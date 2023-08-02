from fastapi import Body, FastAPI, Form, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from worker import create_task
from celery.result import AsyncResult


app = FastAPI()


@app.post("/create_tasks", status_code=201)
def run_task(payload = Body(...)):
    url = payload["url"]
    
    #refersh_ip = payload["refersh_ip"]
    
    print("url", url)
    task = create_task.delay(url=url)
    return JSONResponse({"task_id": task.id})

@app.get("/results/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id)
    
    #consultar a redis
    

    result = {
        "task_id": task_id,
        "task_status": str(task_result.status),
        "task_result": str(task_result.result)
    }
    print(result)
    return JSONResponse(result)

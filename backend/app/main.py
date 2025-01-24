import logging
from typing import Union
from uuid import uuid4
from fastapi import APIRouter, FastAPI, HTTPException, Request, WebSocket
from fastapi.responses import HTMLResponse, JSONResponse
from app.models import CreateTask, Task, UpdateTask
import app.db as db

app = FastAPI()
api_router = APIRouter()
logger = logging.getLogger("uvicorn.error")

tasks_db = []


@app.exception_handler(Exception)
def handle_generic_exception(_: Request, exception: Exception) -> JSONResponse:
    """Handle generic exception"""
    logger.error("An error occurred", exc_info=exception)
    return JSONResponse({"detail": str(exception)}, 500)


@api_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await db.watch_tasks_collection(websocket)
    except Exception as e:
        logger.exception("Error in WebSocket connection: %s", e)
    finally:
        await websocket.close()


@api_router.post("/tasks/", response_model=Task)
async def create_task(task: CreateTask):
    created_task = await db.create_task(task)
    logger.info(f"Task created: {created_task.id}")
    return created_task


@api_router.get("/tasks/", response_model=list[Task])
async def read_tasks():
    tasks = await db.list_tasks()
    return tasks


@api_router.put(
    "/tasks/",
    response_model=Task,
    responses={404: {"description": "Task not found or has a conflict version"}},
)
async def update_task(task: UpdateTask):
    try:
        updated_task = await db.update_task(task=task)
        logger.info(f"Task updated: {updated_task.id}")
        return updated_task
    except db.OptimisticLockException:
        logger.warning(f"Optimistic lock exception for task: {task.id}")
        raise HTTPException(
            status_code=404,
            detail="Task not found due to optimistic lock failure, update the page",
        )


@api_router.delete(
    "/tasks/{task_id}",
    response_model=dict,
    responses={404: {"description": "Task not found"}},
)
async def delete_task(task_id: str):
    success = await db.delete_task(task_id=task_id)
    if not success:
        logger.warning(f"Task not found: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")
    logger.info(f"Task deleted: {task_id}")
    return {"detail": "Task deleted successfully"}


app.include_router(api_router, prefix="/api")

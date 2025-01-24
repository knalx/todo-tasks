from datetime import datetime, timezone
import logging
from bson import ObjectId
from typing import List, Optional
from fastapi import WebSocket
from pydantic import BaseModel

from dotenv import load_dotenv
from pymongo import ReturnDocument

from app.db_config import MongoDBClient
from app.models import CreateTask, Task, UpdateTask

load_dotenv()
logger = logging.getLogger("uvicorn.error")

mongo_client = MongoDBClient()
tasks_collection = mongo_client.get_collection("tasks")


class OptimisticLockException(Exception):
    """Exception raised for optimistic lock conflicts."""

    def __init__(self, message="Optimistic lock conflict detected."):
        self.message = message
        super().__init__(self.message)


async def watch_tasks_collection(websocket: WebSocket):
    async with tasks_collection.watch(full_document="updateLookup") as change_stream:
        async for change in change_stream:
            operationType = change["operationType"]
            logger.info(f"Send msg to Websocket: {operationType}")
            await websocket.send_json(operationType)


async def create_task(task: CreateTask) -> Task:
    task_data = task.model_dump(exclude_unset=True, exclude={"id"})
    task_data["version"] = 1

    result = await tasks_collection.insert_one(task_data)
    created_task = await tasks_collection.find_one({"_id": result.inserted_id})
    return Task(**created_task)


async def list_tasks() -> List[Task]:
    # todo: think about pagination
    tasks = await tasks_collection.find().to_list(length=100)
    return [Task(**task) for task in tasks]


async def update_task(task: UpdateTask) -> Optional[Task]:
    result = await tasks_collection.find_one_and_update(
        {"_id": ObjectId(task.id), "version": task.version},
        {
            "$set": task.model_dump(exclude_unset=True, exclude={"version"}),
            "$inc": {"version": 1},
        },
        return_document=ReturnDocument.AFTER,
    )

    if result is None:
        raise OptimisticLockException(
            "Update conflict detected. Please refresh your data."
        )
    else:
        return Task(**result)


async def delete_task(task_id: str) -> bool:
    result = await tasks_collection.delete_one({"_id": ObjectId(task_id)})
    return result.deleted_count > 0


async def get_task(task_id: str) -> Optional[Task]:
    task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
    return Task(**task) if task else None

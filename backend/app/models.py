from datetime import datetime, timezone

from typing import Optional, Union
from pydantic import BaseModel, model_validator


class CreateTask(BaseModel):
    title: str
    description: str
    completed: bool = False


class Task(CreateTask):
    id: str
    version: int = 1

    @model_validator(mode="before")
    @classmethod
    def validate_id(cls, data: dict):
        """Convert '_id' field to 'id' if it exists, otherwise check for 'id'"""
        if "_id" in data:
            data["id"] = str(data["_id"])
            del data["_id"]
        elif "id" not in data:
            raise ValueError("'_id' or 'id' field is required")
        return data


class UpdateTask(Task):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = False

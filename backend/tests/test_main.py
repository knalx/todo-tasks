import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

api_prefix = "/api/tasks/"


def test_create_task():
    new_task = {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False,
    }

    response = client.post(api_prefix, json=new_task)

    assert response.status_code == 200
    expected_response = new_task.copy()
    expected_response["id"] = response.json().get("id")
    expected_response["version"] = 1
    assert response.json() == expected_response


def test_read_tasks():
    response = client.get(api_prefix)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_task():
    new_task = {
        "title": "Task to Update",
        "description": "This task will be updated",
        "completed": False,
    }
    created_task = client.post(api_prefix, json=new_task)
    task_id = created_task.json().get("id")

    updated_task = {
        "id": task_id,
        "title": "Updated Task",
        "description": "This task has been updated",
        "completed": True,
        "version": 1,
    }

    update_response = client.put(f"{api_prefix}{task_id}", json=updated_task)

    assert update_response.json() == "as"
    # assert update_response.status_code == 200

    expected_response = updated_task.copy()
    expected_response["id"] = task_id
    expected_response["version"] = 2
    assert update_response.json() == expected_response


def test_delete_task():
    # First, create a task to delete
    new_task = {
        "title": "Task to Delete",
        "description": "This task will be deleted",
        "completed": False,
    }
    create_response = client.post(api_prefix, json=new_task)
    task_id = create_response.json().get("id")

    # Delete the task
    delete_response = client.delete(f"{api_prefix}{task_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": f"Task deleted: ID {task_id}"}

    # Verify the task is deleted
    get_response = client.get(f"{api_prefix}{task_id}")
    assert get_response.status_code == 404

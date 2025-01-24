#Todo Service

**Real-Time Collaborative Todo Management System (Assignment)**

This application is a real-time collaborative todo management system built with a Python backend (FastAPI) connected to MongoDB and an Angular frontend.

## How to Run the App

To run the entire application:
1. Start the database
Navigate to the backend folder and execute:
```
    docker-compose up
```
2. Start the backend
```
pipenv install
pipenv shell
fastapi dev
```  
3. Start the frontend
Navigate to the frontend directory and run:
```
npm install  
npm run start
```  
For more details, refer to the README.md files in the backend and frontend folders.

## TODOs:
- Move hardcoded configurations to dedicated configuration files
- Dockerize the entire app
- Implement "edit title and description" feature in the UI
- Add tests for both backend and frontend
- Fix backend test execution logic
- Add proper logging 
- Add pagination.
- Improve WebSocket to update only changed tasks without reloading the list.
# Backend for Todo Service

## Structure
- Uses MongoDB as database
- Uvicorn as web server


## Development

### Virtual Environment
Use `pipenv` to set up Virtual Python Environment and install dependencies:
```
pipenv install
```

### Code Formatting
Install Black pre-commit hook to format your code:
```
pip install pre-commit
```

### Running Development Server
Execute `pipenv shell` to open virtual python env and start dev server:
```
fastapi dev
```
Access API endpoints:
API: `http://127.0.0.1:8000`
Generated API Docs: `http://127.0.0.1:8000/docs`

### Database
Start development environment with MongoDB:
```
docker-compose up -d
```

Access Mongo Express at:
`http://127.0.0.1:8081`

Running Tests
Start infrastructure with docker-compose and run tests:
```
pytest
```

 
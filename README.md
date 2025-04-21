# Project Tracker

A FastAPI backend for managing computer graphics projects and their software versions.  
Tracks which versions are in use and prevents using deprecated or conflicting major versions per project.

---

## Features

- CRUD operations for projects and software versions  
- Associate software with a project  
  - Prevents deprecated versions  
  - Allows only one major version per software type per project  
- Filtering and pagination  


---

## How to Run

### With Docker

```bash
cp .env.example .env
./run.sh
```

## API Endpoints Examples


---

### Health Check

**`GET /`**  
Check if the service is running.

```bash
curl http://localhost:5000/
```

### Projects

**`GET POST /projects/`**  
Create a new project.
```bash
curl -X POST http://localhost:5000/projects/ \
  -H "Content-Type: application/json" \
  -d '{
    "code": "MAYA_PROJ",
    "archived": false,
    "start_date": "2025-04-01",
    "end_date": "2025-05-25"
  }'
```

**`GET GET /projects/`**  
List all projects.
```bash
curl http://localhost:5000/projects/
```

**`GET /projects/{project_id}/`**  
Get a single project by ID.
```bash
curl http://localhost:5000/projects/1
```

### Software Versions
**`POST /software/`**

Create a valid software version.
```bash
curl -X POST http://localhost:8000/software_versions/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Maya",
    "version": "2024.1",
    "vendor": "Autodesk",
    "deprecated": false
  }'
```


**`GET /software_versions/{software_id}`**

Get software version by ID.
```bash
curl http://localhost:8000/software_versions/1
```


### Project–Software Association
**`POST /associate/`**

Associate a valid software version to a project.
```bash
curl -X POST http://localhost:8000/associate/ \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "software_id": 1
  }'
```

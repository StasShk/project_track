from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .db import engine, SessionLocal, Base

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hi {name}!"}


### Projects
@app.post("/projects/", response_model=schemas.ProjectRead)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db, project)


@app.get("/projects/", response_model=List[schemas.ProjectRead])
def list_projects(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_projects(db, skip, limit)


@app.get("/projects/{project_id}", response_model=schemas.ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    crud.delete_project(db, project_id)
    return {"detail": "Project deleted"}


### Software Versions
@app.post("/software_versions/", response_model=schemas.SoftwareVersionRead)
def create_software(sw: schemas.SoftwareVersionCreate, db: Session = Depends(get_db)):
    return crud.create_software_version(db, sw)


@app.get("/software/", response_model=List[schemas.SoftwareVersionRead])
def list_software(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_software_versions(db, skip, limit)


@app.get("/software/{sw_id}", response_model=schemas.SoftwareVersionRead)
def get_software(sw_id: int, db: Session = Depends(get_db)):
    sw = crud.get_software_version(db, sw_id)
    if not sw:
        raise HTTPException(status_code=404, detail="Software version not found")
    return sw


@app.delete("/software/{sw_id}")
def delete_software(sw_id: int, db: Session = Depends(get_db)):
    crud.delete_software_version(db, sw_id)
    return {"detail": "Software version deleted"}


### Association

@app.post("/associate/", response_model=schemas.ProjectSoftwareAssociationRead)
def associate(assoc: schemas.ProjectSoftwareAssociationCreate, db: Session = Depends(get_db)):
    return crud.associate_software_to_project(db, assoc)

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from . import models, schemas


def get_major_version(version: str) -> str:
    return version.split(".")[0]


def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def get_projects(db: Session, skip: int = 0, limit: int = 10, start_date: str = None):
    query = db.query(models.Project)
    if start_date:
        query = query.filter(models.Project.start_date == start_date)
    return query.offset(skip).limit(limit).all()


def delete_project(db: Session, project_id: int):
    project = get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()


# -------- Software Versions --------

def create_software_version(db: Session, sw: schemas.SoftwareVersionCreate):
    db_sw = models.SoftwareVersion(**sw.dict())
    db.add(db_sw)
    db.commit()
    db.refresh(db_sw)
    return db_sw


def get_software_version(db: Session, sw_id: int):
    return db.query(models.SoftwareVersion).filter(models.SoftwareVersion.id == sw_id).first()


def get_software_versions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.SoftwareVersion).offset(skip).limit(limit).all()


def delete_software_version(db: Session, sw_id: int):
    sw = get_software_version(db, sw_id)
    if not sw:
        raise HTTPException(status_code=404, detail="Software version not found")
    db.delete(sw)
    db.commit()


def associate_software_to_project(db: Session, association: schemas.ProjectSoftwareAssociationCreate):
    project = get_project(db, association.project_id)
    software = get_software_version(db, association.software_id)

    if not project or not software:
        raise HTTPException(status_code=404, detail="Project or Software not found")

    if software.deprecated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot associate deprecated software version"
        )

    software_name = software.name
    current_versions = (
        db.query(models.SoftwareVersion)
        .join(models.ProjectSoftwareAssociation)
        .filter(models.ProjectSoftwareAssociation.project_id == project.id)
        .filter(models.SoftwareVersion.name == software_name)
        .all()
    )

    new_major = get_major_version(software.version)

    for v in current_versions:
        if get_major_version(v.version) != new_major:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Project already uses a different major version of {software_name}"
            )

    link = models.ProjectSoftwareAssociation(
        project_id=association.project_id,
        software_id=association.software_id
    )
    db.add(link)
    db.commit()
    db.refresh(link)
    return link

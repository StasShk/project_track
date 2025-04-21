from pydantic import BaseModel
from typing import Optional


class SoftwareVersionBase(BaseModel):
    name: str
    version: str
    vendor: Optional[str] = None
    deprecated: Optional[bool] = False


class SoftwareVersionCreate(SoftwareVersionBase):
    pass


class SoftwareVersionRead(SoftwareVersionBase):
    id: int

    class Config:
        orm_mode = True


# -------- Project --------

class ProjectBase(BaseModel):
    code: str
    archived: Optional[bool] = False
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id: int

    class Config:
        orm_mode = True


# -------- Association --------

class ProjectSoftwareAssociationBase(BaseModel):
    project_id: int
    software_id: int


class ProjectSoftwareAssociationCreate(ProjectSoftwareAssociationBase):
    pass


class ProjectSoftwareAssociationRead(ProjectSoftwareAssociationBase):
    id: int
    software: SoftwareVersionRead

    class Config:
        orm_mode = True

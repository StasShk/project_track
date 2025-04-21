from sqlalchemy import Column, Integer, TEXT, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .db import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(TEXT, unique=True, nullable=False)
    archived = Column(Integer, default=0)
    start_date = Column(TEXT)
    end_date = Column(TEXT)

    software = relationship("ProjectSoftwareAssociation", back_populates="project")


class SoftwareVersion(Base):
    __tablename__ = "software"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(TEXT, nullable=False)
    version = Column(TEXT, nullable=False)
    vendor = Column(TEXT)
    deprecated = Column(Integer, default=0)

    projects = relationship("ProjectSoftwareAssociation", back_populates="software")


class ProjectSoftwareAssociation(Base):
    __tablename__ = "project_software_associations"
    __table_args__ = (
        UniqueConstraint("project_id", "software_id", name="unique_project_software"),
    )

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    software_id = Column(Integer, ForeignKey("software.id"))

    project = relationship("Project", back_populates="software")
    software = relationship("SoftwareVersion", back_populates="projects")
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = "task"
    id         = Column(Integer, primary_key=True)
    title      = Column(String, nullable=False)
    status     = Column(String, nullable=False, server_default="Pendente")
    created_at = Column(DateTime, server_default=func.now())

class TimeEntry(Base):
    __tablename__ = "time_entry"
    id         = Column(Integer, primary_key=True)
    task_id    = Column(Integer, ForeignKey("task.id"))
    start_at   = Column(DateTime, nullable=False, server_default=func.now())
    end_at     = Column(DateTime, nullable=True)
    duration_s = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

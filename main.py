from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
import uvicorn

from database import SessionLocal
from models import Base, Task

from datetime import datetime

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TaskIn(BaseModel):
    title: str

class TaskOut(BaseModel):
    id: int
    title: str
    status: str
    created_at: datetime
    class Config:
        orm_mode = True

class StatusUpdate(BaseModel):
    status: str

ALLOWED = ["Pendente", "Andamento", "Pausado", "Aguardando", "Concluído"]

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=SessionLocal().bind)

@app.post("/tasks/", response_model=TaskOut)
def create_task(data: TaskIn, db: Session = Depends(get_db)):
    t = Task(title=data.title)
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

@app.get("/tasks/", response_model=List[TaskOut])
def list_tasks(db: Session = Depends(get_db)):
    return db.query(Task).order_by(Task.status, Task.created_at).all()

@app.patch("/tasks/{task_id}/status", response_model=TaskOut)
def change_status(task_id: int, upd: StatusUpdate, db: Session = Depends(get_db)):
    if upd.status not in ALLOWED:
        raise HTTPException(400, "Status inválido")
    t = db.query(Task).filter(Task.id == task_id).first()
    if not t:
        raise HTTPException(404, "Task não encontrada")
    t.status = upd.status
    db.commit()
    db.refresh(t)
    return t

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
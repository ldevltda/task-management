from fastapi import FastAPI
from database import engine
from models import Base

app = FastAPI()

# só para garantir que o metadata está disponível
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"status": "ok"}

from fastapi import FastAPI
from sqlalchemy import create_engine

app = FastAPI()

engine = create_engine("sqlite:///exercise.db")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hi {name}!"}

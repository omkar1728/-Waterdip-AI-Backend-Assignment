from fastapi import FastAPI
from pydantic import BaseModel


class Task(BaseModel):
    id: int | None
    title: str
    is_completed: bool = False

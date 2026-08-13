from fastapi import FastAPI
from pydantic import BaseModel


class URL(BaseModel):
    url: str


app = FastAPI()


@app.get("/")
def test_root():
    return {"Project": "URL shortener"}


@app.post("/shorten/")
def shorten(url: URL):
    return url

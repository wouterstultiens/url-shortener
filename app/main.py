from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def test_root():
    return {"Project": "URL shortener"}


@app.get("/shorten/{url}")
def shorten(url: str):
    return {"short_url": url[:-3]}

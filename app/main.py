from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def test_root():
    return {"Project": "Url shortener"}

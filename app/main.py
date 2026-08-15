import random
import re
import string
from datetime import UTC, datetime
from itertools import count
from typing import Annotated

from fastapi import FastAPI, HTTPException
from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    HttpUrl,
)
from pydantic.alias_generators import to_camel


def is_short_code_format(short_code: str) -> str:
    short_code_regex = r"[A-Za-z]{3}[0-9]{3}"
    if not re.fullmatch(short_code_regex, short_code):
        raise ValueError("Invalid ShortCode format")
    return short_code


ShortCode = Annotated[str, AfterValidator(is_short_code_format)]


class ShortenRequest(BaseModel):
    url: HttpUrl


class ShortenedURL(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    id: int
    url: HttpUrl
    short_code: ShortCode
    created_at: datetime
    updated_at: datetime


class ShortenedURLStats(ShortenedURL):
    access_count: int = 0


app = FastAPI()

id_counter = count(1)

shortened_urls: list[ShortenedURLStats] = [
    ShortenedURLStats(
        id=0,
        url=HttpUrl("https://hello.com/helloabc"),
        short_code="jxv834",
        created_at=datetime.now(tz=UTC),
        updated_at=datetime.now(tz=UTC),
        access_count=3,
    )
]


@app.get("/")
def test_root():
    return {"Project": "URL shortener"}


@app.post("/shorten/", response_model=ShortenedURL, status_code=201)
def shorten(payload: ShortenRequest):
    # Assign and increment id
    id = next(id_counter)

    # Create shortcode
    random_characters = "".join(
        [random.choice(string.ascii_lowercase) for _ in range(3)]
    )
    random_numbers = random.randint(100, 1000)
    short_code = random_characters + str(random_numbers)

    # Dates and times
    now = datetime.now(tz=UTC)
    created_at = now
    updated_at = now

    # Create object
    shortened_url = ShortenedURLStats(
        id=id,
        url=payload.url,
        short_code=short_code,
        created_at=created_at,
        updated_at=updated_at,
    )

    # Write to DB
    shortened_urls.append(shortened_url)

    # Return object
    return shortened_url


@app.get("/shorten/{short_code}", response_model=ShortenedURL)
def retrieve_url(short_code: ShortCode):
    for current in shortened_urls:
        if short_code == current.short_code:
            current.access_count += 1
            return current
    raise HTTPException(404, detail="Short code not found in DB")


@app.put("/shorten/{short_code}", response_model=ShortenedURL)
def update_url(short_code: ShortCode, payload: ShortenRequest):
    for i, current in enumerate(shortened_urls):
        if short_code == current.short_code:
            current.url = payload.url
            current.updated_at = datetime.now(tz=UTC)
            shortened_urls[i] = current
            return shortened_urls[i]
    raise HTTPException(404, detail="Short code not found in DB")


@app.delete("/shorten/{short_code}", status_code=204)
def delete_url(short_code: ShortCode):
    for i, current in enumerate(shortened_urls):
        if short_code == current.short_code:
            del shortened_urls[i]
            return {"ok": True}
    raise HTTPException(404, detail="Short code not found in DB")


@app.get("/shorten/{short_code}/stats", response_model=ShortenedURLStats)
def retrieve_url_stats(short_code: ShortCode):
    for current in shortened_urls:
        if short_code == current.short_code:
            return current
    raise HTTPException(404, detail="Short code not found in DB")

import random
import string
from datetime import UTC, datetime
from itertools import count

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class ShortenRequest(BaseModel):
    url: str


class ShortenedURL(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    id: int
    url: str
    short_code: str = Field(min_length=6, max_length=6)
    created_at: datetime
    updated_at: datetime


app = FastAPI()

id_counter = count(0)


shortened_urls: list[ShortenedURL] = []


@app.get("/")
def test_root():
    return {"Project": "URL shortener"}


@app.post("/shorten/", status_code=201)
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
    shortened_url = ShortenedURL(
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

# URL Shortening Service

Project spec from [roadmap.sh](https://roadmap.sh/projects/url-shortening-service), saved for offline use.

## Goal

Build a RESTful API that lets users shorten long URLs. The API must support creating, retrieving, updating, and deleting short URLs, and it must track access statistics.

## Requirements

- Create a new short URL with a randomly generated, unique short code.
- Retrieve the original URL from a short code.
- Update an existing short URL mapping.
- Delete a short URL.
- Track how many times a short URL is accessed, and report it.
- Optional: a minimal frontend and a real redirect endpoint.

No authentication or authorization is required. Focus on the core functionality.

## API Endpoints

### Create Short URL

`POST /shorten`

Request body:

```json
{
  "url": "https://www.example.com/some/long/url"
}
```

- `201 Created` with the new short URL object:

```json
{
  "id": "1",
  "url": "https://www.example.com/some/long/url",
  "shortCode": "abc123",
  "createdAt": "2021-09-01T12:00:00Z",
  "updatedAt": "2021-09-01T12:00:00Z"
}
```

- `400 Bad Request` when validation fails.

### Retrieve Original URL

`GET /shorten/abc123`

- `200 OK` with the short URL object (same shape as above).
- `404 Not Found` when the short code does not exist.

### Update Short URL

`PUT /shorten/abc123`

Request body:

```json
{
  "url": "https://www.example.com/some/updated/url"
}
```

- `200 OK` with the updated object (`updatedAt` changes).
- `400 Bad Request` when validation fails.
- `404 Not Found` when the short code does not exist.

### Delete Short URL

`DELETE /shorten/abc123`

- `204 No Content` on success.
- `404 Not Found` when the short code does not exist.

### Get Statistics

`GET /shorten/abc123/stats`

- `200 OK` with the object plus an `accessCount` field:

```json
{
  "id": "1",
  "url": "https://www.example.com/some/long/url",
  "shortCode": "abc123",
  "createdAt": "2021-09-01T12:00:00Z",
  "updatedAt": "2021-09-01T12:00:00Z",
  "accessCount": 10
}
```

- `404 Not Found` when the short code does not exist.

## Beyond the spec: the break-fix ladder

The spec above is milestone 1 only. The senior-level learning comes from what roadmap.sh does not include:

1. **Milestone 1 — plain build.** FastAPI + Postgres, no cache, no queue. Deploy to Azure App Service.
2. **Milestone 2 — measure.** Load-test with locust until latency falls apart. Record req/s and p95 before and after every change.
3. **Milestone 3 — cache.** Add Redis caching for redirects. Break it again.
4. **Milestone 4 — rate limiter.** Write your own (spec: https://codingchallenges.fyi/challenges/challenge-rate-limiter/).
5. **Milestone 5 — queue + workers.** Move access-count writes to a queue with multiple workers.

Watch every break in Application Insights. Keep the story in the README: "at N req/s, p95 went to X because Y; I added Z; here is the graph."

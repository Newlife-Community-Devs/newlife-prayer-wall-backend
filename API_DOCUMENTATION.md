# PrayerWall Backend API Documentation

Last updated: 2025-11-07

This file documents the FastAPI backend available under `backend/` (served by `uvicorn app.main:app`). It lists all public and authenticated endpoints, request/response shapes (schemas), examples and common error responses.

## Base info

- Base URL (local dev): `http://127.0.0.1:8000`
- Start server (from repository root):

```powershell
cd newlife-prayer-wall/backend
# activate your venv then
uvicorn app.main:app --reload
```

## Authentication

- Auth type: JWT (Bearer tokens) using OAuth2 password flow.
- Token endpoint: `POST /auth/token` — uses `application/x-www-form-urlencoded` with `username` and `password` (OAuth2PasswordRequestForm).
- Returned model: `Token` — {"access_token": "<jwt>", "token_type": "bearer"}
- Use the token in requests as an `Authorization: Bearer <token>` header for protected endpoints.
- Token creation uses `app.auth.create_access_token` and `SECRET_KEY` from `backend/.env`.

## Top-level health and root

- GET `/` — basic root, returns {"message": "PrayerWall backend is running"}
- GET `/health` — health-check which also attempts a simple DB query. Example success:

```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-11-07T...Z"
}
```

## Routes (grouped)

All routes are prefixed in the code using `app.routes.router`:

- Auth: `/auth`
- Prayers: `/prayers`
- Admin: `/admin`

### Auth

- POST `/auth/register`

  - Description: Register a new user.
  - Auth: public
  - Request JSON: `schemas.UserCreate` — {"email":"user@example.com","password":"...","full_name":"..."}
  - Response: `schemas.UserOut` — created user without password
  - Errors: 400 if email already registered

- POST `/auth/token`
  - Description: Obtain access token (OAuth2 password grant). Expects form-encoded fields `username` and `password`.
  - Auth: public
  - Request: Content-Type `application/x-www-form-urlencoded` body: `username=...&password=...`
  - Response: `schemas.Token` — {"access_token":"...","token_type":"bearer"}
  - Errors: 401 Incorrect username or password

### Prayers (`/prayers`)

- POST `/prayers/`

  - Description: Create a prayer request for an authenticated user.
  - Auth: Bearer token required
  - Request JSON: `schemas.PrayerCreate` — e.g. {"title": "Help", "content": "Please pray..."}
  - Response: `schemas.PrayerOut` (201)

- POST `/prayers/submit` (public)
  - Description: Public endpoint used by the frontend modal to submit a prayer request. Maps frontend fields to internal schema and stores submitter info only if not anonymous.
  - Auth: public
  - Request JSON: `schemas.PrayerPublicIn` —
    - Example:

```json
{
  "name": "Jane Doe",
  "phoneNumber": "555-1234",
  "prayerRequest": "Please pray for healing",
  "keepAnonymous": false
}
```

- Internally mapped to `PrayerCreate` and stored with `owner_id = NULL` for public submissions.
- Response: `schemas.PrayerOut` (201)

- GET `/prayers/`

  - Description: List prayers created by the current authenticated user (personal requests).
  - Auth: Bearer token required
  - Response: List[`schemas.PrayerOut`]

- GET `/prayers/wall`

  - Description: Public paginated prayer wall with filtering and sorting.
  - Auth: public
  - Query parameters:
    - `skip` (int, default 0)
    - `limit` (int, default 20)
    - Filter fields provided via dependency `schemas.PrayerFilter` (e.g., `search`, `is_answered`, `is_flagged`, `status`, `created_after`, `created_before`, `sort_by`, `sort_order`).
  - Response: `schemas.PrayerListOut` => {"items": [...], "total": n, "has_more": bool}

- PATCH `/prayers/{prayer_id}`

  - Description: Update a prayer (status / flags / answered). Admins may update status and flags for any prayer. Regular users can update only their own prayers and only limited fields (e.g. mark answered).
  - Auth: Bearer token required
  - Request JSON: `schemas.PrayerUpdate` — {"is_answered": true}
  - Response: `schemas.PrayerOut`
  - Errors: 403 if not authorized, 404 if prayer not found

- GET `/prayers/moderation`
  - Description: Admin-only moderation queue (returns pending items by default)
  - Auth: Bearer token required (admin)
  - Query params: same pagination + `schemas.PrayerFilter`
  - Response: `schemas.PrayerListOut`

### Admin (`/admin`)

- GET `/admin/prayers`

  - Description: Admin paginated list of prayer requests. Query parameters `page` (default 1), `page_size` (default 20).
  - Auth: Bearer token required (admin)
  - Response: `schemas.PrayerListOut` (items + total)

- PATCH `/admin/prayers/{prayer_id}/answered`

  - Description: Mark a prayer as answered (or unmark) — admin-only.
  - Auth: Bearer token required (admin)
  - Query param: `answered` (bool, default true)
  - Response: `schemas.PrayerOut`

- DELETE `/admin/prayers/{prayer_id}`
  - Description: Delete a prayer — admin-only.
  - Auth: Bearer token required (admin)
  - Response: {"detail":"Prayer deleted"}
  - Errors: 404 if not found

## Schemas (high-level)

The Pydantic models are defined in `backend/app/schemas.py`. Important ones shown here with main fields:

- `UserCreate`

  - email: EmailStr
  - password: str
  - full_name: Optional[str]

- `UserOut`

  - id: int, email: EmailStr, full_name: Optional[str], is_active: bool, is_admin: bool

- `Token`

  - access_token: str
  - token_type: str

- `PrayerCreate`

  - title: Optional[str]
  - content: str
  - submitter_name: Optional[str]
  - phone_number: Optional[str]
  - is_anonymous: bool

- `PrayerOut`

  - id: int
  - title: Optional[str]
  - content: str
  - created_at: datetime
  - is_answered: bool
  - is_flagged: bool
  - owner_id: Optional[int]
  - submitter_name, phone_number, is_anonymous

- `PrayerPublicIn` (frontend)

  - name, phoneNumber, prayerRequest, keepAnonymous

- `PrayerListOut`

  - items: list[PrayerOut], total: int, has_more: bool

- `PrayerUpdate`

  - is_answered: Optional[bool], is_flagged: Optional[bool], status: Optional[PrayerStatus]

- `PrayerFilter`
  - search, is_answered, is_flagged, status, created_after, created_before, sort_by, sort_order

## Common error responses

- 400 Bad Request — invalid input (validation errors)
- 401 Unauthorized — invalid/expired token or incorrect username/password
- 403 Forbidden — not authorized for the action (e.g., non-admin accessing admin endpoints)
- 404 Not Found — resource not found
- 500 Internal Server Error — unexpected server error (check logs)

Example token error when credentials are wrong:

```json
{ "detail": "Incorrect username or password" }
```

## Example curl requests

1. Obtain token (PowerShell-friendly):

```powershell
curl -X POST "http://127.0.0.1:8000/auth/token" -H "Content-Type: application/x-www-form-urlencoded" --data "username=admin@prayerwall.com&password=Prayer123!"
```

Response:

```json
{ "access_token": "<JWT_TOKEN>", "token_type": "bearer" }
```

2. Submit a public prayer (no auth):

```bash
curl -X POST "http://127.0.0.1:8000/prayers/submit" -H "Content-Type: application/json" -d '{"name":"Jane","phoneNumber":"555","prayerRequest":"Please pray","keepAnonymous":false}'
```

3. Create a prayer as an authenticated user:

```bash
curl -X POST "http://127.0.0.1:8000/prayers/" -H "Authorization: Bearer <JWT_TOKEN>" -H "Content-Type: application/json" -d '{"title":"Hello","content":"Pray for me"}'
```

4. Get paginated prayer wall with filters:

```bash
curl "http://127.0.0.1:8000/prayers/wall?skip=0&limit=10&search=healing"
```

## Notes, tips and implementation details

- DB: connection string is `DATABASE_URL` in `backend/.env` (defaults to postgres://... in the example). The project uses SQLAlchemy and `Base.metadata.create_all` at startup to create tables.
- Password hashing: `passlib` with bcrypt in `app.auth` (`CryptContext(schemes=["bcrypt"])`).
- JWT: `python-jose` used for JWT encode/decode.
- Pagination: `crud.get_all_prayers_paginated` returns `items, total, has_more`. The API truncates extra row to set `has_more`.
- Admin CLI: `backend/create_admin.py` provides Typer commands to create/change admin users; this is useful for local testing.

## Troubleshooting

- If `/auth/token` returns 401: confirm user exists (DB) and try resetting the password via `create_admin.py` or the CLI `create-admin`/`change-password` commands. Example:

```powershell
cd newlife-prayer-wall/backend
.\.venv\Scripts\Activate.ps1
python create_admin.py create-admin --email admin@prayerwall.com
```

- If DB connection fails, check `backend/.env` and ensure Postgres is running and the database exists.

## Where to look in code

- Routes: `backend/app/routes/*` (`auth.py`, `prayers.py`, `admin.py`)
- Schemas: `backend/app/schemas.py`
- CRUD & models: `backend/app/crud.py`, `backend/app/models.py`
- Auth helpers: `backend/app/auth.py`
- DB config: `backend/app/config.py`, `backend/app/database.py`

---

If you'd like, I can also generate a Postman collection or OpenAPI YAML/JSON exported from the running FastAPI (FastAPI already provides an OpenAPI UI at `/docs` and raw schema at `/openapi.json`). Would you like me to:

- A) Export an `openapi.json` file into `backend/openapi.json` now, or
- B) Generate a Postman collection wrapper, or
- C) Nothing further — this document is fine?

# PrayerWall Backend API Documentation

This document describes the backend API implemented in `backend/app`.
It covers routes, request/response schemas, authentication, examples, and common error responses.

Base URL (development): http://127.0.0.1:8000

## Authentication

- Type: JWT (Bearer)
- Token endpoint: POST /auth/token
  - Content-Type: application/x-www-form-urlencoded
  - Form fields: `username` (email), `password`
  - Response: `{ "access_token": "<JWT>", "token_type": "bearer" }`
  - Notes: Use token in `Authorization: Bearer <token>` header for protected endpoints.

## Routes and Schemas

All routes are mounted under the main app router in `backend/app/routes`.

### 1) Auth

#### POST /auth/register

- Purpose: Register a new user.
- Request body (JSON):
  ```json
  {
    "email": "user@example.com",
    "password": "Password123!",
    "full_name": "Full Name"
  }
  ```
- Response (201/200): `UserOut`:
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "full_name": "Full Name",
    "is_active": true,
    "is_admin": false
  }
  ```

#### POST /auth/token

- Purpose: Obtain JWT access token using username/password (OAuth2 password flow)
- Content-Type: application/x-www-form-urlencoded
- Form: `username` (email), `password`
- Response: `Token`:
  ```json
  { "access_token": "<JWT>", "token_type": "bearer" }
  ```
- Errors: 401 for incorrect credentials

### 2) Prayers

#### POST /prayers/ (protected)

- Purpose: Create a prayer request as an authenticated user.
- Authorization: Bearer token required
- Request body (JSON) `PrayerCreate`:
  ```json
  {
    "title": "Optional title",
    "content": "Prayer text",
    "submitter_name": null,
    "phone_number": null,
    "is_anonymous": false
  }
  ```
- Response: `PrayerOut` (created prayer)

#### POST /prayers/submit (public)

- Purpose: Submit a prayer from the public frontend modal (no auth required).
- Request body (JSON) `PrayerPublicIn` (frontend keys):
  ```json
  {
    "name": "Jane Doe",
    "phoneNumber": "555-1234",
    "prayerRequest": "Please pray for healing",
    "keepAnonymous": false
  }
  ```
- Behavior: Maps frontend keys to internal `PrayerCreate`, stores submitter info only if `keepAnonymous` is false.
- Response: `PrayerOut` (201)

#### GET /prayers/ (protected)

- Purpose: List prayers belonging to the authenticated user.
- Authorization: Bearer token required
- Query params: none (can later support pagination)
- Response: list of `PrayerOut`

#### GET /prayers/wall (public)

- Purpose: Get paginated public prayer wall
- Query params:
  - `skip` (int, default 0)
  - `limit` (int, default 20)
  - Filter params are provided via `PrayerFilter` model (as query parameters)
- Response: `PrayerListOut`:
  ```json
  {
    "items": [
      /* array of PrayerOut */
    ],
    "total": 123,
    "has_more": true
  }
  ```

#### PATCH /prayers/{prayer_id} (protected)

- Purpose: Update prayer (status/flags/answered)
- Authorization: Bearer token required. Admins can update any prayer, users can update their own but cannot change status or flag.
- Request body: `PrayerUpdate`:
  ```json
  {
    "is_answered": true,
    "is_flagged": false,
    "status": "approved"
  }
  ```
- Response: updated `PrayerOut`

#### GET /prayers/moderation (protected, admin only)

- Purpose: Get prayers requiring moderation. Defaults to showing pending if no status filter provided.
- Query params: `skip`, `limit`, filter params
- Response: `PrayerListOut`

### 3) Admin routes (prefixed with /admin)

> Note: Admin routes use `require_admin` dependency to enforce admin-only access.

#### GET /admin/prayers

- Purpose: Paginated list of all prayers (admin view)
- Query params: `page` (default 1), `page_size` (default 20)
- Response: `PrayerListOut`

#### PATCH /admin/prayers/{prayer_id}/answered

- Purpose: Mark prayer as answered or un-answered
- Query param: `answered` (bool, default true)
- Response: `PrayerOut`

#### DELETE /admin/prayers/{prayer_id}

- Purpose: Delete a prayer (admin only)
- Response: `{ "detail": "Prayer deleted" }`

## Schemas (short reference)

- `UserCreate`: { email: EmailStr, password: str, full_name?: str }
- `UserOut`: { id: int, email: EmailStr, full_name?: str, is_active: bool, is_admin: bool }
- `PrayerCreate`: { title?: str, content: str, submitter_name?: str, phone_number?: str, is_anonymous?: bool }
- `PrayerOut`: { id, title, content, created_at, is_answered, is_flagged, owner_id?, submitter_name?, phone_number?, is_anonymous? }
- `PrayerPublicIn` (frontend): { name?, phoneNumber?, prayerRequest, keepAnonymous? }
- `PrayerListOut`: { items: [PrayerOut], total: int, has_more: bool }
- `PrayerUpdate`: { is_answered?: bool, is_flagged?: bool, status?: "pending"|"approved"|"rejected"|"archived" }

## Authentication and Security Notes

- Tokens issued by `/auth/token` expire after `ACCESS_TOKEN_EXPIRE_MINUTES` (default 60). The secret key is configured in `.env` as `SECRET_KEY`.
- Admin-only endpoints use `require_admin` dependency which checks `is_admin` on the current user.
- Public endpoints are rate-limited implicitly by deployment; add a rate-limiter or captcha for the public submit endpoint in production.

## Example curl commands (PowerShell friendly)

Health check:

```powershell
curl "http://127.0.0.1:8000/health"
```

Obtain token (PowerShell):

```powershell
curl -X POST "http://127.0.0.1:8000/auth/token" -H "Content-Type: application/x-www-form-urlencoded" --data "username=admin@prayerwall.com&password=Prayer123!"
```

Submit a public prayer (JSON):

```powershell
curl -X POST "http://127.0.0.1:8000/prayers/submit" -H "Content-Type: application/json" -d '{"name":"Jane Doe","phoneNumber":"555-1234","prayerRequest":"Please pray for healing","keepAnonymous":false}'
```

Auth-protected request (example get my prayers):

```powershell
$token = "<JWT>"
curl -H "Authorization: Bearer $token" "http://127.0.0.1:8000/prayers/"
```

## Errors and status codes

- 401 Unauthorized: invalid or missing token, incorrect credentials
- 403 Forbidden: not authorized (e.g., non-admin trying to access admin endpoints)
- 404 Not Found: prayer or resource not found
- 400 Bad Request: validation errors on inputs

## Next steps / Improvements

- Add OpenAPI/Swagger examples via FastAPI's `response_model` and `example` parameters for better generated docs.
- Add request/response examples to Pydantic schemas for clearer auto-generated docs.
- Add rate-limiting and reCAPTCHA for `/prayers/submit` to mitigate spam.
- Add Alembic migrations instead of relying on `create_all` in production.

---

If you'd like, I can:

- Create a `backend/openapi_overrides.py` to add improved examples to the auto-generated docs.
- Generate Postman/Insomnia collection JSON for import.
- Add API docs to the frontend README or expose a static markdown in `/public`.

Which would you prefer next?

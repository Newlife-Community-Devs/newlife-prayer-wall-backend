# PrayerWall Backend API Documentation# PrayerWall Backend API Documentation

**Last Updated**: 2025-11-12 **Last updated: 2025-11-12**

**API Version**: 1.0.0

**Repository**: https://github.com/Newlife-Community-Devs/newlife-prayer-wall-backend This document provides comprehensive documentation for the PrayerWall FastAPI backend. It covers all endpoints, authentication, request/response schemas, deployment configuration, and testing procedures.

This document provides comprehensive documentation for the PrayerWall FastAPI backend, covering all endpoints, authentication, request/response schemas, deployment configuration, and testing procedures.## Base Information

## Table of Contents- **Base URL (local dev)**: `http://127.0.0.1:8000`

- **Repository**: https://github.com/Newlife-Community-Devs/newlife-prayer-wall-backend

- [Base Information](#base-information)- **Tech Stack**: FastAPI, PostgreSQL, SQLAlchemy, JWT Authentication

- [Authentication](#authentication)- **Python Version**: 3.11+

- [Health Check Endpoints](#health-check-endpoints)

- [API Routes](#api-routes)### Starting the Server (Local Development)

  - [Auth Routes](#auth-routes-auth)

  - [Prayer Routes](#prayer-routes-prayers)```powershell

  - [Admin Routes](#admin-routes-admin)cd backend

- [Data Schemas](#data-schemas)# Activate virtual environment

- [Error Responses](#error-responses).\.venv\Scripts\Activate.ps1 # Windows PowerShell

- [Testing](#testing)source .venv/bin/activate # Linux/Mac

- [Deployment](#deployment)

- [Database Setup](#database-setup)# Start server

- [Development](#development)python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

- [Troubleshooting](#troubleshooting)```

---## Authentication

## Base Information### Overview

- **Base URL (local dev)**: `http://127.0.0.1:8000`- **Type**: JWT (JSON Web Tokens) with Bearer authentication

- **Tech Stack**: FastAPI, PostgreSQL, SQLAlchemy, JWT Authentication- **Algorithm**: HS256

- **Python Version**: 3.11+- **Token Expiration**: 60 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)

- **Interactive Docs**: - **Password Hashing**: bcrypt (via passlib==1.7.4)

  - Swagger UI: http://127.0.0.1:8000/docs

  - ReDoc: http://127.0.0.1:8000/redoc### Token Endpoint

  - OpenAPI Schema: http://127.0.0.1:8000/openapi.json

**POST** `/auth/token`

### Starting the Server (Local Development)

Obtain a JWT access token using OAuth2 password flow.

`````powershell

cd backend**Request**:

# Activate virtual environment

.\.venv\Scripts\Activate.ps1  # Windows PowerShell- **Content-Type**: `application/x-www-form-urlencoded`

source .venv/bin/activate      # Linux/Mac- **Body** (form-encoded):

  - `username`: User's email address

# Start server  - `password`: User's password

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

```**Response** (200 OK):



---```json

{

## Authentication  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",

  "token_type": "bearer"

### Overview}

- **Type**: JWT (JSON Web Tokens) with Bearer authentication```

- **Algorithm**: HS256

- **Token Expiration**: 60 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)**Errors**:

- **Password Hashing**: bcrypt (via passlib==1.7.4)

- `401 Unauthorized`: Incorrect username or password

### Token Endpoint

**Example** (PowerShell):

**POST** `/auth/token`

```powershell

Obtain a JWT access token using OAuth2 password flow.curl -X POST "http://127.0.0.1:8000/auth/token" `

  -H "Content-Type: application/x-www-form-urlencoded" `

**Request**:  --data "username=admin@prayerwall.com&password=Prayer123!"

- **Content-Type**: `application/x-www-form-urlencoded````

- **Body** (form-encoded):

  - `username`: User's email address### Using the Token

  - `password`: User's password

Include the token in the `Authorization` header for protected endpoints:

**Response** (200 OK):

```json```

{Authorization: Bearer <your_jwt_token>

  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",```

  "token_type": "bearer"

}## Health Check Endpoints

`````

### GET `/`

**Errors**:

- `401 Unauthorized`: Incorrect username or passwordBasic root endpoint to verify the API is running.

**Example** (PowerShell):**Response** (200 OK):

`````powershell

curl -X POST "http://127.0.0.1:8000/auth/token" ````json

  -H "Content-Type: application/x-www-form-urlencoded" `{

  --data "username=admin@prayerwall.com&password=Prayer123!"  "message": "PrayerWall backend is running"

```}

`````

### Using the Token

### GET `/health`

Include the token in the `Authorization` header for protected endpoints:

Health check endpoint that verifies database connectivity.

```

Authorization: Bearer <your_jwt_token>**Response** (200 OK):

```

````json

---{

  "status": "healthy",

## Health Check Endpoints  "database": "connected",

  "timestamp": "2025-11-12T13:15:25.123456"

### GET `/`}

Basic root endpoint to verify the API is running.```



**Response** (200 OK):**Response** (503 Service Unavailable):

```json

{```json

  "message": "PrayerWall backend is running"{

}  "status": "unhealthy",

```  "database": "disconnected",

  "error": "Connection error details"

### GET `/health`}

Health check endpoint that verifies database connectivity.```



**Response** (200 OK):## API Routes

```json

{All routes are organized by prefix:

  "status": "healthy",

  "database": "connected",- **Auth**: `/auth` - Authentication and user registration

  "timestamp": "2025-11-12T13:15:25.123456"- **Prayers**: `/prayers` - Prayer request management

}- **Admin**: `/admin` - Administrative functions

````

---

**Response** (503 Service Unavailable):

```json### Auth Routes (`/auth`)

{

"status": "unhealthy",#### POST `/auth/register`

"database": "disconnected",

"error": "Connection error details"Register a new user account.

}

````**Authentication**: Public (no token required)



---**Request Body** (`UserCreate`):



## API Routes```json

{

All routes are organized by prefix:  "email": "user@example.com",

- **Auth**: `/auth` - Authentication and user registration  "password": "SecurePassword123!",

- **Prayers**: `/prayers` - Prayer request management  "full_name": "John Doe"

- **Admin**: `/admin` - Administrative functions}

````

**Legend**:

- 🔓 = Public (no authentication required)**Response** (201 Created) - `UserOut`:

- 🔒 = Protected (requires Bearer token)

- 👮 = Admin Only (requires admin privileges)```json

{

--- "id": 1,

"email": "user@example.com",

### Auth Routes (`/auth`) "full_name": "John Doe",

"is_active": true,

#### POST `/auth/register` 🔓 "is_admin": false

}

Register a new user account.```

**Request Body** (`UserCreate`):**Errors**:

```````json

{- `400 Bad Request`: Email already registered

  "email": "user@example.com",

  "password": "SecurePassword123!",**Example**:

  "full_name": "John Doe"

}```powershell

```curl -X POST "http://127.0.0.1:8000/auth/register" `

  -H "Content-Type: application/json" `

**Response** (201 Created) - `UserOut`:  -d '{"email":"user@example.com","password":"SecurePass123!","full_name":"John Doe"}'

```json```

{

  "id": 1,#### POST `/auth/token`

  "email": "user@example.com",

  "full_name": "John Doe",See [Authentication](#authentication) section above.

  "is_active": true,

  "is_admin": false---

}

```### Prayer Routes (`/prayers`)



**Errors**:#### POST `/prayers/submit` 🔓 Public

- `400 Bad Request`: Email already registered

**Public endpoint** for submitting prayer requests from the frontend modal (no authentication required).

**Example**:

```powershell**Authentication**: Public (no token required)

curl -X POST "http://127.0.0.1:8000/auth/register" `

  -H "Content-Type: application/json" `**Request Body** (`PrayerPublicIn`):

  -d '{"email":"user@example.com","password":"SecurePass123!","full_name":"John Doe"}'

``````json

{

#### POST `/auth/token` 🔓  "name": "Jane Doe",

  "phoneNumber": "555-1234",

See [Authentication](#authentication) section above.  "prayerRequest": "Please pray for healing and recovery",

  "keepAnonymous": false

---}

```````

### Prayer Routes (`/prayers`)

**Field Mapping**:

#### POST `/prayers/submit` 🔓

- `prayerRequest` → `content` (prayer text)

**Public endpoint** for submitting prayer requests from the frontend modal (no authentication required).- `name` → `submitter_name` (stored only if `keepAnonymous` is `false`)

- `phoneNumber` → `phone_number` (stored only if `keepAnonymous` is `false`)

**Request Body** (`PrayerPublicIn`):- `keepAnonymous` → `is_anonymous`

````json

{**Response** (201 Created) - `PrayerOut`:

  "name": "Jane Doe",

  "phoneNumber": "555-1234",```json

  "prayerRequest": "Please pray for healing and recovery",{

  "keepAnonymous": false  "id": 1,

}  "title": null,

```  "content": "Please pray for healing and recovery",

  "created_at": "2025-11-12T13:15:25.423851",

**Field Mapping**:  "is_answered": false,

- `prayerRequest` → `content` (prayer text)  "is_flagged": false,

- `name` → `submitter_name` (stored only if `keepAnonymous` is `false`)  "status": "pending",

- `phoneNumber` → `phone_number` (stored only if `keepAnonymous` is `false`)  "owner_id": null,

- `keepAnonymous` → `is_anonymous`  "submitter_name": "Jane Doe",

  "phone_number": "555-1234",

**Response** (201 Created) - `PrayerOut`:  "is_anonymous": false

```json}

{```

  "id": 1,

  "title": null,**Example**:

  "content": "Please pray for healing and recovery",

  "created_at": "2025-11-12T13:15:25.423851",```powershell

  "is_answered": false,curl -X POST "http://127.0.0.1:8000/prayers/submit" `

  "is_flagged": false,  -H "Content-Type: application/json" `

  "status": "pending",  -d '{"name":"Jane Doe","phoneNumber":"555-1234","prayerRequest":"Please pray for healing","keepAnonymous":false}'

  "owner_id": null,```

  "submitter_name": "Jane Doe",

  "phone_number": "555-1234",#### GET `/prayers/wall` 🔓 Public

  "is_anonymous": false

}Get paginated list of approved prayers for the public prayer wall.

````

**Authentication**: Public (no token required)

**Example**:

````powershell**Query Parameters**:

curl -X POST "http://127.0.0.1:8000/prayers/submit" `

  -H "Content-Type: application/json" `- `skip` (int, default: 0) - Number of items to skip for pagination

  -d '{"name":"Jane Doe","phoneNumber":"555-1234","prayerRequest":"Please pray for healing","keepAnonymous":false}'- `limit` (int, default: 20, max: 100) - Number of items per page

```- `search` (string, optional) - Search in prayer content

- `is_answered` (boolean, optional) - Filter by answered status

#### GET `/prayers/wall` 🔓- `is_flagged` (boolean, optional) - Filter by flagged status

- `status` (enum, optional) - Filter by status: `pending`, `approved`, `rejected`, `archived`

Get paginated list of approved prayers for the public prayer wall.- `created_after` (datetime, optional) - Filter prayers created after this date

- `created_before` (datetime, optional) - Filter prayers created before this date

**Query Parameters**:- `sort_by` (enum, default: `created_at`) - Sort field: `created_at`, `is_answered`, `is_flagged`

- `skip` (int, default: 0) - Number of items to skip for pagination- `sort_order` (enum, default: `desc`) - Sort order: `asc`, `desc`

- `limit` (int, default: 20, max: 100) - Number of items per page

- `search` (string, optional) - Search in prayer content**Response** (200 OK) - `PrayerListOut`:

- `is_answered` (boolean, optional) - Filter by answered status

- `is_flagged` (boolean, optional) - Filter by flagged status```json

- `status` (enum, optional) - Filter by status: `pending`, `approved`, `rejected`, `archived`{

- `created_after` (datetime, optional) - Filter prayers created after this date  "items": [

- `created_before` (datetime, optional) - Filter prayers created before this date    {

- `sort_by` (enum, default: `created_at`) - Sort field: `created_at`, `is_answered`, `is_flagged`      "id": 1,

- `sort_order` (enum, default: `desc`) - Sort order: `asc`, `desc`      "title": null,

      "content": "Please pray for healing",

**Response** (200 OK) - `PrayerListOut`:      "created_at": "2025-11-12T13:15:25.423851",

```json      "is_answered": false,

{      "is_flagged": false,

  "items": [      "status": "approved",

    {      "owner_id": null,

      "id": 1,      "submitter_name": "Jane Doe",

      "title": null,      "phone_number": null,

      "content": "Please pray for healing",      "is_anonymous": false

      "created_at": "2025-11-12T13:15:25.423851",    }

      "is_answered": false,  ],

      "is_flagged": false,  "total": 1,

      "status": "approved",  "has_more": false

      "owner_id": null,}

      "submitter_name": "Jane Doe",```

      "phone_number": null,

      "is_anonymous": false**Example**:

    }

  ],```powershell

  "total": 1,# Basic request

  "has_more": falsecurl "http://127.0.0.1:8000/prayers/wall?skip=0&limit=10"

}

```# With filters

curl "http://127.0.0.1:8000/prayers/wall?skip=0&limit=10&search=healing&status=approved"

**Example**:```

```powershell

# Basic request#### POST `/prayers/` 🔒 Protected

curl "http://127.0.0.1:8000/prayers/wall?skip=0&limit=10"

Create a prayer request as an authenticated user.

# With filters

curl "http://127.0.0.1:8000/prayers/wall?skip=0&limit=10&search=healing&status=approved"**Authentication**: Bearer token required

````

**Request Body** (`PrayerCreate`):

#### POST `/prayers/` 🔒

```````json

Create a prayer request as an authenticated user.{

  "title": "Healing Request",

**Request Body** (`PrayerCreate`):  "content": "Please pray for complete recovery",

```json  "submitter_name": null,

{  "phone_number": null,

  "title": "Healing Request",  "is_anonymous": false

  "content": "Please pray for complete recovery",}

  "submitter_name": null,```

  "phone_number": null,

  "is_anonymous": false**Response** (201 Created) - `PrayerOut`:

}

``````json

{

**Response** (201 Created) - `PrayerOut`  "id": 2,

  "title": "Healing Request",

**Example**:  "content": "Please pray for complete recovery",

```powershell  "created_at": "2025-11-12T14:20:15.123456",

curl -X POST "http://127.0.0.1:8000/prayers/" `  "is_answered": false,

  -H "Authorization: Bearer <YOUR_TOKEN>" `  "is_flagged": false,

  -H "Content-Type: application/json" `  "status": "pending",

  -d '{"title":"Healing","content":"Please pray for recovery"}'  "owner_id": 1,

```  "submitter_name": null,

  "phone_number": null,

#### GET `/prayers/` 🔒  "is_anonymous": false

}

Get list of prayers created by the authenticated user.```



**Response** (200 OK) - `List[PrayerOut]`**Example**:



#### PATCH `/prayers/{prayer_id}` 🔒```powershell

curl -X POST "http://127.0.0.1:8000/prayers/" `

Update a prayer request (status, flags, or answered state).  -H "Authorization: Bearer <YOUR_TOKEN>" `

  -H "Content-Type: application/json" `

**Authorization**:   -d '{"title":"Healing","content":"Please pray for recovery"}'

- Regular users can only update their own prayers (limited fields)```

- Admins can update any prayer (all fields)

#### GET `/prayers/` 🔒 Protected

**Path Parameters**:

- `prayer_id` (int) - ID of the prayer to updateGet list of prayers created by the authenticated user.



**Request Body** (`PrayerUpdate`):**Authentication**: Bearer token required

```json

{**Response** (200 OK) - `List[PrayerOut]`:

  "is_answered": true,

  "is_flagged": false,```json

  "status": "approved"[

}  {

```    "id": 2,

    "title": "My Prayer",

**Response** (200 OK) - `PrayerOut` (updated prayer)    "content": "Please pray for me",

    "created_at": "2025-11-12T14:20:15.123456",

**Errors**:    "is_answered": false,

- `403 Forbidden`: Not authorized to update this prayer    "is_flagged": false,

- `404 Not Found`: Prayer not found    "status": "approved",

    "owner_id": 1,

**Example**:    "submitter_name": null,

```powershell    "phone_number": null,

curl -X PATCH "http://127.0.0.1:8000/prayers/1" `    "is_anonymous": false

  -H "Authorization: Bearer <YOUR_TOKEN>" `  }

  -H "Content-Type: application/json" `]

  -d '{"is_answered":true}'```

```````

#### PATCH `/prayers/{prayer_id}` 🔒 Protected

#### GET `/prayers/moderation` 👮

Update a prayer request (status, flags, or answered state).

Get prayers requiring moderation (defaults to pending status).

**Authentication**: Bearer token required

**Query Parameters**: Same as `/prayers/wall` (skip, limit, filters)**Authorization**:

**Response** (200 OK) - `PrayerListOut`- Regular users can only update their own prayers (limited fields)

- Admins can update any prayer (all fields)

**Errors**:

- `403 Forbidden`: User is not an admin**Path Parameters**:

---- `prayer_id` (int) - ID of the prayer to update

### Admin Routes (`/admin`)**Request Body** (`PrayerUpdate`):

All admin routes require authentication with an admin user account.```json

{

#### GET `/admin/prayers` 👮 "is_answered": true,

"is_flagged": false,

Get paginated list of all prayers (admin view). "status": "approved"

}

**Query Parameters**:```

- `page` (int, default: 1) - Page number

- `page_size` (int, default: 20) - Items per page**Response** (200 OK) - `PrayerOut` (updated prayer)

**Response** (200 OK) - `PrayerListOut`**Errors**:

**Example**:- `403 Forbidden`: Not authorized to update this prayer

```powershell- `404 Not Found`: Prayer not found

curl "http://127.0.0.1:8000/admin/prayers?page=1&page_size=20" `

-H "Authorization: Bearer <ADMIN_TOKEN>"**Example**:

````

```powershell

#### PATCH `/admin/prayers/{prayer_id}/answered` 👮curl -X PATCH "http://127.0.0.1:8000/prayers/1" `

  -H "Authorization: Bearer <YOUR_TOKEN>" `

Mark a prayer as answered or unanswered.  -H "Content-Type: application/json" `

  -d '{"is_answered":true}'

**Path Parameters**:```

- `prayer_id` (int) - ID of the prayer

#### GET `/prayers/moderation` 🔒 Admin Only

**Query Parameters**:

- `answered` (boolean, default: true) - Whether to mark as answeredGet prayers requiring moderation (defaults to pending status).



**Response** (200 OK) - `PrayerOut` (updated prayer)**Authentication**: Bearer token required (admin)



**Example**:**Query Parameters**: Same as `/prayers/wall` (skip, limit, filters)

```powershell

# Mark as answered**Response** (200 OK) - `PrayerListOut`

curl -X PATCH "http://127.0.0.1:8000/admin/prayers/1/answered?answered=true" `

  -H "Authorization: Bearer <ADMIN_TOKEN>"**Errors**:

````

- `403 Forbidden`: User is not an admin

#### DELETE `/admin/prayers/{prayer_id}` 👮

---

Delete a prayer request.

### Admin Routes (`/admin`)

**Path Parameters**:

- `prayer_id` (int) - ID of the prayer to deleteAll admin routes require authentication with an admin user account.

**Response** (200 OK):#### GET `/admin/prayers` 🔒 Admin Only

```json

{Get paginated list of all prayers (admin view).

  "detail": "Prayer deleted"

}**Authentication**: Bearer token required (admin)

```

**Query Parameters**:

---

- `page` (int, default: 1) - Page number

## Data Schemas- `page_size` (int, default: 20) - Items per page

All request and response bodies use Pydantic models defined in `app/schemas.py`. As of Pydantic v2, all models use `ConfigDict(from_attributes=True)` for ORM compatibility.**Response** (200 OK) - `PrayerListOut`

### User Schemas**Example**:

#### `UserCreate````powershell

```pythoncurl "http://127.0.0.1:8000/admin/prayers?page=1&page_size=20" `

{ -H "Authorization: Bearer <ADMIN_TOKEN>"

"email": "user@example.com", # EmailStr (validated email format)```

"password": "SecurePass123!", # str (min 8 chars recommended)

"full_name": "John Doe" # Optional[str]#### PATCH `/admin/prayers/{prayer_id}/answered` 🔒 Admin Only

}

````Mark a prayer as answered or unanswered.



#### `UserOut`**Authentication**: Bearer token required (admin)

```python

{**Path Parameters**:

  "id": 1,                          # int

  "email": "user@example.com",      # EmailStr- `prayer_id` (int) - ID of the prayer

  "full_name": "John Doe",          # Optional[str]

  "is_active": true,                # bool**Query Parameters**:

  "is_admin": false                 # bool

}- `answered` (boolean, default: true) - Whether to mark as answered

````

**Response** (200 OK) - `PrayerOut` (updated prayer)

### Prayer Schemas

**Errors**:

#### `PrayerCreate`

```python- `404 Not Found`: Prayer not found

{

"title": "Prayer Title", # Optional[str]**Example**:

"content": "Prayer text...", # str (required)

"submitter_name": "Jane", # Optional[str]```powershell

"phone_number": "555-1234", # Optional[str]# Mark as answered

"is_anonymous": false # Optional[bool] (default: False)curl -X PATCH "http://127.0.0.1:8000/admin/prayers/1/answered?answered=true" `

} -H "Authorization: Bearer <ADMIN_TOKEN>"

```

# Mark as unanswered

#### `PrayerPublicIn`curl -X PATCH "http://127.0.0.1:8000/admin/prayers/1/answered?answered=false" `

Frontend-friendly schema for public prayer submissions.  -H "Authorization: Bearer <ADMIN_TOKEN>"

```

````python

{#### DELETE `/admin/prayers/{prayer_id}` 🔒 Admin Only

  "name": "Jane Doe",               # Optional[str]

  "phoneNumber": "555-1234",        # Optional[str]Delete a prayer request.

  "prayerRequest": "Prayer text",   # str (required)

  "keepAnonymous": false            # Optional[bool] (default: False)**Authentication**: Bearer token required (admin)

}

```**Path Parameters**:



#### `PrayerOut`- `prayer_id` (int) - ID of the prayer to delete

```python

{**Response** (200 OK):

  "id": 1,                          # int

  "title": "Prayer Title",          # Optional[str]```json

  "content": "Prayer text...",      # str{

  "created_at": "2025-11-12T...",   # datetime (ISO 8601 format)  "detail": "Prayer deleted"

  "is_answered": false,             # bool}

  "is_flagged": false,              # bool```

  "status": "pending",              # str (enum: pending|approved|rejected|archived)

  "owner_id": 1,                    # Optional[int] (null for public submissions)**Errors**:

  "submitter_name": "Jane",         # Optional[str]

  "phone_number": "555-1234",       # Optional[str]- `404 Not Found`: Prayer not found

  "is_anonymous": false             # Optional[bool]

}**Example**:

````

````powershell

#### `PrayerUpdate`curl -X DELETE "http://127.0.0.1:8000/admin/prayers/1" `

```python  -H "Authorization: Bearer <ADMIN_TOKEN>"

{```

  "is_answered": true,              # Optional[bool]

  "is_flagged": false,              # Optional[bool]---

  "status": "approved"              # Optional[PrayerStatus] (enum)

}## Data Schemas

````

All request and response bodies use Pydantic models defined in `app/schemas.py`. As of Pydantic v2, all models use `ConfigDict(from_attributes=True)` for ORM compatibility.

#### `PrayerListOut`

```````python### User Schemas

{

  "items": [/* Array of PrayerOut */],  # List[PrayerOut]#### `UserCreate`

  "total": 42,                           # int (total count)

  "has_more": true                       # bool (more items available)Used for user registration.

}

``````python

{

### Enums  "email": "user@example.com",      # EmailStr (validated email format)

  "password": "SecurePass123!",     # str (min 8 chars recommended)

#### `PrayerStatus`  "full_name": "John Doe"           # Optional[str]

```python}

"pending"      # Awaiting moderation```

"approved"     # Approved for display

"rejected"     # Not approved#### `UserOut`

"archived"     # Archived/hidden

```Returned when fetching user information (password excluded).



#### `PrayerSortField````python

```python{

"created_at"  "id": 1,                          # int

"is_answered"  "email": "user@example.com",      # EmailStr

"is_flagged"  "full_name": "John Doe",          # Optional[str]

```  "is_active": true,                # bool

  "is_admin": false                 # bool

#### `SortOrder`}

```python```

"asc"   # Ascending

"desc"  # Descending### Prayer Schemas

```````

#### `PrayerCreate`

### Authentication Schemas

Used by authenticated users to create prayers.

#### `Token`

`python`python

{{

"access_token": "eyJhbGciOi...", # str (JWT token) "title": "Prayer Title", # Optional[str]

"token_type": "bearer" # str (always "bearer") "content": "Prayer text...", # str (required)

} "submitter_name": "Jane", # Optional[str]

```"phone_number": "555-1234",       # Optional[str]

  "is_anonymous": false             # Optional[bool] (default: False)

---}

```

## Error Responses

#### `PrayerPublicIn`

### Status Codes

Frontend-friendly schema for public prayer submissions.

| Code | Meaning | When It Occurs |

|------|---------|----------------|```python

| 200 | OK | Successful GET/PATCH/DELETE request |{

| 201 | Created | Successful POST request (resource created) | "name": "Jane Doe", # Optional[str]

| 400 | Bad Request | Validation errors, invalid input data | "phoneNumber": "555-1234", # Optional[str]

| 401 | Unauthorized | Missing/invalid/expired token, incorrect credentials | "prayerRequest": "Prayer text", # str (required)

| 403 | Forbidden | Insufficient permissions | "keepAnonymous": false # Optional[bool] (default: False)

| 404 | Not Found | Resource not found |}

| 422 | Unprocessable Entity | Pydantic validation errors |```

| 500 | Internal Server Error | Unexpected server error |

| 503 | Service Unavailable | Database connection failed |**Field Mapping**:

### Error Format- `prayerRequest` → `content`

- `name` → `submitter_name` (null if `keepAnonymous` is true)

```json- `phoneNumber`→`phone_number`(null if`keepAnonymous` is true)

{- `keepAnonymous` → `is_anonymous`

"detail": "Error message describing what went wrong"

}#### `PrayerOut`

````

Returned when fetching prayer data.

### Example Errors

```python

**401 Unauthorized**:{

```json  "id": 1,                          # int

{  "title": "Prayer Title",          # Optional[str]

  "detail": "Incorrect username or password"  "content": "Prayer text...",      # str

}  "created_at": "2025-11-12T...",   # datetime (ISO 8601 format)

```  "is_answered": false,             # bool

  "is_flagged": false,              # bool

**403 Forbidden**:  "status": "pending",              # str (enum: pending|approved|rejected|archived)

```json  "owner_id": 1,                    # Optional[int] (null for public submissions)

{  "submitter_name": "Jane",         # Optional[str]

  "detail": "Not authorized to perform this action"  "phone_number": "555-1234",       # Optional[str]

}  "is_anonymous": false             # Optional[bool]

```}

````

**422 Validation Error**:

```json#### `PrayerUpdate`

{

"detail": [Used to update prayer properties.

    {

      "loc": ["body", "email"],```python

      "msg": "value is not a valid email address",{

      "type": "value_error.email"  "is_answered": true,              # Optional[bool]

    }  "is_flagged": false,              # Optional[bool]

] "status": "approved" # Optional[PrayerStatus] (enum)

}}

````



---#### `PrayerListOut`



## TestingPaginated list response.



### Automated Smoke Test```python

{

The backend includes an automated smoke test script (`test_api.py`) that validates:  "items": [/* Array of PrayerOut */],  # List[PrayerOut]

1. ✅ Authentication (token endpoint)  "total": 42,                           # int (total count)

2. ✅ Prayer submission (public endpoint)  "has_more": true                       # bool (more items available)

3. ✅ Prayer wall retrieval (paginated list)}

4. ✅ Prayer appears in wall after submission```



**Running the Smoke Test**:#### `PrayerFilter`



```powershellQuery parameters for filtering prayers.

cd backend

python test_api.py --username admin@prayerwall.com --password Prayer123!```python

```{

  "search": "healing",                   # Optional[str]

**Optional Arguments**:  "is_answered": false,                  # Optional[bool]

- `--username` - Admin email (default: admin@prayerwall.com)  "is_flagged": false,                   # Optional[bool]

- `--password` - Admin password (default: Prayer123!)  "status": "approved",                  # Optional[PrayerStatus]

- `--base-url` - API base URL (default: http://127.0.0.1:8000)  "created_after": "2025-11-01T...",     # Optional[datetime]

  "created_before": "2025-11-30T...",    # Optional[datetime]

**Expected Output**:  "sort_by": "created_at",               # Optional[PrayerSortField]

```  "sort_order": "desc"                   # Optional[SortOrder]

Token received}

Submitting prayer...```

Prayer submitted: {'id': 1, 'content': '...', ...}

Fetched prayer wall, total items: 1### Enums

Found submitted prayer in wall (id= 1 )

Smoke test completed successfully.#### `PrayerStatus`

```

```python

---enum PrayerStatus {

  PENDING = "pending"      # Awaiting moderation

## Deployment  APPROVED = "approved"    # Approved for display

  REJECTED = "rejected"    # Not approved

### Environment Variables  ARCHIVED = "archived"    # Archived/hidden

}

| Variable | Description | Required | Example |```

|----------|-------------|----------|---------|

| `DATABASE_URL` | PostgreSQL connection string | Yes | `postgresql://user:pass@host:5432/dbname` |#### `PrayerSortField`

| `SECRET_KEY` | JWT signing key (keep secret!) | Yes | Random 32+ character string |

| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | No | `60` (default) |```python

enum PrayerSortField {

**Generating a Secure SECRET_KEY**:  CREATED_AT = "created_at"

```powershell  IS_ANSWERED = "is_answered"

python -c "import secrets; print(secrets.token_urlsafe(32))"  IS_FLAGGED = "is_flagged"

```}

```

### Vercel Deployment

#### `SortOrder`

The backend includes a `vercel.json` configuration for serverless deployment.

```python

**Steps**:enum SortOrder {

  ASC = "asc"

1. **Configure Environment Variables** in Vercel Dashboard:  DESC = "desc"

   - `DATABASE_URL` → Your production PostgreSQL URL}

   - `SECRET_KEY` → Your generated secret key```

   - `ACCESS_TOKEN_EXPIRE_MINUTES` → `60`

### Authentication Schemas

2. **Deploy via GitHub**:

   - Connect repository to Vercel#### `Token`

   - Import: `https://github.com/Newlife-Community-Devs/newlife-prayer-wall-backend`

   - Deploy automatically on push to `main`Returned after successful authentication.



3. **Database Migration for Production**:```python

{

```sql  "access_token": "eyJhbGciOi...",   # str (JWT token)

ALTER TABLE prayer_requests   "token_type": "bearer"             # str (always "bearer")

ADD COLUMN status VARCHAR DEFAULT 'pending', }

ADD COLUMN submitter_name VARCHAR, ```

ADD COLUMN phone_number VARCHAR,

ADD COLUMN is_anonymous BOOLEAN DEFAULT FALSE;---

```

## Error Responses

### Docker Deployment

The API uses standard HTTP status codes and returns errors in a consistent JSON format.

**Building the Image**:

```powershell### Status Codes

cd backend

docker build -t prayerwall-backend .| Code | Meaning               | When It Occurs                                                       |

```| ---- | --------------------- | -------------------------------------------------------------------- |

| 200  | OK                    | Successful GET/PATCH/DELETE request                                  |

**Running Locally**:| 201  | Created               | Successful POST request (resource created)                           |

```powershell| 400  | Bad Request           | Validation errors, invalid input data                                |

docker run -p 8000:8000 `| 401  | Unauthorized          | Missing/invalid/expired token, incorrect credentials                 |

  -e DATABASE_URL="postgresql://user:pass@host:5432/dbname" `| 403  | Forbidden             | Insufficient permissions (e.g., non-admin accessing admin endpoints) |

  -e SECRET_KEY="your-secret-key" `| 404  | Not Found             | Resource not found (prayer, user, etc.)                              |

  prayerwall-backend| 422  | Unprocessable Entity  | Pydantic validation errors                                           |

```| 500  | Internal Server Error | Unexpected server error (check logs)                                 |

| 503  | Service Unavailable   | Database connection failed                                           |

---

### Error Response Format

## Database Setup

```json

### Schema Overview{

  "detail": "Error message describing what went wrong"

#### `users` Table}

```sql```

CREATE TABLE users (

    id SERIAL PRIMARY KEY,### Common Error Examples

    email VARCHAR UNIQUE NOT NULL,

    hashed_password VARCHAR NOT NULL,**401 Unauthorized - Invalid Credentials**:

    full_name VARCHAR,

    is_active BOOLEAN DEFAULT TRUE,```json

    is_admin BOOLEAN DEFAULT FALSE{

);  "detail": "Incorrect username or password"

```}

```

#### `prayer_requests` Table

```sql**401 Unauthorized - Missing Token**:

CREATE TABLE prayer_requests (

    id SERIAL PRIMARY KEY,```json

    title VARCHAR,{

    content TEXT NOT NULL,  "detail": "Not authenticated"

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,}

    is_answered BOOLEAN DEFAULT FALSE,```

    is_flagged BOOLEAN DEFAULT FALSE,

    status VARCHAR DEFAULT 'pending',**403 Forbidden - Insufficient Permissions**:

    submitter_name VARCHAR,

    phone_number VARCHAR,```json

    is_anonymous BOOLEAN DEFAULT FALSE,{

    owner_id INTEGER REFERENCES users(id)  "detail": "Not authorized to perform this action"

);}

````

### Creating an Admin User**404 Not Found**:

`powershell`json

cd backend{

python create_admin.py create-admin --email admin@prayerwall.com "detail": "Prayer not found"

# Enter password when prompted}

````



**Change Admin Password**:**422 Validation Error**:

```powershell

python create_admin.py change-password --email admin@prayerwall.com```json

```{

  "detail": [

---    {

      "loc": ["body", "email"],

## Development      "msg": "value is not a valid email address",

      "type": "value_error.email"

### Project Structure    }

  ]

```}

backend/```

├── app/

│   ├── main.py              # FastAPI app entry point## Example curl requests

│   ├── auth.py              # JWT & password hashing utilities

│   ├── config.py            # Configuration settings1. Obtain token (PowerShell-friendly):

│   ├── crud.py              # Database CRUD operations

│   ├── database.py          # SQLAlchemy setup```powershell

│   ├── dependencies.py      # FastAPI dependenciescurl -X POST "http://127.0.0.1:8000/auth/token" -H "Content-Type: application/x-www-form-urlencoded" --data "username=admin@prayerwall.com&password=Prayer123!"

│   ├── models.py            # SQLAlchemy ORM models```

│   ├── schemas.py           # Pydantic schemas

│   └── routes/Response:

│       ├── auth.py          # Auth endpoints

│       ├── prayers.py       # Prayer endpoints```json

│       └── admin.py         # Admin endpoints{ "access_token": "<JWT_TOKEN>", "token_type": "bearer" }

├── .env                     # Environment variables (local)```

├── Dockerfile               # Docker container definition

├── vercel.json              # Vercel deployment config2. Submit a public prayer (no auth):

├── requirements.txt         # Python dependencies

├── create_admin.py          # Admin user management CLI```bash

├── test_api.py              # Automated smoke testcurl -X POST "http://127.0.0.1:8000/prayers/submit" -H "Content-Type: application/json" -d '{"name":"Jane","phoneNumber":"555","prayerRequest":"Please pray","keepAnonymous":false}'

└── API_DOCUMENTATION.md     # This file```

```

3. Create a prayer as an authenticated user:

### Key Dependencies

```bash

```curl -X POST "http://127.0.0.1:8000/prayers/" -H "Authorization: Bearer <JWT_TOKEN>" -H "Content-Type: application/json" -d '{"title":"Hello","content":"Pray for me"}'

fastapi>=0.95.0           # Web framework```

uvicorn[standard]>=0.20.0 # ASGI server

sqlalchemy>=1.4           # ORM4. Get paginated prayer wall with filters:

psycopg2-binary>=2.9      # PostgreSQL adapter

passlib==1.7.4            # Password hashing```bash

bcrypt==4.0.1             # bcrypt for passlibcurl "http://127.0.0.1:8000/prayers/wall?skip=0&limit=10&search=healing"

python-jose>=3.3          # JWT handling```

python-multipart>=0.0.6   # Form data parsing

pydantic>=1.10            # Data validation## Notes, tips and implementation details

```

- DB: connection string is `DATABASE_URL` in `backend/.env` (defaults to postgres://... in the example). The project uses SQLAlchemy and `Base.metadata.create_all` at startup to create tables.

### Local Development Workflow- Password hashing: `passlib` with bcrypt in `app.auth` (`CryptContext(schemes=["bcrypt"])`).

- JWT: `python-jose` used for JWT encode/decode.

1. **Clone Repository**:- Pagination: `crud.get_all_prayers_paginated` returns `items, total, has_more`. The API truncates extra row to set `has_more`.

   ```powershell- Admin CLI: `backend/create_admin.py` provides Typer commands to create/change admin users; this is useful for local testing.

   git clone https://github.com/Newlife-Community-Devs/newlife-prayer-wall-backend.git

   cd newlife-prayer-wall-backend/backend## Troubleshooting

   ```

- If `/auth/token` returns 401: confirm user exists (DB) and try resetting the password via `create_admin.py` or the CLI `create-admin`/`change-password` commands. Example:

2. **Create Virtual Environment**:

   ```powershell```powershell

   python -m venv .venvcd newlife-prayer-wall/backend

   .\.venv\Scripts\Activate.ps1.\.venv\Scripts\Activate.ps1

   ```python create_admin.py create-admin --email admin@prayerwall.com

```

3. **Install Dependencies**:

   ```powershell- If DB connection fails, check `backend/.env` and ensure Postgres is running and the database exists.

   pip install -r requirements.txt

   ```## Where to look in code



4. **Configure Environment**:- Routes: `backend/app/routes/*` (`auth.py`, `prayers.py`, `admin.py`)

   ```powershell- Schemas: `backend/app/schemas.py`

   cp .env.example .env- CRUD & models: `backend/app/crud.py`, `backend/app/models.py`

   # Edit .env with your DATABASE_URL and SECRET_KEY- Auth helpers: `backend/app/auth.py`

   ```- DB config: `backend/app/config.py`, `backend/app/database.py`



5. **Create Admin User**:---

   ```powershell

   python create_admin.py create-admin --email admin@prayerwall.comIf you'd like, I can also generate a Postman collection or OpenAPI YAML/JSON exported from the running FastAPI (FastAPI already provides an OpenAPI UI at `/docs` and raw schema at `/openapi.json`). Would you like me to:

   ```

- A) Export an `openapi.json` file into `backend/openapi.json` now, or

6. **Run Server**:- B) Generate a Postman collection wrapper, or

   ```powershell- C) Nothing further — this document is fine?

   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

   ```# PrayerWall Backend API Documentation



7. **Run Tests**:This document describes the backend API implemented in `backend/app`.

   ```powershellIt covers routes, request/response schemas, authentication, examples, and common error responses.

   python test_api.py

   ```Base URL (development): http://127.0.0.1:8000



### CORS Configuration## Authentication



**Development** (current):- Type: JWT (Bearer)

```python- Token endpoint: POST /auth/token

allow_origins=["*"]  # Permissive for development  - Content-Type: application/x-www-form-urlencoded

```  - Form fields: `username` (email), `password`

  - Response: `{ "access_token": "<JWT>", "token_type": "bearer" }`

**Production Recommendation**:  - Notes: Use token in `Authorization: Bearer <token>` header for protected endpoints.

```python

allow_origins=["https://yourdomain.com", "https://www.yourdomain.com"]## Routes and Schemas

```

All routes are mounted under the main app router in `backend/app/routes`.

---

### 1) Auth

## Troubleshooting

#### POST /auth/register

### Database Connection Failed

**Error**: `could not connect to server: Connection refused`- Purpose: Register a new user.

- Request body (JSON):

**Solutions**:  ```json

- Verify PostgreSQL is running  {

- Check `DATABASE_URL` in `.env`    "email": "user@example.com",

- Ensure database exists: `createdb prayerdb`    "password": "Password123!",

    "full_name": "Full Name"

### Import Error  }

**Error**: `ModuleNotFoundError: No module named 'main'`  ```

- Response (201/200): `UserOut`:

**Solution**: Use correct module path:  ```json

```powershell  {

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000    "id": 1,

```    "email": "user@example.com",

    "full_name": "Full Name",

### Form Data Error    "is_active": true,

**Error**: `RuntimeError: Form data requires 'python-multipart'`    "is_admin": false

  }

**Solution**:  ```

```powershell

pip install python-multipart>=0.0.6#### POST /auth/token

```

- Purpose: Obtain JWT access token using username/password (OAuth2 password flow)

### Password Hashing Error- Content-Type: application/x-www-form-urlencoded

**Error**: `ValueError: password cannot be longer than 72 bytes`- Form: `username` (email), `password`

- Response: `Token`:

**Solution**:  ```json

```powershell  { "access_token": "<JWT>", "token_type": "bearer" }

pip install passlib==1.7.4 bcrypt==4.0.1  ```

```- Errors: 401 for incorrect credentials



### Undefined Column Error### 2) Prayers

**Error**: `psycopg2.errors.UndefinedColumn: column "status" does not exist`

#### POST /prayers/ (protected)

**Solution**: Run database migration (see [Database Setup](#database-setup))

- Purpose: Create a prayer request as an authenticated user.

---- Authorization: Bearer token required

- Request body (JSON) `PrayerCreate`:

## Additional Resources  ```json

  {

- **FastAPI Documentation**: https://fastapi.tiangolo.com/    "title": "Optional title",

- **SQLAlchemy ORM**: https://docs.sqlalchemy.org/    "content": "Prayer text",

- **Pydantic V2**: https://docs.pydantic.dev/latest/    "submitter_name": null,

- **JWT Introduction**: https://jwt.io/introduction    "phone_number": null,

- **PostgreSQL Docs**: https://www.postgresql.org/docs/    "is_anonymous": false

  }

---  ```

- Response: `PrayerOut` (created prayer)

## Support & Contributing

#### POST /prayers/submit (public)

- **Repository**: https://github.com/Newlife-Community-Devs/newlife-prayer-wall-backend

- **Issues**: https://github.com/Newlife-Community-Devs/newlife-prayer-wall-backend/issues- Purpose: Submit a prayer from the public frontend modal (no auth required).

- Request body (JSON) `PrayerPublicIn` (frontend keys):

---  ```json

  {

**Maintained by**: Newlife Community Devs    "name": "Jane Doe",

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
````

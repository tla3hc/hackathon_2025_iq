# HTTP API Endpoints in controller.py

This document describes the HTTP endpoints defined in the `Controller` class, including their purpose and the structure of any JSON payloads or responses.

---

## `/` (index)

**Method:** GET
**Description:**
Returns a simple HTML page listing available API endpoints. No JSON payload or response.

---

## `/health`

**Method:** GET
**Description:**
Health check endpoint. Returns server status, current timestamp, and server type.
**Response JSON:**

```json
{
    "status": "healthy",
    "timestamp": <float>,
    "server_type": "HTTP"
}
```

---

## `/login`

**Method:** GET, POST
**Description:**
Handles user authentication. On successful login, connects to the localization server and fetches package list.
**Request (POST form):**

- password: string

**Response JSON:**

```json
{
    "message": <str>
}
```

---

## `/logout`

**Method:** GET
**Description:**
Clears the session and redirects to the login page. No JSON payload or response.

---

## `/road_information`

**Method:** GET
**Description:**
Returns road information from the map server if authenticated.
**Response JSON:**

```json
{
    "points": [list[]],
    "streets" [
        {
            "name": <string>,
            "start": [<int>, <int>],
            "end": [<int>, <int]
        },
        ...
    ]
}
```

---

## `/packages`

**Method:** GET
**Description:**
Returns available packages if authenticated.
**Response JSON:**

```json
{
    <package_id>: {
        "id": <int>,
        "position": [<float>, <float>]
    },
    ...
}
```

---

## `/get_tokens`

**Method:** GET
**Description:**
Returns tokens for the current path node if car is not running and user is authenticated.

---

## `/set_index`

**Method:** POST
**Description:**
Updates the car route based on the provided index if authenticated.
**Request JSON:**

```json
{
    "index": <int>
}
```

**Response JSON:**

```json
{
    "message": <str>
}
```

---

## `/car`

**Method:** GET
**Description:**
Returns the current state, position, orientation, and obstacles of the car if authenticated.
**Response JSON:**

```json
{
    "state": <str>, (e.g. "STOP", "BLOCKED", "MOVE_FORWARD", "MOVE_BACKWARD", "TURN")
    "position": [<float>, <float>],
    "orientation": <float>,
    "obstacles": <list>
}
```

---

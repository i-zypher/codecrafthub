# CodeCraftHub API: Test Cases

20 copy-and-paste tests covering every endpoint, successful operations, and error scenarios.

## Before you start

1. **Start the server** in one terminal: `python app.py`
2. **Open a second terminal** for the tests (the first one is busy running the server).
3. **Start with a clean slate** so the IDs match the expected responses below. Stop the server, delete `courses.json`, then start the server again.
4. **Put the `tests` folder inside your `codecrafthub` folder**, and run every command from the `codecrafthub` folder.

```
codecrafthub/
├── app.py
├── courses.json
├── TESTING.md
└── tests/
    ├── new_course.json
    ├── new_course_2.json
    ├── update_course.json
    ├── update_bad_status.json
    ├── missing_fields.json
    ├── bad_status.json
    ├── bad_date.json
    └── empty_name.json
```

### Why the JSON lives in separate files

Typing JSON directly into a curl command breaks easily on Windows, because PowerShell and Command Prompt each handle quotes differently. Putting the JSON in a file and passing it with `-d "@tests/file.json"` works the same in every terminal.

### Which curl command to type

| Terminal | Command |
|---|---|
| **PowerShell** (VS Code default on Windows) | `curl.exe` (plain `curl` runs a different PowerShell command) |
| Command Prompt, Git Bash, Mac, Linux | `curl` |

Commands below use `curl.exe`. On Mac or Linux, drop the `.exe`.

### What the flags mean

| Flag | Meaning |
|---|---|
| `-i` | Show the response headers, including the status code (`200 OK`, `404 NOT FOUND`, etc.) |
| `-X POST` | Which HTTP method to use. Without `-X`, curl sends a GET. |
| `-H "Content-Type: application/json"` | Tells Flask the body is JSON |
| `-d "@tests/file.json"` | Send the contents of that file as the request body. Keep the quotes: in PowerShell, an unquoted `@` means something else. |

> **Note:** `created_at` in your responses will show the time you ran the test, not the times below. Everything else should match exactly.

---

## Part 1: Successful operations

Run these in order. Later tests depend on courses created by earlier ones.

### Test 1: Check the server is running

```
curl.exe -i http://127.0.0.1:5000/
```

**Expected:** `200 OK`

```json
{
  "message": "CodeCraftHub API is running"
}
```

### Test 2: Get all courses (empty)

```
curl.exe -i http://127.0.0.1:5000/api/courses
```

**Expected:** `200 OK`

```json
[]
```

### Test 3: Add a course

Payload (`tests/new_course.json`):

```json
{
  "name": "Python Basics",
  "description": "Learn Python fundamentals",
  "target_date": "2026-12-31",
  "status": "In Progress"
}
```

```
curl.exe -i -X POST http://127.0.0.1:5000/api/courses -H "Content-Type: application/json" -d "@tests/new_course.json"
```

**Expected:** `201 CREATED`

```json
{
  "created_at": "2026-09-27T07:39:32",
  "description": "Learn Python fundamentals",
  "id": 1,
  "name": "Python Basics",
  "status": "In Progress",
  "target_date": "2026-12-31"
}
```

### Test 4: Add a second course

Payload (`tests/new_course_2.json`):

```json
{
  "name": "Flask REST APIs",
  "description": "Build APIs with Flask",
  "target_date": "2027-01-31",
  "status": "Not Started"
}
```

```
curl.exe -i -X POST http://127.0.0.1:5000/api/courses -H "Content-Type: application/json" -d "@tests/new_course_2.json"
```

**Expected:** `201 CREATED`

```json
{
  "created_at": "2026-09-27T07:39:32",
  "description": "Build APIs with Flask",
  "id": 2,
  "name": "Flask REST APIs",
  "status": "Not Started",
  "target_date": "2027-01-31"
}
```

### Test 5: Get all courses

```
curl.exe -i http://127.0.0.1:5000/api/courses
```

**Expected:** `200 OK`, a list with both courses

```json
[
  {
    "created_at": "2026-09-27T07:39:32",
    "description": "Learn Python fundamentals",
    "id": 1,
    "name": "Python Basics",
    "status": "In Progress",
    "target_date": "2026-12-31"
  },
  {
    "created_at": "2026-09-27T07:39:32",
    "description": "Build APIs with Flask",
    "id": 2,
    "name": "Flask REST APIs",
    "status": "Not Started",
    "target_date": "2027-01-31"
  }
]
```

### Test 6: Get one course

```
curl.exe -i http://127.0.0.1:5000/api/courses/1
```

**Expected:** `200 OK`

```json
{
  "created_at": "2026-09-27T07:39:32",
  "description": "Learn Python fundamentals",
  "id": 1,
  "name": "Python Basics",
  "status": "In Progress",
  "target_date": "2026-12-31"
}
```

### Test 7: Update a course

Only the fields you send are changed. Everything else stays the same.

Payload (`tests/update_course.json`):

```json
{
  "status": "Completed",
  "description": "Finished all Python fundamentals modules"
}
```

```
curl.exe -i -X PUT http://127.0.0.1:5000/api/courses/1 -H "Content-Type: application/json" -d "@tests/update_course.json"
```

**Expected:** `200 OK`. `status` and `description` changed, and `id`, `name`, `target_date`, and `created_at` did not.

```json
{
  "created_at": "2026-09-27T07:39:32",
  "description": "Finished all Python fundamentals modules",
  "id": 1,
  "name": "Python Basics",
  "status": "Completed",
  "target_date": "2026-12-31"
}
```

### Test 8: Delete a course

```
curl.exe -i -X DELETE http://127.0.0.1:5000/api/courses/2
```

**Expected:** `200 OK`

```json
{
  "message": "Course 2 deleted"
}
```

### Test 9: Confirm the delete

```
curl.exe -i http://127.0.0.1:5000/api/courses
```

**Expected:** `200 OK`, only course 1 remains

```json
[
  {
    "created_at": "2026-09-27T07:39:32",
    "description": "Finished all Python fundamentals modules",
    "id": 1,
    "name": "Python Basics",
    "status": "Completed",
    "target_date": "2026-12-31"
  }
]
```

---

## Part 2: Error scenarios

These should all fail on purpose. A passing test here means the API **rejects** the bad request with the right status code and a clear message, and doesn't save anything.

### Test 10: Missing required fields

Payload (`tests/missing_fields.json`):

```json
{
  "name": "Incomplete Course"
}
```

```
curl.exe -i -X POST http://127.0.0.1:5000/api/courses -H "Content-Type: application/json" -d "@tests/missing_fields.json"
```

**Expected:** `400 BAD REQUEST`, listing every missing field

```json
{
  "error": "Missing required field(s): description, target_date, status"
}
```

### Test 11: Invalid status value

Payload (`tests/bad_status.json`):

```json
{
  "name": "Bad Status Course",
  "description": "Status is not allowed",
  "target_date": "2026-12-31",
  "status": "Kinda Started"
}
```

```
curl.exe -i -X POST http://127.0.0.1:5000/api/courses -H "Content-Type: application/json" -d "@tests/bad_status.json"
```

**Expected:** `400 BAD REQUEST`

```json
{
  "error": "'status' must be one of: Not Started, In Progress, Completed"
}
```

### Test 12: Invalid date format

Payload (`tests/bad_date.json`):

```json
{
  "name": "Bad Date Course",
  "description": "Date is in the wrong format",
  "target_date": "12/31/2026",
  "status": "Not Started"
}
```

```
curl.exe -i -X POST http://127.0.0.1:5000/api/courses -H "Content-Type: application/json" -d "@tests/bad_date.json"
```

**Expected:** `400 BAD REQUEST`

```json
{
  "error": "'target_date' must be a valid date in YYYY-MM-DD format"
}
```

### Test 13: Blank name

Payload (`tests/empty_name.json`), where the name is only spaces:

```json
{
  "name": "   ",
  "description": "Name is only spaces",
  "target_date": "2026-12-31",
  "status": "Not Started"
}
```

```
curl.exe -i -X POST http://127.0.0.1:5000/api/courses -H "Content-Type: application/json" -d "@tests/empty_name.json"
```

**Expected:** `400 BAD REQUEST`

```json
{
  "error": "'name' must be a non-empty string"
}
```

### Test 14: Body is not JSON

```
curl.exe -i -X POST http://127.0.0.1:5000/api/courses -H "Content-Type: application/json" -d "this is not json"
```

**Expected:** `400 BAD REQUEST`

```json
{
  "error": "Request body must be valid JSON"
}
```

### Test 15: Update with an invalid status

Payload (`tests/update_bad_status.json`):

```json
{
  "status": "Done-ish"
}
```

```
curl.exe -i -X PUT http://127.0.0.1:5000/api/courses/1 -H "Content-Type: application/json" -d "@tests/update_bad_status.json"
```

**Expected:** `400 BAD REQUEST`. Course 1 keeps its `Completed` status (check with Test 6).

```json
{
  "error": "'status' must be one of: Not Started, In Progress, Completed"
}
```

### Test 16: Get a course that doesn't exist

```
curl.exe -i http://127.0.0.1:5000/api/courses/999
```

**Expected:** `404 NOT FOUND`

```json
{
  "error": "Course 999 not found"
}
```

### Test 17: Update a course that doesn't exist

```
curl.exe -i -X PUT http://127.0.0.1:5000/api/courses/999 -H "Content-Type: application/json" -d "@tests/update_course.json"
```

**Expected:** `404 NOT FOUND`

```json
{
  "error": "Course 999 not found"
}
```

### Test 18: Delete a course that doesn't exist

```
curl.exe -i -X DELETE http://127.0.0.1:5000/api/courses/999
```

**Expected:** `404 NOT FOUND`

```json
{
  "error": "Course 999 not found"
}
```

### Test 19: Endpoint that doesn't exist

```
curl.exe -i http://127.0.0.1:5000/api/nope
```

**Expected:** `404 NOT FOUND`

```json
{
  "error": "Endpoint not found"
}
```

### Test 20: Wrong HTTP method

The API has no `PATCH` route.

```
curl.exe -i -X PATCH http://127.0.0.1:5000/api/courses/1
```

**Expected:** `405 METHOD NOT ALLOWED`

```json
{
  "error": "Method not allowed on this endpoint"
}
```

---

## Results checklist

| # | Test | Expected status | Pass? |
|---|---|---|---|
| 1 | Server running | 200 | |
| 2 | Get all (empty) | 200 | |
| 3 | Add course | 201 | |
| 4 | Add second course | 201 | |
| 5 | Get all | 200 | |
| 6 | Get one | 200 | |
| 7 | Update course | 200 | |
| 8 | Delete course | 200 | |
| 9 | Confirm delete | 200 | |
| 10 | Missing fields | 400 | |
| 11 | Invalid status | 400 | |
| 12 | Invalid date | 400 | |
| 13 | Blank name | 400 | |
| 14 | Body not JSON | 400 | |
| 15 | Update with invalid status | 400 | |
| 16 | Get missing course | 404 | |
| 17 | Update missing course | 404 | |
| 18 | Delete missing course | 404 | |
| 19 | Unknown endpoint | 404 | |
| 20 | Wrong method | 405 | |

## Troubleshooting

| Problem | Cause and fix |
|---|---|
| `Failed to connect to 127.0.0.1 port 5000` | The server isn't running. Start it with `python app.py` in another terminal. |
| `Warning: Couldn't read data from file` | You're not in the `codecrafthub` folder, or the `tests` folder is missing. Run `cd` to the project folder. |
| PowerShell asks for `Uri:` or shows a red parameter error | You typed `curl` instead of `curl.exe`. |
| IDs don't match the expected responses | Old data is still in `courses.json`. Stop the server, delete the file, restart, and run from Test 1. |
| The response is an HTML page instead of JSON | The server is running an older `app.py`. Stop it (`Ctrl+C`), save, and restart. |

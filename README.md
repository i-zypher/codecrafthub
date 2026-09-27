# CodeCraftHub

A simple REST API for tracking the courses you want to learn. Built with Python and Flask, with all data stored in a plain JSON file, so there's no database to set up.

CodeCraftHub is a learning project. It's small enough to read in one sitting, and it covers the core ideas behind almost every web API: HTTP methods, endpoints, JSON request and response bodies, status codes, validation, and error handling.

---

## Table of contents

1. [Project overview](#project-overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Running the application](#running-the-application)
5. [API endpoints](#api-endpoints)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)
8. [Project structure](#project-structure)
9. [Limitations and next steps](#limitations-and-next-steps)

---

## Project overview

### What it does

CodeCraftHub lets you keep a list of courses you plan to take. For each course it tracks:

| Field | Description | Example |
|---|---|---|
| `id` | Unique number, assigned automatically | `1` |
| `name` | Course name | `"Python Basics"` |
| `description` | What the course covers | `"Learn Python fundamentals"` |
| `target_date` | When you want to finish, in `YYYY-MM-DD` format | `"2026-12-31"` |
| `status` | One of `Not Started`, `In Progress`, or `Completed` | `"In Progress"` |
| `created_at` | When the course was added, set automatically | `"2026-09-27T07:39:32"` |

There's no website or user interface. You talk to it by sending HTTP requests, the same way a mobile app or web front end would talk to a real backend.

### New to REST APIs? Start here

A **REST API** is a program that lets other programs work with data over HTTP. It uses four main ideas:

- **Resources** are the things you're managing. Here, that's courses.
- **Endpoints** are the URLs where resources live, like `/api/courses` for all courses or `/api/courses/1` for course number 1.
- **HTTP methods** say what you want to do:

  | Method | Action | CRUD name |
  |---|---|---|
  | `POST` | Create something new | **C**reate |
  | `GET` | Read data | **R**ead |
  | `PUT` | Change existing data | **U**pdate |
  | `DELETE` | Remove data | **D**elete |

- **Status codes** are numbers in every response that say how it went. `2xx` means success, `4xx` means the request had a problem, and `5xx` means the server had a problem.

---

## Features

- **Full CRUD** for courses: create, read all, read one, update, and delete
- **JSON file storage** in `courses.json`, created automatically on first run
- **Validation** of every field:
  - all fields required when creating a course
  - `name` and `description` can't be blank
  - `target_date` must be a real date in `YYYY-MM-DD` format
  - `status` must be exactly `Not Started`, `In Progress`, or `Completed`
- **Partial updates**: send only the fields you want to change
- **Clear JSON errors** for every failure, including unknown URLs and wrong methods
- **Safe file handling**:
  - saves are written to a temporary file first, so a crash mid-save can't corrupt your data
  - a corrupted `courses.json` returns an error instead of being silently overwritten
- **Beginner-friendly code**: one file, with comments explaining each part

---

## Installation

### Requirements

- **Python 3.9 or newer.** Check with `python --version` (Windows) or `python3 --version` (Mac/Linux).
- **A code editor.** These instructions use [VS Code](https://code.visualstudio.com/).
- **curl**, for testing. It's built into Windows 10 and 11, macOS, and most Linux systems.

If you don't have Python, download it from [python.org](https://www.python.org/downloads/). On Windows, check **"Add Python to PATH"** on the installer's first screen.

### Step 1: Get the project files

Put `app.py`, `requirements.txt`, and this README in a folder called `codecrafthub`, then open that folder in VS Code (**File → Open Folder**).

### Step 2: Open a terminal

In VS Code, press `` Ctrl+` `` (the backtick key, next to `1`). The terminal should open in your `codecrafthub` folder.

### Step 3: Create a virtual environment

A virtual environment keeps this project's packages separate from everything else on your computer.

**Windows:**

```bash
python -m venv venv
```

**Mac/Linux:**

```bash
python3 -m venv venv
```

### Step 4: Activate the virtual environment

**Windows (PowerShell):**

```powershell
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

You'll see `(venv)` at the start of your terminal prompt. You need to activate it again every time you open a new terminal.

> **Windows tip:** If PowerShell says running scripts is disabled, run this once, then try again:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

This installs Flask and the packages it depends on. Check that it worked:

```bash
pip show flask
```

It should print a version number.

---

## Running the application

With the virtual environment active, run:

**Windows:**

```bash
python app.py
```

**Mac/Linux:**

```bash
python3 app.py
```

You should see something like:

```
Data file: C:\codecrafthub\courses.json
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

Open **http://127.0.0.1:5000/** in your browser. You should see:

```json
{
  "message": "CodeCraftHub API is running"
}
```

The server keeps running until you stop it with `Ctrl+C`. While it's running, that terminal is busy, so open a second terminal (the **+** button on the terminal panel) to send requests.

**Debug mode** is on, so Flask restarts automatically when you save `app.py` and shows detailed error pages. That's useful while learning, but it should never be used on a real public server.

---

## API endpoints

**Base URL:** `http://127.0.0.1:5000`

| Method | Endpoint | Description | Success code |
|---|---|---|---|
| `GET` | `/` | Check the server is running | `200 OK` |
| `POST` | `/api/courses` | Add a new course | `201 Created` |
| `GET` | `/api/courses` | Get all courses | `200 OK` |
| `GET` | `/api/courses/<id>` | Get one course | `200 OK` |
| `PUT` | `/api/courses/<id>` | Update a course | `200 OK` |
| `DELETE` | `/api/courses/<id>` | Delete a course | `200 OK` |

> **Windows users:** In PowerShell, type `curl.exe`, not `curl`. Plain `curl` runs a different PowerShell command. In Command Prompt, Git Bash, Mac, or Linux, plain `curl` is fine.
>
> The `-i` flag shows the status code in the response. The examples below send JSON from files in the `tests` folder. See [Testing](#testing) for why.

### Add a course

`POST /api/courses`

All four fields are required. `id` and `created_at` are generated by the server.

**Request body:**

```json
{
  "name": "Python Basics",
  "description": "Learn Python fundamentals",
  "target_date": "2026-12-31",
  "status": "In Progress"
}
```

**Command:**

```bash
curl.exe -i -X POST http://127.0.0.1:5000/api/courses -H "Content-Type: application/json" -d "@tests/new_course.json"
```

**Response:** `201 Created`

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

**Possible errors:** `400` for missing fields, a blank name or description, an invalid date, an invalid status, or a body that isn't JSON.

### Get all courses

`GET /api/courses`

```bash
curl.exe -i http://127.0.0.1:5000/api/courses
```

**Response:** `200 OK`. This is a list, and it's `[]` when there are no courses.

```json
[
  {
    "created_at": "2026-09-27T07:39:32",
    "description": "Learn Python fundamentals",
    "id": 1,
    "name": "Python Basics",
    "status": "In Progress",
    "target_date": "2026-12-31"
  }
]
```

You can also open this URL in your browser, because browsers send GET requests.

### Get one course

`GET /api/courses/<id>`

```bash
curl.exe -i http://127.0.0.1:5000/api/courses/1
```

**Response:** `200 OK`, a single course object.

**Possible errors:** `404` if no course has that ID.

```json
{
  "error": "Course 999 not found"
}
```

### Update a course

`PUT /api/courses/<id>`

Send only the fields you want to change. Anything you leave out stays the same. `id` and `created_at` can't be changed.

**Request body:**

```json
{
  "status": "Completed",
  "description": "Finished all Python fundamentals modules"
}
```

**Command:**

```bash
curl.exe -i -X PUT http://127.0.0.1:5000/api/courses/1 -H "Content-Type: application/json" -d "@tests/update_course.json"
```

**Response:** `200 OK`, the full updated course.

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

**Possible errors:** `400` for invalid values, `404` if the course doesn't exist.

> **A note on REST conventions:** Strictly speaking, `PUT` means "replace the whole resource" and `PATCH` means "change some fields." This API uses `PUT` for partial updates, which many real APIs also do. Supporting true `PATCH` is a good next step.

### Delete a course

`DELETE /api/courses/<id>`

```bash
curl.exe -i -X DELETE http://127.0.0.1:5000/api/courses/1
```

**Response:** `200 OK`

```json
{
  "message": "Course 1 deleted"
}
```

**Possible errors:** `404` if the course doesn't exist.

### Status codes used

| Code | Meaning | When you'll see it |
|---|---|---|
| `200 OK` | Success | Get, update, or delete worked |
| `201 Created` | New resource created | A course was added |
| `400 Bad Request` | The request had a problem | Missing or invalid fields, or the body isn't JSON |
| `404 Not Found` | Nothing at that address | Unknown course ID or unknown URL |
| `405 Method Not Allowed` | The URL exists, but not for that method | For example, `PATCH` on a course |
| `500 Internal Server Error` | The server couldn't do its job | `courses.json` can't be read or written, or is corrupted |

Every error comes back as JSON in the same shape:

```json
{
  "error": "A message explaining what went wrong"
}
```

---

## Testing

The full test suite is in **[TESTING.md](TESTING.md)**: 20 copy-and-paste tests with the expected response for each, covering every endpoint and every error case.

### Quick start

1. Start the server in one terminal with `python app.py`.
2. For a clean run, stop the server, delete `courses.json`, and start it again. That way the IDs match the expected responses.
3. Open a second terminal in the `codecrafthub` folder.
4. Work through Tests 1 to 20 in order and tick them off in the checklist at the end of TESTING.md.

### Why the test data lives in files

Typing JSON directly into a curl command breaks easily on Windows, because PowerShell and Command Prompt handle quotes differently. The tests keep each JSON body in a file in the `tests` folder and send it with `-d "@tests/file.json"`, which works the same in every terminal. Keep the quotes around `@tests/...`, because an unquoted `@` means something else in PowerShell.

### Other ways to test

- **Browser:** works for GET requests only. Try `http://127.0.0.1:5000/api/courses`.
- **REST Client extension for VS Code** (by Huachao Mao): write requests in a `.http` file and click **Send Request** above each one.
- **Postman:** a desktop app with a visual interface for building requests.

---

## Troubleshooting

### Setup problems

| Problem | Fix |
|---|---|
| `python` is not recognized | Python isn't installed or isn't on your PATH. Reinstall it and check **"Add Python to PATH."** On Mac/Linux, use `python3`. |
| `ModuleNotFoundError: No module named 'flask'` | The virtual environment isn't active (no `(venv)` in your prompt). Activate it, then run `pip install -r requirements.txt` if needed. |
| PowerShell says running scripts is disabled | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then activate again. |

### Server problems

| Problem | Fix |
|---|---|
| `python app.py` exits without starting a server | Make sure `app.py` is saved (no white dot on the VS Code tab), and that `if __name__ == "__main__":` at the bottom isn't indented. |
| `Address already in use` / port 5000 is busy | Another server is already running. Check every terminal tab in VS Code and stop it with `Ctrl+C`. |
| A new endpoint gives `404` or `405` | Every `@app.route` must be above the `if __name__ == "__main__":` block. Code after `app.run()` never runs. Save and restart the server. |
| `NameError: name 'request' is not defined` | The imports at the top are incomplete. The Flask line should be `from flask import Flask, jsonify, request`. |

### Request problems

| Problem | Fix |
|---|---|
| Opening `http://127.0.0.1:5000/` gives 404 | Use the full endpoint path, like `http://127.0.0.1:5000/api/courses`. |
| `Failed to connect to 127.0.0.1 port 5000` | The server isn't running. Start it in another terminal. |
| PowerShell asks for `Uri:` or shows a red parameter error | You typed `curl` instead of `curl.exe`. |
| `Couldn't read data from file` | Run curl from the `codecrafthub` folder, and make sure the `tests` folder is there. |
| `400: Request body must be valid JSON` | The JSON is malformed, or the `Content-Type: application/json` header is missing. Check for missing commas or quotes. |
| `500: Storage error: courses.json contains invalid JSON` | The data file was edited by hand and broken. Fix the JSON, or delete the file to start fresh. **Deleting it removes all courses.** |

### Reading error messages

When Python shows a long error (a traceback), look at the **last few lines** first. The line starting with `File "...app.py"` points to your code, and the very last line names the error.

---

## Project structure

```
codecrafthub/
├── app.py              # The entire application: setup, helpers, routes, error handlers
├── courses.json        # Your course data (created automatically; don't edit while the server runs)
├── requirements.txt    # Python packages the project needs (Flask and its dependencies)
├── README.md           # This file
├── TESTING.md          # Step-by-step test cases with expected responses
├── tests/              # JSON request bodies used by the tests
│   ├── new_course.json
│   ├── new_course_2.json
│   ├── update_course.json
│   ├── update_bad_status.json
│   ├── missing_fields.json
│   ├── bad_status.json
│   ├── bad_date.json
│   └── empty_name.json
└── venv/               # Virtual environment (created during installation; don't edit)
```

### Inside `app.py`

The file is organized top to bottom in the order a request flows through it:

| Section | What it contains |
|---|---|
| **Imports and setup** | Loads Flask and creates the `app` object |
| **Configuration** | The data file name, allowed statuses, and required fields |
| **`StorageError`** | A custom error raised when the data file can't be read or written |
| **JSON file helpers** | `init_data_file()`, `load_courses()`, `save_courses()`, `get_next_id()`, `find_course()` |
| **Validation** | `validate_course()` checks incoming data, and `get_json_body()` safely reads the request body |
| **Routes** | One function per endpoint, each marked with `@app.route(...)` |
| **Error handlers** | Turn storage errors, unknown URLs, and wrong methods into JSON responses |
| **Start the server** | The `if __name__ == "__main__":` block that runs `app.run()` |

### How a request flows

Here's what happens when you add a course:

1. curl sends `POST /api/courses` with a JSON body.
2. Flask matches the URL and method to `add_course()`.
3. `get_json_body()` reads the JSON, and `validate_course()` checks every field. Any problem returns a `400` immediately.
4. `load_courses()` reads the current list from `courses.json`.
5. The new course gets the next ID and a timestamp, and is added to the list.
6. `save_courses()` writes the whole list back to the file.
7. `jsonify()` sends the new course back with status `201`.

Every endpoint follows the same pattern: **read the request → validate → load → change → save → respond**.

### Why IDs aren't reused

`get_next_id()` uses the highest existing ID plus one, not the number of courses plus one. If you had courses 1, 2, and 3 and deleted course 2, counting would give 3 again, a duplicate. Using the highest ID avoids that.

---

## Limitations and next steps

This project is intentionally simple. A few things it doesn't handle, which are worth knowing:

- **One user at a time.** Every request reads and rewrites the whole JSON file. If two requests save at the same moment, one change can be lost. Real apps use a database like SQLite or PostgreSQL to handle this.
- **No authentication.** Anyone who can reach the server can change the data. That's fine on your own computer, but not on the internet.
- **Development server only.** Flask's built-in server isn't meant for production. Real deployments use a production server like Gunicorn or Waitress.

Ideas for extending it:

- Filter by status with a query parameter: `GET /api/courses?status=In Progress`
- Add a stats endpoint that counts courses per status
- Add a true `PATCH` endpoint and make `PUT` replace the whole course
- Write automated tests with `pytest` and Flask's test client
- Swap the JSON file for SQLite

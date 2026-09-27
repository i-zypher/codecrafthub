"""
CodeCraftHub - a simple REST API for tracking courses you want to learn.

Built with Flask. Course data is stored in a plain JSON file (courses.json),
so no database is needed.

Run it with:   python app.py
Then visit:    http://127.0.0.1:5000/api/courses
"""

import json
import os
from datetime import datetime

from flask import Flask, jsonify, request

# Create the Flask application
app = Flask(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DATA_FILE = "courses.json"  # Where all course data is stored
VALID_STATUSES = ["Not Started", "In Progress", "Completed"]
REQUIRED_FIELDS = ["name", "description", "target_date", "status"]


# ---------------------------------------------------------------------------
# Custom error for file problems
# ---------------------------------------------------------------------------

class StorageError(Exception):
    """Raised when courses.json can't be read or written.

    Instead of handling file errors inside every route, the helpers raise
    this error, and one error handler (further down) turns it into a clean
    500 JSON response.
    """


# ---------------------------------------------------------------------------
# JSON file helpers
# ---------------------------------------------------------------------------

def init_data_file():
    """Create courses.json with an empty list if it doesn't exist yet."""
    if not os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "w") as f:
                json.dump([], f)
        except OSError as e:
            raise StorageError(f"Could not create {DATA_FILE}: {e}")


def load_courses():
    """Read all courses from the JSON file and return them as a list."""
    init_data_file()  # Recreate the file if someone deleted it while running

    try:
        with open(DATA_FILE, "r") as f:
            content = f.read().strip()
    except OSError as e:
        raise StorageError(f"Could not read {DATA_FILE}: {e}")

    # An empty file just means "no courses yet"
    if not content:
        return []

    # If the file has broken JSON, stop with an error instead of silently
    # returning []. Returning [] here would cause the next save to overwrite
    # the file and wipe out every course in it.
    try:
        courses = json.loads(content)
    except json.JSONDecodeError:
        raise StorageError(f"{DATA_FILE} contains invalid JSON. Fix or delete the file.")

    if not isinstance(courses, list):
        raise StorageError(f"{DATA_FILE} should contain a list of courses.")

    return courses


def save_courses(courses):
    """Write the full list of courses back to the JSON file.

    We write to a temporary file first, then swap it into place. If the
    program crashes mid-write, the original courses.json stays intact.
    """
    temp_file = DATA_FILE + ".tmp"
    try:
        with open(temp_file, "w") as f:
            json.dump(courses, f, indent=2)
        os.replace(temp_file, DATA_FILE)  # Swap the new file in
    except OSError as e:
        raise StorageError(f"Could not save {DATA_FILE}: {e}")


def get_next_id(courses):
    """Return the next available ID (one higher than the current highest).

    We don't use len(courses) + 1, because after a delete that could
    produce an ID that already exists.
    """
    if not courses:
        return 1
    return max(course["id"] for course in courses) + 1


def find_course(courses, course_id):
    """Return the course with this ID, or None if it doesn't exist."""
    for course in courses:
        if course["id"] == course_id:
            return course
    return None


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_course(data, partial=False):
    """Check course data. Returns an error message, or None if it's valid.

    partial=False (used by POST): every required field must be present.
    partial=True  (used by PUT):  only the fields that were sent are checked,
                                  so you can update just one field at a time.
    """
    # 1. Check that required fields are present (POST only)
    if not partial:
        missing = [field for field in REQUIRED_FIELDS if field not in data]
        if missing:
            return f"Missing required field(s): {', '.join(missing)}"

    # 2. name and description must be non-empty text
    for field in ["name", "description"]:
        if field in data:
            value = data[field]
            if not isinstance(value, str) or not value.strip():
                return f"'{field}' must be a non-empty string"

    # 3. target_date must be a real date in YYYY-MM-DD format
    if "target_date" in data:
        try:
            datetime.strptime(data["target_date"], "%Y-%m-%d")
        except (ValueError, TypeError):
            return "'target_date' must be a valid date in YYYY-MM-DD format"

    # 4. status must be one of the allowed values (exact match)
    if "status" in data and data["status"] not in VALID_STATUSES:
        return f"'status' must be one of: {', '.join(VALID_STATUSES)}"

    return None  # No problems found


def get_json_body():
    """Return the request's JSON body as a dict, or None if it isn't valid JSON."""
    data = request.get_json(silent=True)  # silent=True: return None instead of crashing
    if not isinstance(data, dict):
        return None
    return data


# ---------------------------------------------------------------------------
# Routes (the API endpoints)
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    """Simple check that the server is running."""
    return jsonify({"message": "CodeCraftHub API is running"}), 200


@app.route("/api/courses", methods=["POST"])
def add_course():
    """Add a new course."""
    data = get_json_body()
    if data is None:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    error = validate_course(data)
    if error:
        return jsonify({"error": error}), 400

    courses = load_courses()

    # Build the new course. id and created_at are generated here,
    # never taken from the client.
    new_course = {
        "id": get_next_id(courses),
        "name": data["name"].strip(),
        "description": data["description"].strip(),
        "target_date": data["target_date"],
        "status": data["status"],
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    courses.append(new_course)
    save_courses(courses)

    return jsonify(new_course), 201  # 201 = Created


@app.route("/api/courses", methods=["GET"])
def get_courses():
    """Return every course."""
    courses = load_courses()
    return jsonify(courses), 200


@app.route("/api/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    """Return one course by its ID."""
    courses = load_courses()
    course = find_course(courses, course_id)
    if course is None:
        return jsonify({"error": f"Course {course_id} not found"}), 404
    return jsonify(course), 200


@app.route("/api/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    """Update one or more fields of an existing course."""
    data = get_json_body()
    if data is None:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    courses = load_courses()
    course = find_course(courses, course_id)
    if course is None:
        return jsonify({"error": f"Course {course_id} not found"}), 404

    error = validate_course(data, partial=True)
    if error:
        return jsonify({"error": error}), 400

    # Only these fields can be changed. id and created_at are protected.
    for field in ["name", "description", "target_date", "status"]:
        if field in data:
            value = data[field]
            course[field] = value.strip() if isinstance(value, str) else value

    # course is the actual object inside the courses list,
    # so saving the list saves the change.
    save_courses(courses)
    return jsonify(course), 200

@app.route("/api/courses/stats", methods=["GET"])
def get_stats():
    """Return the total number of courses and a count for each status."""
    courses = load_courses()

    # Start every status at 0, so statuses with no courses still appear
    by_status = {status: 0 for status in VALID_STATUSES}
    for course in courses:
        by_status[course["status"]] += 1

    return jsonify({
        "total_courses": len(courses),
        "by_status": by_status,
    }), 200


@app.route("/api/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    """Delete a course by its ID."""
    courses = load_courses()
    course = find_course(courses, course_id)
    if course is None:
        return jsonify({"error": f"Course {course_id} not found"}), 404

    courses.remove(course)
    save_courses(courses)
    return jsonify({"message": f"Course {course_id} deleted"}), 200


# ---------------------------------------------------------------------------
# Error handlers: make every error come back as JSON, not an HTML page
# ---------------------------------------------------------------------------

@app.errorhandler(StorageError)
def handle_storage_error(e):
    return jsonify({"error": f"Storage error: {e}"}), 500


@app.errorhandler(404)
def handle_not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(405)
def handle_method_not_allowed(e):
    return jsonify({"error": "Method not allowed on this endpoint"}), 405


# ---------------------------------------------------------------------------
# Start the server
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    init_data_file()  # Make sure courses.json exists before accepting requests
    print(f"Data file: {os.path.abspath(DATA_FILE)}")
    app.run(debug=True)  # debug=True: auto-reload on save, detailed errors
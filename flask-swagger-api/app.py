
from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)

# Swagger configuration
app.config["SWAGGER"] = {
    "title": "Student Management API",
    "uiversion": 3
}

swagger = Swagger(app)

# Temporary in-memory storage
students = {}
next_id = 1


@app.route("/", methods=["GET"])
def home():
    """Welcome endpoint
    ---
    responses:
      200:
        description: API is running successfully
    """
    return jsonify({
        "message": "Welcome to Student Management API",
        "swagger_url": "/apidocs/"
    })


@app.route("/students", methods=["POST"])
def create_student():
    """Create a student
    ---
    tags:
      - Students
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - age
          properties:
            name:
              type: string
              example: Rahul
            age:
              type: integer
              example: 21
            course:
              type: string
              example: Python
    responses:
      201:
        description: Student created successfully
      400:
        description: Invalid request data
    """
    global next_id

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400

    if not data.get("name") or "age" not in data:
        return jsonify({"error": "Name and age are required"}), 400

    try:
        age = int(data["age"])
        if isinstance(data["age"], bool) or age <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "Age must be a positive integer"}), 400

    student = {
        "id": next_id,
        "name": data["name"],
        "age": age,
        "course": data.get("course", "")
    }

    students[next_id] = student
    next_id += 1

    return jsonify(student), 201


@app.route("/students", methods=["GET"])
def get_students():
    """Get all students
    ---
    tags:
      - Students
    responses:
      200:
        description: List of all students
    """
    return jsonify(list(students.values()))


@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    """Get a student by ID
    ---
    tags:
      - Students
    parameters:
      - name: student_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Student found
      404:
        description: Student not found
    """
    student = students.get(student_id)

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(student)


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """Update a student
    ---
    tags:
      - Students
    parameters:
      - name: student_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: Priya
            age:
              type: integer
              example: 22
            course:
              type: string
              example: Data Science
    responses:
      200:
        description: Student updated successfully
      404:
        description: Student not found
    """
    student = students.get(student_id)

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400

    if "name" in data:
        if not isinstance(data["name"], str) or not data["name"].strip():
            return jsonify({"error": "Name must be a non-empty string"}), 400
        student["name"] = data["name"].strip()

    if "age" in data:
        try:
            age = int(data["age"])
            if isinstance(data["age"], bool) or age <= 0:
                raise ValueError
            student["age"] = age
        except (ValueError, TypeError):
            return jsonify({"error": "Age must be a positive integer"}), 400

    if "course" in data:
        if not isinstance(data["course"], str):
            return jsonify({"error": "Course must be a string"}), 400
        student["course"] = data["course"]

    return jsonify(student)


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """Delete a student
    ---
    tags:
      - Students
    parameters:
      - name: student_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Student deleted successfully
      404:
        description: Student not found
    """
    if student_id not in students:
        return jsonify({"error": "Student not found"}), 404

    deleted = students.pop(student_id)

    return jsonify({
        "message": "Student deleted successfully",
        "student": deleted
    })


if __name__ == "__main__":
    app.run(debug=True)

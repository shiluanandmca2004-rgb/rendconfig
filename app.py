import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

PASS_MARKS = int(os.getenv("PASS_MARKS", 40))

# Home route
@app.route("/")
def home():
    return "🎓 Welcome to Grade Calculator API (Render Deployment)"

# HTML Form page
@app.route("/form", methods=["GET", "POST"])
def form():
    grade = None
    marks = None
    result = None

    if request.method == "POST":
        try:
            marks = int(request.form["marks"])
        except:
            result = "❌ Invalid input, enter a number."
            return render_template_string(FORM_HTML, result=result)

        if marks >= 90:
            grade = "A+"
        elif marks >= 75:
            grade = "A"
        elif marks >= 60:
            grade = "B"
        elif marks >= PASS_MARKS:
            grade = "C"
        else:
            grade = "Fail"

        result = f"Marks: {marks} → Grade: {grade}"

    return render_template_string(FORM_HTML, result=result)

# API endpoint (JSON POST)
@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    if not data or "marks" not in data:
        return jsonify({"error": "Please provide 'marks' in JSON"}), 400

    marks = data["marks"]

    if marks >= 90:
        grade = "A+"
    elif marks >= 75:
        grade = "A"
    elif marks >= 60:
        grade = "B"
    elif marks >= PASS_MARKS:
        grade = "C"
    else:
        grade = "Fail"

    return jsonify({"marks": marks, "grade": grade})

# Full HTML Template with Navbar & Footer
FORM_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Grade Calculator</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light d-flex flex-column min-vh-100">

    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container">
        <a class="navbar-brand fw-bold" href="/form">🎓 Grade Calculator</a>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container flex-grow-1 d-flex justify-content-center align-items-center">
        <div class="card shadow-lg p-4 rounded-4 mt-5 mb-5" style="width: 400px;">
            <h2 class="text-center mb-4">Calculate Your Grade</h2>
            <form method="POST">
                <div class="mb-3">
                    <label for="marks" class="form-label">Enter Marks</label>
                    <input type="number" class="form-control" name="marks" required placeholder="e.g. 85">
                </div>
                <button type="submit" class="btn btn-primary w-100">Calculate</button>
            </form>
            {% if result %}
                <div class="alert alert-info text-center mt-4">
                    <strong>{{ result }}</strong>
                </div>
            {% endif %}
        </div>
    </div>

    <!-- Footer -->
    <footer class="bg-dark text-white text-center py-3 mt-auto">
        <p class="mb-0">© 2025 Grade Calculator | Powered by Flask & Bootstrap | Deployed on Render</p>
    </footer>

</body>
</html>
"""

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

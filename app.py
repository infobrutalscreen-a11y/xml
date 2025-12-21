from flask import Flask, request, send_file
import os
from convert import convert

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FILE = "output.yml"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("file")

        if not file:
            return "Файл не загружен", 400

        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)

        convert(input_path, OUTPUT_FILE)

        return send_file(OUTPUT_FILE, as_attachment=True)

    return """
    <h2>XML → YML конвертер</h2>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".xml" required>
        <br><br>
        <button type="submit">Конвертировать</button>
    </form>
    """

if __name__ == "__main__":
    app.run(debug=True)
    
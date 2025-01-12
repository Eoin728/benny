import os
import time

from flask import Flask, Response, render_template, request, send_file
from werkzeug.utils import secure_filename

from process import transcribe

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Process the file here (example: just adding '_processed' to filename)
        processed_filename = filename.rsplit(".", 1)[0] + "_transcribed.txt"
        processed_filepath = os.path.join(
            app.config["UPLOAD_FOLDER"], processed_filename
        )

        # Simple file processing (just copying in this example)
        time.sleep(2)
        with open(filepath, "rb") as f:
            content = transcribe(f)
            # content = f.read()
        # print(content)
        with open(processed_filepath, "w") as f:
            # temproary
            # with open(processed_filepath, "wb") as f:
            f.write(content)

        return {"processed_file": processed_filename}


# @app.route("/download/<filename>")
# def download_file(filename):
#     return send_file(
#         os.path.join(app.config["UPLOAD_FOLDER"], filename), as_attachment=True
#     )


# if __name__ == "__main__":
#     app.run(debug=True)
@app.route("/download/<filename>")
def download_file(filename):
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    def generate():
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(8192)  # 8KB chunks
                if not chunk:
                    break
                yield chunk

    return Response(
        generate(),
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Length": os.path.getsize(filepath),
        },
    )


if __name__ == "__main__":
    app.run(debug=True)

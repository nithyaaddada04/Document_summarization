import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from utils.extract import extract_text_from_path
from utils.summarize import extractive_summary
from utils.keywords import extract_keywords
from utils.ocr import extract_text_from_image_if_possible

ALLOWED_EXT = {".pdf", ".docx", ".txt", ".png", ".jpg", ".jpeg"}

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "change-this-secret"

def allowed_file(filename: str) -> bool:
    return "." in filename and os.path.splitext(filename.lower())[1] in ALLOWED_EXT

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("document")
        sentences = int(request.form.get("sentences", 5))

        if not file or file.filename.strip() == "":
            flash("Please choose a file.")
            return redirect(url_for("index"))

        if not allowed_file(file.filename):
            flash("Unsupported file type. Use PDF, DOCX, TXT, PNG, JPG.")
            return redirect(url_for("index"))

        fname = secure_filename(file.filename)
        fpath = os.path.join(app.config["UPLOAD_FOLDER"], fname)
        file.save(fpath)

        ext = os.path.splitext(fname.lower())[1]

        # Extract text (OCR for images, parser for pdf/docx/txt)
        if ext in {".png", ".jpg", ".jpeg"}:
            text, ocr_note = extract_text_from_image_if_possible(fpath)
        else:
            text = extract_text_from_path(fpath)
            ocr_note = None

        if not text.strip():
            flash("We couldn't extract any text from that file.")
            return redirect(url_for("index"))

        # Summarize + keywords
        summary = extractive_summary(text, sentences=sentences)
        keywords = extract_keywords(text, top_k=10)

        return render_template(
            "result.html",
            filename=fname,
            original_text=text,
            summary_text=summary,
            keywords=keywords,
            ocr_note=ocr_note
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

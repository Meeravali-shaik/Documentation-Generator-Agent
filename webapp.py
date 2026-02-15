import os
import time
from html import escape
from flask import Flask, render_template, request, Response, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from repo_parser import read_repo
from llm_agent import generate_doc
from github_loader import clone_repo

app = Flask(__name__)

LAST_PDF_PATH = None




def generate_pdf(text, output_path):
    doc = SimpleDocTemplate(output_path)
    styles = getSampleStyleSheet()
    elements = []

    safe_text = escape(text).replace("\n", "<br/>")

    elements.append(Paragraph("<b>Project Documentation</b>", styles['Title']))
    elements.append(Spacer(1, 24))
    elements.append(Paragraph(safe_text, styles['Normal']))

    doc.build(elements)




def process_project(input_value):
    global LAST_PDF_PATH

    yield "Starting documentation process...\n"

    
    if input_value.startswith("http"):
        yield "Cloning / Updating GitHub repository...\n"
        folder_path = clone_repo(input_value)
    else:
        folder_path = input_value

    yield "Reading project files...\n"
    files = read_repo(folder_path)

    combined_code = ""

    for path, code in files.items():
        name = os.path.basename(path)
        yield f"Adding file to context: {name}\n"
        combined_code += f"\n\n### FILE: {name}\n{code[:6000]}\n"

    yield "Sending whole project to Gemini (single request)...\n"

    doc_text, _ = generate_doc(combined_code)

    yield "Generating PDF...\n"

    os.makedirs("output", exist_ok=True)
    pdf_path = os.path.join("output", "Project_Documentation.pdf")
    generate_pdf(doc_text, pdf_path)

    LAST_PDF_PATH = pdf_path

    yield "Done! Click Download PDF button.\n"




@app.route("/")
def index():
    return render_template("index.html")


@app.route("/progress")
def progress():
    input_value = request.args.get("input_value")

    def generate():
        for msg in process_project(input_value):
            yield f"data: {msg}\n\n"
            time.sleep(0.4)

    return Response(generate(), mimetype="text/event-stream")


@app.route("/download")
def download():
    return send_file(LAST_PDF_PATH, as_attachment=True)



if __name__ == "__main__":
    app.run(debug=True)

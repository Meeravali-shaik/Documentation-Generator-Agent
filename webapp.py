import os
import time
import re
from html import escape
from flask import Flask, render_template, request, Response, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from repo_parser import read_repo
from llm_agent import generate_doc
from github_loader import clone_repo


pt = 1

app = Flask(__name__)

LAST_PDF_PATH = None


def parse_markdown_to_pdf_elements(text, styles):
    """Convert markdown text to reportlab PDF elements"""
    elements = []
    lines = text.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        
        if not line.strip():
            elements.append(Spacer(1, 12))
            i += 1
            continue
        
        
        if line.startswith('# '):
            content = line[2:].strip()
            content = escape(content)
            
           
            if elements and len(elements) > 5:
                elements.append(PageBreak())
            
            elements.append(Paragraph(f"<b>{content}</b>", styles['Heading1']))
            elements.append(Spacer(1, 18))
            i += 1
            continue
        
       
        if line.startswith('### '):
            content = line[4:].strip()
            content = escape(content)
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f"<b>{content}</b>", styles['Heading3']))
            elements.append(Spacer(1, 10))
            i += 1
            continue
        
        
        if line.startswith('## '):
            content = line[3:].strip()
            content = escape(content)
            elements.append(Spacer(1, 8))
            elements.append(Paragraph(f"<b>{content}</b>", styles['Heading2']))
            elements.append(Spacer(1, 12))
            i += 1
            continue
        
        
        if line.strip().startswith('* ') or line.strip().startswith('- '):
            content = line.strip()[2:].strip()
            
            content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)  
            content = content.replace('`', '')  
            content = escape(content) 
            elements.append(Paragraph(f"• {content}", styles['Normal']))
            i += 1
            continue
        
       
        content = line.strip()
        
        
        content = escape(content)
        
        
        content = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', content)
        
      
        content = re.sub(r'`([^`]+)`', r'<u>\1</u>', content)
        
        if content:
            elements.append(Paragraph(content, styles['Normal']))
            elements.append(Spacer(1, 6))
        
        i += 1
    
    return elements


def generate_pdf(text, output_path):
    doc = SimpleDocTemplate(output_path, topMargin=50, bottomMargin=50, leftMargin=40, rightMargin=40)
    styles = getSampleStyleSheet()
    
 
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=(0, 51, 102),
        spaceAfter=30,
        alignment=1 
    )
    
    elements = []

 
    elements.append(Spacer(1, 60))
    elements.append(Paragraph("Project Documentation", title_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("<i>Comprehensive Technical Documentation</i>", styles['Normal']))
    elements.append(Spacer(1, 40))
    
    
    elements.append(PageBreak())
    
 
    pdf_elements = parse_markdown_to_pdf_elements(text, styles)
    elements.extend(pdf_elements)

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
    if LAST_PDF_PATH and os.path.exists(LAST_PDF_PATH):
        return send_file(LAST_PDF_PATH, as_attachment=True)
    return {"error": "PDF not found"}, 404



if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False") == "True"
    app.run(debug=debug, host="0.0.0.0", port=port)

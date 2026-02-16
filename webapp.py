import os
import time
import re
import traceback
from html import escape
from flask import Flask, render_template, request, Response, send_file, send_from_directory
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from repo_parser import read_repo
from llm_agent import generate_doc
from github_loader import clone_repo

# Check for required environment variables
if not os.getenv("GEMINI_API_KEY"):
    print("WARNING: GEMINI_API_KEY environment variable not set!")

app = Flask(__name__, static_folder='static', static_url_path='/static')

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

    try:
        # Check for required environment variable
        if not os.getenv("GEMINI_API_KEY"):
            yield "ERROR: GEMINI_API_KEY not configured. Please set in Vercel environment variables."
            return

        if not input_value or not input_value.strip():
            yield "ERROR: No input provided. Please enter a folder path or GitHub URL."
            return

        yield "Starting documentation process..."

        
        if input_value.startswith("http"):
            yield "Cloning / Updating GitHub repository..."
            try:
                folder_path = clone_repo(input_value)
            except Exception as e:
                yield f"ERROR: Failed to clone repository: {str(e)}"
                return
        else:
            folder_path = input_value

        yield "Reading project files..."
        try:
            files = read_repo(folder_path)
        except Exception as e:
            yield f"ERROR: Failed to read project files: {str(e)}"
            return

        if not files:
            yield "ERROR: No Python files found in the project."
            return

        combined_code = ""

        for path, code in files.items():
            name = os.path.basename(path)
            yield f"Adding file to context: {name}"
            combined_code += f"\n\n### FILE: {name}\n{code[:6000]}\n"

        yield "Sending whole project to Gemini (single request)..."

        try:
            doc_text, _ = generate_doc(combined_code)
        except Exception as e:
            yield f"ERROR: Failed to generate documentation: {str(e)}"
            return

        yield "Generating PDF..."

        try:
            os.makedirs("output", exist_ok=True)
            pdf_path = os.path.join("output", "Project_Documentation.pdf")
            generate_pdf(doc_text, pdf_path)
            LAST_PDF_PATH = pdf_path
        except Exception as e:
            yield f"ERROR: Failed to generate PDF: {str(e)}"
            return

        yield "Done! Click Download PDF button."

    except Exception as e:
        yield f"ERROR: Unexpected error: {str(e)}"
        traceback.print_exc()



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory('static', filename)


@app.route("/debug")
def debug():
    """Debug endpoint to check environment and connectivity"""
    debug_info = {
        "status": "OK",
        "gemini_api_key_set": bool(os.getenv("GEMINI_API_KEY")),
        "flask_debug": os.getenv("FLASK_DEBUG", "False"),
        "environment": os.getenv("FLASK_ENV", "production")
    }
    return debug_info


@app.route("/progress")
def progress():
    input_value = request.args.get("input_value")

    def generate():
        try:
            # Send initial message
            yield f"data: Initializing...\n\n"
            
            for msg in process_project(input_value):
                # Ensure proper SSE format
                msg_clean = str(msg).replace('\n', ' ').strip()
                if msg_clean:
                    yield f"data: {msg_clean}\n\n"
                time.sleep(0.2)
                
        except Exception as e:
            error_msg = f"ERROR: {str(e)}"
            yield f"data: {error_msg}\n\n"
            print(f"Progress endpoint error: {e}")
            traceback.print_exc()

    # Add headers to support streaming on serverless platforms
    response = Response(generate(), mimetype="text/event-stream")
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Connection'] = 'keep-alive'
    response.headers['X-Accel-Buffering'] = 'no'
    return response


@app.route("/download")
def download():
    if LAST_PDF_PATH and os.path.exists(LAST_PDF_PATH):
        return send_file(LAST_PDF_PATH, as_attachment=True)
    return {"error": "PDF not found"}, 404



if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False") == "True"
    app.run(debug=debug, host="0.0.0.0", port=port)

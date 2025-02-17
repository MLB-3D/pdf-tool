from flask import Flask, request, send_file
import fitz  # PyMuPDF
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def pdf_zuschneiden(input_pdf, output_pdf, x0, y0, x1, y1, drehen):
    doc = fitz.open(input_pdf)
    
    for page in doc:
        page.set_cropbox(fitz.Rect(x0, y0, x1, y1))
        if drehen:
            page.set_rotation(-90)
    
    doc.save(output_pdf)
    doc.close()

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return {"error": "Keine Datei hochgeladen"}, 400
    
    file = request.files['file']
    if file.filename == '':
        return {"error": "Leere Datei"}, 400
    
    input_pdf = os.path.join(UPLOAD_FOLDER, file.filename)
    output_pdf = os.path.join(PROCESSED_FOLDER, f"bearbeitet_{file.filename}")
    file.save(input_pdf)
    
    drehen = request.form.get('drehen', 'false').lower() == 'true'
    
    try:
        pdf_zuschneiden(input_pdf, output_pdf, 41, 89, 247, 195, drehen)
        return send_file(output_pdf, as_attachment=True)
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

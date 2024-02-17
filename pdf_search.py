import os
from PyPDF2 import PdfReader

UPLOAD_FOLDER = 'uploads'

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page_text = pdf_reader.pages[page_num].extract_text()
            if page_text:
                text += page_text
        return text.lower() if text else None

def search_skill_in_pdfs(skill_to_search):
    pdf_names_with_skill = []

    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(UPLOAD_FOLDER, filename)
            pdf_text = extract_text_from_pdf(pdf_path)

            if pdf_text is not None and skill_to_search.lower() in pdf_text:
                pdf_names_with_skill.append(filename)
    
    return pdf_names_with_skill


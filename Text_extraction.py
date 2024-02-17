# from pdfminer.high_level import extract_text
# from pyresparser import ResumeParser
# from pdfminer3.layout import LAParams, LTTextBox
# from pdfminer3.pdfpage import PDFPage
# from pdfminer3.pdfinterp import PDFResourceManager
# from pdfminer3.pdfinterp import PDFPageInterpreter
# from pdfminer3.converter import TextConverter
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity as cs
# import nltk
# import spacy
# # nltk.download('stopwords')
# spacy.load('en_core_web_sm')


# def extract_pdf_content(file_path):
#   """
#   Extracts the content from a PDF file using pdfminer.

#   Args:
#     file_path: The path to the PDF file.

#   Returns:
#     A string containing the extracted text.
#   """
#   try:
#     with open(file_path, 'rb') as pdf_file:
#       text = extract_text(pdf_file)
#       return text
#   except Exception as e:
#     print(f"Error extracting content from PDF: {e}")
#     return ""

# file_path = 'Python-Developer-Resume-1-1-1.pdf'
# job_description = 'job_description.txt'
# data = extract_pdf_content(file_path)
# if data:
#     print(data)
# else:
#     print("Failed to extract text from PDF.")

# resume_data = ResumeParser('./Python-Developer-Resume-1-1-1.pdf').get_extracted_data()
# print("Hello " + resume_data['name'])
# print('Name: ' + resume_data['name'])
# print('Email: ' + resume_data['email'])
# print('Contact: ' + resume_data['mobile_number'])
# print('Resume pages: ' + str(resume_data['no_of_pages']))

# content = [job_description, data]
# cv = CountVectorizer()
# matrix = cv.fit_transform(content)
# sm = cs(matrix)
# print(str(sm[1][0]*100))

from pdfminer.high_level import extract_text
from pyresparser import ResumeParser
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_pdf_content(file_path):
    try:
        with open(file_path, 'rb') as pdf_file:
            text = extract_text(pdf_file)
            return text
    except Exception as e:
        print(f"Error extracting content from PDF: {e}")
        return ""

if __name__ == "__main__":
    file_path = 'Avesh_Momin_resume.pdf'
    job_description_path = 'job_description.txt'

    # Extract content from resume PDF
    resume_content = extract_pdf_content(file_path)
    if resume_content:
        print("Resume Content:")
        print(resume_content)
    else:
        print("Failed to extract text from resume PDF.")

    # Parse resume using pyresparser
    # resume_data = ResumeParser(file_path).get_extracted_data()
    # if resume_data:
    #     print("\nExtracted Resume Data:")
    #     print('Name:', resume_data.get('name'))
    #     print('Email:', resume_data.get('email'))
    #     print('Contact:', resume_data.get('mobile_number'))
    #     print('No. of Pages:', resume_data.get('no_of_pages'))
    # else:
    #     print("Failed to parse resume.")

    # Load job description
    with open(job_description_path, 'r') as job_desc_file:
        job_description_content = job_desc_file.read()

    # Compute similarity between resume and job description
    content = [job_description_content, resume_content]
    cv = CountVectorizer()
    matrix = cv.fit_transform(content)
    similarity_matrix = cosine_similarity(matrix)

    print("\nSimilarity between resume and job description:", similarity_matrix[1][0]*100)

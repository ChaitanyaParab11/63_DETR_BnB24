import spacy
from spacy import displacy
import matplotlib.pyplot as plt
import PyPDF2

# Load English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def visualize_resume_from_pdf(pdf_path):
    # Extract text from PDF
    resume_text = extract_text_from_pdf(pdf_path)

    # Process the resume text
    doc = nlp(resume_text)
    print(doc.ents)

    # Extract entities and labels
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Visualize named entities
    displacy.render(doc, style="ent", jupyter=False)

    # Display a bar chart of entity types
    entity_types = [ent[1] for ent in entities]
    entity_counts = {ent_type: entity_types.count(ent_type) for ent_type in set(entity_types)}

    plt.bar(entity_counts.keys(), entity_counts.values())
    plt.xlabel("Entity Type")
    plt.ylabel("Count")
    plt.title("Analysis Of Resume")
    # plt.show()
    plt.savefig('static/images/visualization.png')


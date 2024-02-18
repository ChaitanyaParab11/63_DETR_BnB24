from flask import Flask, render_template, request, redirect, url_for, jsonify, render_template_string, send_file
import os
import pickle
import pandas as pd
from werkzeug.utils import secure_filename
from pdf_search import search_skill_in_pdfs  # Import the search function from pdf_search
from my_analysis import visualize_resume_from_pdf 

app = Flask(__name__)


# Mock data (replace with actual data handling)
candidates = [
    {'name': 'John Doe', 'qualifications': 'Bachelor\'s in Computer Science', 'experience': '5 years', 'skills': 'Python, Java', 'cultural_fit': 8.5},
    {'name': 'Jane Smith', 'qualifications': 'Master\'s in Business Administration', 'experience': '7 years', 'skills': 'Leadership, Communication', 'cultural_fit': 9.2},
    # Add more candidate data
]


# Set the path where you want to store the uploaded PDFs
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'}

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/handle_bulk_pdf_upload', methods=['POST'])
def handle_bulk_pdf_upload():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'pdfFiles' not in request.files:
            return redirect(request.url)

        pdf_files = request.files.getlist('pdfFiles')

        for pdf_file in pdf_files:
            # Check if the file is a PDF
            if pdf_file and allowed_file(pdf_file.filename):
                # Securely save the file with a unique name
                filename = secure_filename(pdf_file.filename)
                pdf_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                # Perform additional processing if needed

        # Return a response indicating successful upload
        return 'Bulk PDF upload successful'

@app.route('/search_skill', methods=['POST'])
def search_skill():
    data = request.get_json()
    skill_to_search = data.get('searchSkill', '')
    
    # Replace this with your logic to search for the skill in PDFs
    # and get the list of PDF names containing the skill
    pdf_names = search_skill_in_pdfs(skill_to_search)

    response = {
        "html": render_template_string("""
            {% if pdf_names %}
                <ul style="list-style-type: none; padding: 0;">
                    {% for pdf_name in pdf_names %}
                        <li style="font-size: 20px; color: white; display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid #ddd; padding-bottom: 5px;">
                            <span style="flex: 1;">
                                <a href="{{ url_for('open_pdf', filename=pdf_name) }}" target="_blank" style="color: white;">{{ pdf_name }}</a>
                            </span>
                            <button class="welcome-hero-btn" onclick="analysePDF('{{ pdf_name }}')">
                                Analyse <i data-feather="search"></i>
                            </button>
                        </li>
                    {% endfor %}
                </ul>
            {% elif no_result %}
                <p style="font-size: 20px; color: white;">No results found for the skill "{{ skill }}".</p>
            {% endif %}
        """, pdf_names=pdf_names, skill=skill_to_search)
    }

    return jsonify(response)

@app.route('/analyse_pdf/<pdf_name>')
def analyse_pdf(pdf_name):
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_name)

    # Check if the file exists
    if not os.path.exists(pdf_path):
        return "File not found", 404

    # Save visualization as image
    image_path = visualize_resume_from_pdf(pdf_path, "static/images/visualization.png")

    # Render the HTML with the image path
    return render_template('profile_screening.html', image_path=image_path)

@app.route('/open_pdf/<filename>')
def open_pdf(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(filepath, mimetype='application/pdf', as_attachment=False)


@app.route('/profile_screening', methods=['GET'])
def profile_screening():
    pdf_name = request.args.get('pdf')  # Get the PDF name from the URL parameter
    # You may want to include additional logic here to process the PDF name if needed

    # Render the profile_screening.html template and pass the PDF name
    return render_template('profile_screening.html', pdf_name=pdf_name)

@app.route('/qualifications-experience-analysis')
def qualifications_experience_analysis():
    return render_template('qualifications_experience_analysis.html', candidates=candidates)

@app.route('/skills-assessment')
def skills_assessment():
    return render_template('skills_assessment.html', candidates=candidates)

@app.route('/cultural-fit-evaluation')
def cultural_fit_evaluation():
    return render_template('cultural_fit_evaluation.html', candidates=candidates)

@app.route('/detailed-dashboard')
def detailed_dashboard():
    return render_template('detailed_dashboard.html', candidates=candidates)


def recommend(category, data, similarity):
    index = data[data['Category'] == category].index[0]
    distances = similarity[index]
    resume_list = sorted(list(enumerate(distances)), key=lambda x: x[1])[1:7]

    recommended_resume = [data.iloc[i[0]].resume_id for i in resume_list]
    return recommended_resume

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_category = request.form['selected_category']
        name = recommend(selected_category, data, similarity)

        return render_template('index.html', selected_category=selected_category, name=name, categories=data['Category'].unique())

    return render_template('index.html', selected_category='', name=None, categories=data['Category'].unique())


if __name__ == '__main__':
        app.config['UPLOAD_FOLDER'] = 'uploads'
        data_dict = pickle.load(open('data_dict.pkl', 'rb'))
        data = pd.DataFrame(data_dict)
        similarity = pickle.load(open('similarity.pkl', 'rb'))
        
        app.run(debug=True)


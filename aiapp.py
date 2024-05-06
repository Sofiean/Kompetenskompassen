# Import necessary libraries
from flask import Flask, render_template, request
import pandas as pd
import os
from OpenAI_Functions import generate_text, config_api

# Create a Flask application instance
app = Flask(__name__)

# Load environment variables from .env
config_api()

# Define the current working directory
current_dir = os.getcwd()

# Define the path to the folder containing the CSV files
data_folder = os.path.join(current_dir, 'CSVfiler')

# Load CSV files for each year and store them in a dictionary
data_by_year = {}
for year in range(2018, 2023):
    file_path = os.path.join(data_folder, f'skills_by_occupation_update{year}.csv')
    try:
        data = pd.read_csv(file_path)
        data_by_year[year] = data
    except FileNotFoundError:
        print(f"Data for year {year} not found.")

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for the analysis page
@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    if request.method == 'POST':
        # Process form data
        selected_occupation = request.form['occupation']
        selected_municipality = request.form['municipality']
        selected_years = request.form.getlist('years')

        # Filter data based on form input
        filtered_data = pd.concat([data_by_year[int(year)] for year in selected_years], ignore_index=True)

        # Perform analysis
        top_skills = filtered_data.groupby('Skill')['Count'].sum().nlargest(10)

        if top_skills.empty:
            top_skills = []

        # Render analysis template with results
        return render_template('analysis.html', 
                               selected_occupation=selected_occupation,
                               selected_municipality=selected_municipality,
                               selected_years=selected_years,
                               top_skills=top_skills)

    # Render initial analysis page
    top_skills = data_by_year[2018].groupby('Skill')['Count'].sum().nlargest(10)

    return render_template('analysis.html', top_skills=top_skills,
                           occupation_options=data_by_year[2018]['Occupation Field'].unique().tolist(),
                           municipality_options=data_by_year[2018]['Municipality'].unique().tolist(),
                           years_options=list(data_by_year.keys()))
"""
# Route for the AI page
@app.route('/AI', methods=['GET', 'POST'])
def ai_page():
    if request.method == 'POST':
        # Generate AI text based on form input
        selected_competence = request.form['selected_competence']
        generated_text = generate_text(selected_competence)
        
        # Render AI template with generated text
        return render_template('AI.html', generated_text=generated_text)

    # Render AI page with form to select a competence
    all_competencies = set()
    for data in data_by_year.values():
        all_competencies.update(data['Skill'].unique())

    return render_template('AI.html', all_competencies=all_competencies)
"""
#Börja om från början med chatgpt och mata den med all kod på nytt
@app.route('/AI')
def ai():
    all_competencies = set()
    for data in data_by_year.values():
        all_competencies.update(data['Skill'].unique())
    return render_template('AI.html', all_competencies=all_competencies)

@app.route('/generate_text', methods=['POST'])
def generate_text():
    selected_competence = request.form['selected_competence']
    generated_text = generate_text(selected_competence)
    return render_template('AI.html', generated_text=generated_text)

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)

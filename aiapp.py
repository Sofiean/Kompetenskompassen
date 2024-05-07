# Import necessary libraries
from flask import Flask, render_template, request
import pandas as pd
import os
from openai_functions import config_api, generate_text

app = Flask(__name__)

config_api()

# Get the current working directory
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

# Get all unique competencies from the data
all_competencies = set()
for data in data_by_year.values():
    all_competencies.update(data['Skill'].unique())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    if request.method == 'POST':
        selected_occupation = request.form['occupation']
        selected_municipality = request.form['municipality']
        selected_years = request.form.getlist('years')

        # Create a DataFrame with selected years and occupation
        filtered_data = pd.concat([data_by_year[int(year)] for year in selected_years], ignore_index=True)

        # Generate analysis results
        top_skills = filtered_data.groupby('Skill')['Count'].sum().nlargest(10)
        
        # Check if top_skills is empty or undefined
        if top_skills.empty:
            top_skills = []  # Assign an empty list as a default value

        return render_template('analysis.html', 
                               selected_occupation=selected_occupation,
                               selected_municipality=selected_municipality,
                               selected_years=selected_years,
                               top_skills=top_skills)

    # Here we assume that top_skills is defined and available
    # You need to define or retrieve top_skills appropriately
    top_skills = data_by_year[2018].groupby('Skill')['Count'].sum().nlargest(10)

    return render_template('analysis.html', top_skills=top_skills,
                           occupation_options=data_by_year[2018]['Occupation Field'].unique().tolist(),
                           municipality_options=data_by_year[2018]['Municipality'].unique().tolist(),
                           years_options=list(data_by_year.keys()))



# Route for the AI page
@app.route('/ai', methods=['GET', 'POST'])
def ai_page():
    if request.method == 'POST':
        # Generate AI text based on form input
        selected_competence = request.form['selected_competence']
        generated_text = generate_text(selected_competence)
        
        # Render AI template with generated text
        return render_template('ai.html', generated_text=generated_text)

    # Render AI page with form to select a competence
    all_competencies = set()
    for data in data_by_year.values():
        all_competencies.update(data['Skill'].unique())

    return render_template('ai.html', all_competencies=all_competencies)

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)

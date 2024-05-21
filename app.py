from flask import Flask, render_template, request
import pandas as pd
from openaifunctions import config_api, generate_text

app = Flask(__name__)

#OPEN AI API 
config_api()


# Load CSV files into a dictionary
csv_files = {}
for year in range(2018, 2023):
    csv_files[str(year)] = pd.read_csv(f'CSVfiler/skills_by_occupation_update{year}.csv')

# Get unique values for occupation, municipality, and years
all_occupations = set()
all_municipalities = set()
all_years = [str(year) for year in range(2018, 2023)]

for year_data in csv_files.values():
    all_occupations.update(year_data['Occupation Field'].unique())
    all_municipalities.update(year_data['Municipality'].unique())

@app.route('/')
def home():
    return render_template('home.html', occupation_options=all_occupations,
                                         municipality_options=all_municipalities,
                                         years_options=all_years)

@app.route('/statistik', methods=['POST', 'GET'])
def statistik_page():
    if request.method == 'POST':
        occupation = request.form['occupation']
        municipality = request.form['municipality']
        year = request.form['years']
        
        # Filter data based on user input
        filtered_data = csv_files[year][(csv_files[year]['Occupation Field'] == occupation) & 
                                         (csv_files[year]['Municipality'] == municipality)]
        
        # Get top 10 skills
        top_skills = filtered_data.groupby('Skill').sum()['Count'].nlargest(10)
        
        # Convert top_skills to list of tuples for passing to template
        top_skills_list = list(top_skills.items())
        
        return render_template('statistik.html', top_skills=top_skills_list,
                                             occupation_options=all_occupations,
                                             municipality_options=all_municipalities,
                                             years_options=all_years)
    else:
        return render_template('statistik.html', occupation_options=all_occupations,
                                             municipality_options=all_municipalities,
                                             years_options=all_years)

@app.route('/home')
def home_page():
    return render_template('home.html')


# Route for the AI page
@app.route('/kompetenslexikon', methods=['GET', 'POST'])
def ai_page():
    if request.method == 'POST':
        # Generate AI text based on form input
        selected_competence = request.form['selected_competence']
        generated_text = generate_text(selected_competence)
        
        # Render AI template with generated text
        return render_template('kompetenslexikon.html', generated_text=generated_text)

    # Render AI page with form to select a competence
    all_competencies = set()
    for data in csv_files.values():
        all_competencies.update(data['Skill'].unique())

    return render_template('kompetenslexikon.html', all_competencies=all_competencies)


if __name__ == '__main__':
    app.run(debug=True)

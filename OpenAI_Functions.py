import streamlit as st
from openai import OpenAI

import pandas as pd
import re

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
ghost = os.getenv("API_KEY")
client = OpenAI(api_key=ghost)


#Funktion Med AI
def generate_text(prompt):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Du är en näringslivsexpert som förklarar kompetenser och fokuserar på dess användningsområden i samhället och hur den appliceras i organisationer."},
        #{skriv en negativ prompt till systemet}
        {"role": "user", "content": "Skriv en strukturerad text som först förklarar kompetensen " + prompt +" och sedan ber."},
        {"role": "user", "content": "Ifall " + prompt + " består av flera kompetenser, förklara vikten av sambandet mellan dessa kompetenser."}
    ]
    ) 
    answer = response.choices[0].message
    return answer


#DATA
# Load data from CSV files and store them in a dictionary
data_by_year = {}
for year in range(2018, 2023):
    file_path = f"./CSVfiler/skills_by_occupation_update{year}.csv"
    try:
        data = pd.read_csv(file_path)
        file_year = re.search(r'\d{4}', file_path).group()
        data['Year'] = int(file_year)
        data_by_year[year] = data
    except FileNotFoundError:
        st.error(f"Data for year {year} not found.")




# Get all unique competencies from the data
all_competencies = set()
for data in data_by_year.values():
    all_competencies.update(data['Skill'].unique())


#HUVUDKOD/Visualiseringen
# Streamlit-app titel
st.title("Generera text om kompetenser")


# Dropdown menu for selecting competence
selected_competence = st.selectbox("Välj en kompetens", list(all_competencies))


# Generera och visa text när användaren klickar på knappen
if st.button("Generera text"):
    prompt = selected_competence #om jag vill ändra selected competence till en lista 
    generated_text = generate_text(prompt)
    st.text_area("Genererad text", generated_text)

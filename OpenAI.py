"sk-proj-TnYIP0TvCZic4v5Q5zPdT3BlbkFJWuxegZ3lzp4rq48h75OG"

import streamlit as st
from openai import OpenAI
client = OpenAI(api_key="sk-proj-TnYIP0TvCZic4v5Q5zPdT3BlbkFJWuxegZ3lzp4rq48h75OG")

def generate_text(prompt):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Du är en näringslivsexpert som förklarar kompetenser och fokuserar på dess användningsområden i samhället och hur den appliceras i organisationer."},
        {"role": "user", "content": "Skriv en strukturerad text som först förklarar kompetensen " + prompt +" och sedan ber."},
        {"role": "user", "content": "Ifall " + prompt + "är flera kompetenser, förklara sambandet och dess betydelse."}
    ]
    ) 
    answer = response.choices[0].message
    return answer







# Dictionary med kompetenser och deras beskrivningar (ersätt med dina egna data)
competencies_data = {
    "Python-programmering": "Beskrivning av Python-programmering...",
    "Dataanalys": "Beskrivning av dataanalys...",
    "Maskininlärning": "Beskrivning av maskininlärning...",
    # Lägg till fler kompetenser här...
}

"""
# Läs in CSV-filerna för varje år och lagra dem i en dictionary
data_by_year = {}
for year in range(2016, 2023):
    file_path = f"./skills_by_occupation_{year}.csv"
    try:
        data = pd.read_csv(file_path)
        # Extrahera året från filnamnet
        file_year = re.search(r'\d{4}', file_path).group()
        data['Year'] = int(file_year)
        data_by_year[year] = data
    except FileNotFoundError:
        st.error(f"Data for year {year} not found.")

"""



#HUVUDKOD
# Streamlit-app titel
st.title("Generera text om kompetenser")

# Dropdown-menyn för att välja kompetens
selected_competence = st.selectbox("Välj en kompetens", list(competencies_data.keys()))


# Generera och visa text när användaren klickar på knappen
if st.button("Generera text"):
    prompt = selected_competence #om jag vill ändra selected competence till en lista 
    generated_text = generate_text(prompt)
    st.text_area("Genererad text", generated_text)

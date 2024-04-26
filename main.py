import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Använd tema "dark"
st.set_page_config(page_title="My Streamlit App", page_icon=":rocket:", layout="centered", initial_sidebar_state="expanded")
col1, col2, col3 = st.columns(3)

st.markdown(
    """
    <style>
        .top-bar {
            background-color: #333;
            color: white;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo {
            font-size: 24px;
            font-weight: bold;
        }
        .menu-item {
            margin-left: 20px;
            cursor: pointer;
            border: none;
            background: none;
            color: white;
            font-size: 16px;
        }
        .menu-item:hover {
            text-decoration: underline;
        }
        .page-content {
            display: none;
        }
    </style>
    """
    , unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="top-bar">
        <div class="logo">My Streamlit App</div>
        <div class="menu">
            <button class="menu-item" onclick="showPage('home')">Home</button>
            <button class="menu-item" onclick="showPage('about')">About</button>
            <button class="menu-item" onclick="showPage('contact')">Contact</button>
        </div>
    </div>
    <div class="page-content" id="home-content">
        <h2>Welcome to the Home Page!</h2>
        <p>This is the home page of our application.</p>
        <p>Here, you can find information about various topics.</p>
        <img src="https://via.placeholder.com/400" alt="Home Page Image">
        <p>For more details, explore further!</p>
    </div>
    <div class="page-content" id="about-content">
        <h2>Welcome to the About Page!</h2>
        <p>Learn more about our application and its creators here.</p>
        <p>We strive to provide useful insights and tools for our users.</p>
        <img src="https://via.placeholder.com/400" alt="About Page Image">
        <p>Feel free to reach out to us for any inquiries!</p>
    </div>
    <div class="page-content" id="contact-content">
        <h2>Welcome to the Contact Page!</h2>
        <p>Contact us if you have any questions or feedback.</p>
        <p>We are here to assist you!</p>
        <img src="https://via.placeholder.com/400" alt="Contact Page Image">
        <p>Feel free to fill out the form below:</p>
        <form>
            <label for="name">Name:</label><br>
            <input type="text" id="name" name="name"><br>
            <label for="email">Email:</label><br>
            <input type="email" id="email" name="email"><br><br>
            <label for="message">Message:</label><br>
            <textarea id="message" name="message" rows="4" cols="50"></textarea><br><br>
            <input type="submit" value="Submit">
        </form>
    </div>
    <script>
        function showPage(page) {{
            var pages = ['home', 'about', 'contact'];
            for (var i = 0; i < pages.length; i++) {{
                var pageId = pages[i] + '-content';
                var pageContent = document.getElementById(pageId);
                if (page === pages[i]) {{
                    pageContent.style.display = 'block';
                }} else {{
                    pageContent.style.display = 'none';
                }}
            }}
        }}
    </script>
    """
    , unsafe_allow_html=True
)

# Läs in CSV-filerna för varje år och lagra dem i en dictionary
data_by_year = {}
for year in range(2018, 2023):
    file_path = f"./CSVfiler/skills_by_occupation_update{year}.csv"
    try:
        data = pd.read_csv(file_path)
        # Extrahera året från filnamnet
        file_year = re.search(r'\d{4}', file_path).group()
        data['Year'] = int(file_year)
        data_by_year[year] = data
    except FileNotFoundError:
        st.error(f"Data for year {year} not found.")

# Streamlit-applikation
st.title("Skills Analysis")

# Dropdown för att välja yrkesgrupp
occupation_options = sorted(set(data_by_year[2018]['Occupation Field']))
selected_occupation = st.selectbox("Choose Occupation Field", occupation_options)

# Multiselect för att välja år
years_options = list(data_by_year.keys())
selected_years = st.multiselect("Choose Years", years_options, default=years_options)

# Visa varning om inga år är valda
if not selected_years:
    st.warning("Please choose at least one year.")
else:
    # Skapa en DataFrame med valda år och yrkesgrupp
    filtered_data = pd.concat([data_by_year[year][data_by_year[year]['Occupation Field'] == selected_occupation] for year in selected_years], ignore_index=True)

    # Diagram för de mest vanliga kompetenserna
    if not filtered_data.empty:
        st.subheader(f"Top 10 Skills for {selected_occupation} ({', '.join(map(str, selected_years))})")
        top_skills = filtered_data.groupby('Skill')['Count'].sum().nlargest(10)

        # Skapa en figur och en axel för plotten med önskad storlek
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plotta datan på axeln med vald färg och linjetyp
        sns.barplot(x=top_skills.values, y=top_skills.index, ax=ax)
        ax.set_xlabel('Count')
        ax.set_ylabel('Skill')
        ax.set_title(f"Top 10 Skills for {selected_occupation} ({', '.join(map(str, selected_years))})")

        # Lägg till en checkbox för varje kompetens
        selected_skills = st.multiselect("Choose Skills", top_skills.index)

        # Visa plotten i Streamlit
        st.pyplot(fig)

        # Skapa en trendkurva för valda år om mer än ett år är valt
        if len(selected_years) > 1:
            st.subheader(f"Trend for Top 10 Skills for {selected_occupation}")

            # Filtera datan baserat på valda kompetenser
            selected_skills_data = filtered_data[filtered_data['Skill'].isin(selected_skills)]

            # Skapa en figur och en axel för trendkurvan
            fig_trend, ax_trend = plt.subplots(figsize=(10, 6))

            # Plotta datan på axeln med linjediagram utan skuggning
            sns.lineplot(data=selected_skills_data, x='Year', y='Count', hue='Skill', marker='o', ci=None, ax=ax_trend)

            # Anpassa text och etiketter
            ax_trend.set_xlabel('Year', fontsize=14)
            ax_trend.set_ylabel('Count', fontsize=14)
            ax_trend.set_title(f"Trend for Top 10 Skills for {selected_occupation} over selected years", fontsize=16)
            ax_trend.legend(fontsize=12)

            # Visa trendkurvan i Streamlit
            st.pyplot(fig_trend)
    else:
        st.error("No data available for selected occupation field and year(s).")
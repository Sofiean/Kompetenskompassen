
Hej!

Vi har gjort applikationen KompetensKompassen som tillåter kommuner att  enkelt få överblick över vilka kompetenser arbetsgivare inom olika branscher och sektorer söker efter. 
Klicka på länken för att utforska våran app. http://kompetenskompassen.pythonanywhere.com/

**Beskrivning av kod:**

Applikationen är kodad med flask ramverket i python och använder även html samt javascript. Vi hämtar även en API-nyckel från OpenAI som ligger i en .env fil.
App.py hämtar OpenAI chatgpt 3.5 baserade funktionen "generate_text" och funktionen "config_api" från openaifuntions.py
App.py hämtar också data från CSVfiler som har skapats i filen skapacsv.py. Denna data har ursprungligen utvunnits från jobtechs databas, https://jobtechdev.se/sv.

**Moduler:** 

pip install --upgrade openai

pip install python-dotenv

pip install flask

pip install pandas

För att installera alla moduler skriv pip install -r requirements.txt

**API-nyckel:**

1. För att köra koden krävs det att man erhåller en egen API-nyckel från OpenAI. Skapa den här https://platform.openai.com/api-keys.
2. Skapa en fil i Kompetenskompassen mappen och namnge den ".env".
3. I .env filen skriver du endast "API_KEY = "din api nyckel här"". Exempelvis  API_KEY = "sk-12345abcde67890FGHIJklmnopQRSTUVwxyz"


**Köra koden:**

1. Öppna en terminal.
2. Se till att du är i KompetensGapet mappen, annars skriver du till exempel "cd /Users/Gustav/Documents/GitHub/KompetensKompassen"
3. Kör sedan koden genom att skriva in "python app.py"
4. Du får då en adress,"http://127.0.0.1:5000/", till en lokal server som du kopierar och söker på i valfri webbläsare. 





Hej!

Vi har gjort applikationen KompetensKompassen som tillåter kommuner att  enkelt få överblick över vilka kompetenser arbetsgivare inom olika branscher och sektorer söker efter.
Klicka på länken för att utforska våran app. http://kompetenskompassen.pythonanywhere.com/

Beskrivning av kod:

Applikationen är kodad med flask ramverket i python och använder även html samt javascript. Vi hämtar även en API-nyckel från OpenAI som ligger i en .env fil.
App.py hämtar OpenAI chatgpt 3.5 baserade funktionen "generate_text" och funktionen "config_api" från openaifuntions.py
Vi hämtar jobbdata från jobtech och skapar CSVfiler.

Moduler: 

pip install --upgrade openai
pip install python-dotenv
pip install flask
pip install pandas
För att installera alla moduler skriv pip install -r requirements.txt




API-nyckel:

1. För att köra koden krävs det att man erhåller en egen api nyckel från OpenAI. Skapa den här https://platform.openai.com/api-keys.
2. Skapa en fil i Kompetenskompassen mappen och namnge den ".env".
3. I den skriver du endast API_KEY = "din api nyckel här" 

Köra koden:

1. Öppna en terminal.
2. Se till att du är i KompetensGapet mappen, annars skriver du till exempel "cd /Users/Gustav/Documents/GitHub/KompetensKompassen"
3. Kör sedan koden genom att skriva in "python app.py"
4. Du får då en adress till en lokal server som du kopierar och söker på i valfri webbläsare. "http://127.0.0.1:5000/"




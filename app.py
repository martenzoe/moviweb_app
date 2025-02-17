from datamanager import create_app  # Importiert die Application Factory

# Erstellt die Flask-App durch Aufruf der Factory-Funktion
app = create_app()

if __name__ == '__main__':
    # Startet den Flask-Entwicklungsserver
    app.run(debug=True)

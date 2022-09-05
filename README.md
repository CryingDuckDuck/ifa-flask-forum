# IFA Praxisarbeit - Flask Forum

## Lokale Entwicklungsumgebung aufsetzen

- Python installieren: https://www.python.org/downloads/
- Postgresql installieren: https://www.postgresql.org/download/

```bash
    $ git clone https://github.com/CryingDuckDuck/ifa-praxisarbeit
    
    $ cd ifa-praxisarbeit
    
    # virtualenv generieren
    $ python -m venv venv
    
    # virtualenv aktivieren
    $ source venv/bin/activate
    $ venv\Scripts\activate.bat (windows)
    
    # Packages installieren
    $ pip install -r requirements.txt
```
In der Datei .env.example findet man Umgebungsvariablen mit denen die Applikation konfiguriert werden kann. 
Die Datei sollte kopiert und zu ".env" umbenannt werden. Diese Datei sollte nicht gepusht werden.

Die Variable FLASK_SQLALCHEMY_DATABASE_URI ist der Connectionstring für die Postgresql Datenbank, gegebenfalls müssen 
die Userdaten und der Datenbankname angepasst werden.

Danach kann die Datenbank mit Daten initialisiert werden:

```bash
$ flask seed-db
```

App laufen lassen:

```bash
$ flask run
```


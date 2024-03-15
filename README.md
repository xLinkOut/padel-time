# 🏓 PadelTime
Sistema di prenotazione per partite di Padel.

## Build 'n run

### Environment
Dal file `.env.example` creare una copia `.env` ed inserire i dati necessari al funzionamento (informazioni sul database, eccetera).

### Database
L'applicazione e' pensata per funzionare con un database relazionale. E' possibile utilizzare il Dockerfile fornito per avviare un container MySQL.

```bash
docker build -t padel-time-db .
docker run -d -p 3306:3306 --name padel-time-db padel-time-db
```

### Server
Il backend e' scritto in Flask. Per avviarlo, installare il necessario (opzionale: in un virtualenv) e avviare il server:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd src/
flask --app main.py run [--debug]
```

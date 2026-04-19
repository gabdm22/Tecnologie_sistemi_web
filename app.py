from flask import Flask, request, render_template, redirect, session
import sqlite3
import os
from werkzeug.security import generate_password_hash


app = Flask(__name__)

os.makedirs("static/uploads", exist_ok=True)

def get_connection_db():
    conn = sqlite3.connect('mova_db.db')
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------------------------------------------------

#home page
@app.route('/')
def home():
    return render_template('welcome.html')

# -----------------------------------------------------------------------

# vetrina
@app.route('/vetrina.html')
def mostra_vetrina():
    conn = get_connection_db()
    opere_db = conn.execute("SELECT * FROM opera").fetchall()
    conn.close()

    return render_template("vetrina.html", opere=opere_db)

# -----------------------------------------------------------------------

# pagina vendita
@app.route('/form_vendita.html')
def vendi():
    return render_template("form_vendita.html")


# upload
@app.route('/upload', methods=["POST"])
def carica_opera():
    nome = request.form["nome"]
    prezzo = request.form["prezzo"]
    categoria = request.form["categoria"]
    dimensioni = request.form["dimensioni"]
    immagine = request.files["immagine"]

    if immagine:
        nome_img = immagine.filename
        percorso_salv = os.path.join("static/uploads", nome_img)
        immagine.save(percorso_salv)

        conn = get_connection_db()
        conn.execute("INSERT INTO opera (nome, prezzo, categoria, dimensioni, immagine) VALUES (?, ?, ?, ?, ?)", (nome, prezzo, categoria, dimensioni, nome_img))
        conn.commit()
        conn.close()

        return render_template("/form_vendita.html", caricato=True)
    else:
        return render_template("/form_vendita.html", caricato=False)

# -----------------------------------------------------------------------

# pagina acquisto
@app.route('/form_acquisto.html')
def mostra_pag_acquisto():
    return render_template("/form_acquisto.html")





# -----------------------------------------------------------------------

# pagina registrazione
@app.route('/form_registrazione.html')
def registra():
    return render_template("form_registrazione.html")

# registrazione
@app.route('/registrazione', methods=["POST"])
def registazione():
    nome = request.form["nome"]
    cognome = request.form["cognome"]
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    verifica_password = request.form["verifica_password"]
    if not all([nome, cognome, username, email, password, verifica_password]):
        return "ERRORE! tutti i campi sono obbligatori",400
    if password != verifica_password:
        return "ERRORE! le password non coincidono",400
    if len(password) < 8:
        return "ERRORE! la password deve essere lunga almeno 8 caratteri",400
    if not (any(c.isupper() for c in password) and any(c.islower() for c in password) and any(c.isdigit() for c in password)):
        return "ERRORE! la password deve contenere almeno una lettera maiuscola, una lettera minuscola e un numero",400
    
    conn = get_connection_db()
    # Controlla se l'username esiste già
    utente_esistente = conn.execute("SELECT * FROM utente WHERE username = ?", (username,)).fetchone()
    if utente_esistente:
        conn.close()
        return "ERRORE! username già esistente",400
    #genera hash della password e salva utente
    password_hash = generate_password_hash(password)
    conn.execute("INSERT INTO utente (nome, cognome, username, email, password) VALUES (?, ?, ?, ?, ?)", (nome, cognome, username, email, password_hash))
    conn.commit()
    conn.close()
    return redirect("/vetrina.html")













# pagina assistenza
@app.route('/form_assistenza.html', methods=['GET', 'POST'])
def assistenza():
    if request.method == 'POST':
        oggetto = request.form['oggetto']
        mess = request.form['messaggio']

        print('-- Ricevuta nuova richiesta assistenza --')
        print(f'Oggetto: {oggetto}')
        print(f'Messaggio: {mess}')

        return render_template("form_assistenza.html", inviato=True)

    return render_template("form_assistenza.html", inviato=False)


if __name__=="__main__":
    app.run(host='0.0.0.0', port=5500, debug=True)
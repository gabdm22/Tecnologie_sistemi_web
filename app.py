from flask import Flask, jsonify, request, render_template, redirect, session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


app = Flask(__name__)

app.secret_key = 'secret_key_mova'

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
    autore = session.get('username')
    if not autore:  # blocco l'accesso alla pagina di vendita a chi non è loggato 
        return redirect('/form_login.html')
    
    return render_template("form_vendita.html")


# vendita
@app.route('/upload', methods=["POST"])
def carica_opera():
    autore = session.get('username')
    if not autore:  # blocco la vendita a chi non è loggato
        return redirect('/form_login.html')

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
        conn.execute("INSERT INTO opera (nome, autore, prezzo, categoria, dimensioni, immagine) VALUES (?, ?, ?, ?, ?, ?)", (nome, autore, prezzo, categoria, dimensioni, nome_img))
        conn.commit()
        conn.close()

        return render_template("/form_vendita.html", caricato=True)
    else:
        return render_template("/form_vendita.html", caricato=False)

# -----------------------------------------------------------------------

# pagina acquisto
@app.route('/form_acquisto.html')
def mostra_pag_acquisto():
    autore = session.get('username')
    if not autore:
        return redirect("/form_login.html")
    
    id_opera_da_acquistare = request.args.get('id_opera')
    return render_template("/form_acquisto.html", acquistato=False, id_opera=id_opera_da_acquistare)

@app.route('/acquista', methods=["POST"])
def acquista_opera():
    utente_loggato = session.get('username')
    if not utente_loggato:
        return redirect("/form_login.html")
    
    id_opera = request.form.get('id_opera')
    indirizzo = request.form.get('indirizzo')
    numero_carta = request.form.get('numero_carta')
    scadenza = request.form.get('scadenza')

    conn = get_connection_db()

    try:
        # salvo il prezzo in tabella ORDINE
        opera = conn.execute("SELECT prezzo FROM opera WHERE id = ?", (id_opera,)).fetchone()
        prezzo_opera = opera['prezzo']
        cursor = conn.cursor()

        # salvo l'indirizzo in INDIRIZZO
        cursor.execute(
            "INSERT INTO indirizzo (via, citta, cap, id_utente) VALUES (?, ?, ?, ?)",
            (indirizzo, 'N/D', 'N/D', utente_loggato)
        )
        id_indirizzo_generato = cursor.lastrowid

        # salvo il metodo di pagamento in METODO DI PAGAMENTO
        if numero_carta:
            ultime_4 = numero_carta[-4:]
        else:
            ultime_4 = '0000'
        cursor.execute(
            "INSERT INTO metodo_pagamento (provider, scadenza, ultime_4_cifre, token_pagamento, id_utente) VALUES (?, ?, ?, ?, ?)",
            ("Carta di credito", scadenza, ultime_4, "fake_token_123", utente_loggato)
        )

        # creo l'ordine generale in ORDINE
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO ordine (data, stato, totale, id_utente, id_indirizzo) VALUES (?, ?, ?, ?, ?)",
            (data, "Completato", prezzo_opera, utente_loggato, id_indirizzo_generato)
        )
        id_ordine_generato = cursor.lastrowid

        #creo l'ordine dettagliato in ORDINE_OPERA
        cursor.execute(
            "INSERT INTO ordine_opera (id_ordine, id_opera, prezzo_acquisto) VALUES (?, ?, ?)",
            (id_ordine_generato, id_opera, prezzo_opera)
        )

        # tolgo l'opera dalla vetrina
        cursor.execute(
            "UPDATE opera SET disponibilita=0 WHERE id=?",
            (id_opera,)
        )

        conn.commit()
        esito_acquisto = True

    except Exception as e:
        conn.rollback()
        esito_acquisto = False

    conn.close()
    return render_template("/form_acquisto.html", acquistato=esito_acquisto)


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
# -----------------------------------------------------------------------
#pagina login
@app.route("/form_login.html")
def login():
    return render_template("form_login.html")
#login 
@app.route("/login", methods=["POST"])
def effettua_login():
    username = request.form["username"]
    password = request.form["password"]
    conn = get_connection_db()
    utente = conn.execute("SELECT * FROM utente WHERE username = ?", (username,)).fetchone()
    conn.close()
    if utente and check_password_hash(utente['password'],password):
        # session['utente_id'] = utente['id']
        session['username'] = utente['username']
        return jsonify({"success": True, "redirect": "/vetrina.html"}), 200
    else:
        return jsonify({"success": False, "message": "username o password errati"}), 401

            

 













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
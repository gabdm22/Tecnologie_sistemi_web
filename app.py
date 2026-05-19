from flask import Flask, jsonify, request, render_template, redirect, session, url_for
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta


app = Flask(__name__)

# genera una chiave casuale di 24 byte ogni volta che il server parte
app.secret_key = os.urandom(24)

# imposto un timer per mantenere la sessione attiva 60 minuti
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)

os.makedirs("static/uploads", exist_ok=True)

def get_connection_db():
    conn = sqlite3.connect('mova_db.db')
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------------------------------------------------

#home page
@app.route('/')
def home():
    """
    Mostra la schermata di benvenuto al sito
    """

    return render_template('welcome.html')



# -------------------------------- VETRINA -------------------------------------
# -----------------------------------------------------------------------

# vetrina
@app.route('/vetrina.html')
def mostra_vetrina():
    """
    Mostra la pagina della vetrina utilizzando jinja2 per il rendering dinamico dei dati in database
    """

    conn = get_connection_db()
    opere_carrello = []
    utente_loggato = session.get('username')

    if utente_loggato:
        opere_db = conn.execute("SELECT * FROM opera WHERE autore!=?", (utente_loggato,)).fetchall()

        carrello = conn.execute("SELECT id_opera FROM in_carrello WHERE id_utente=?", (utente_loggato,)).fetchall()
        for elem in carrello:
            opere_carrello.append(elem['id_opera'])
    else:
        opere_db = conn.execute("SELECT * FROM opera").fetchall()
    
    conn.close()

    return render_template("vetrina.html", opere=opere_db, in_carrello=opere_carrello)



# --------------------------------- VENDITA -------------------------------------
# -----------------------------------------------------------------------

# pagina vendita
@app.route('/form_vendita.html')
def vendi():
    """
    Mostra la pagina del form per la vendita delle opere
    """

    autore = session.get('username')
    if not autore:  # blocco l'accesso alla pagina di vendita a chi non è loggato 
        return redirect('/form_login.html')
    
    return render_template("form_vendita.html")


# vendita
@app.route('/upload', methods=["POST"])
def carica_opera():
    """
    Effettua l'inserimento in database dei dati inseriti dall'utente in form di vendita
    """

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


# ------------------------------ ACQUISTO E CARRELLO ----------------------------------------
# -----------------------------------------------------------------------

# pagina acquisto
@app.route('/form_acquisto.html')
def mostra_pag_acquisto():
    """
    Mostra la pagina del form di acquisto
    """

    utente_loggato = session.get('username')
    if not utente_loggato:
        return redirect("/form_login.html")
    
    id_opera_da_acquistare = request.args.get('id_opera')
    provenienza_carrello = request.args.get('da_carrello') == 'true'
    conn = get_connection_db()
    opere_da_acquistare = []
    if provenienza_carrello:
        query = """
            SELECT o.* from in_carrello ic JOIN opera o ON ic.id_opera=o.id
            WHERE ic.id_utente = ? and o.disponibilita=1
           """
        opere_da_acquistare = conn.execute(query, (utente_loggato,)).fetchall()
    elif id_opera_da_acquistare:
        opera = conn.execute("SELECT * FROM opera WHERE id = ? AND disponibilita=1", (id_opera_da_acquistare,)).fetchone()
        if opera:
            opere_da_acquistare = [opera]
    conn.close()
    if not opere_da_acquistare:
        return redirect("/vetrina.html")
    totale = sum(float(op['prezzo']) for op in opere_da_acquistare)
    
    return render_template("/form_acquisto.html", 
                           acquistato=False, 
                           opere=opere_da_acquistare, 
                           totale=totale,
                           da_carrello=provenienza_carrello)
    

@app.route('/acquista', methods=["POST"])
def acquista_opera():
    """
    Inserisce in database i dati inseriti dall'utente nel form di acquisto ed effettua l'acquisto dell'opera
    """

    utente_loggato = session.get('username')
    if not utente_loggato:
        return redirect("/form_login.html")
    #carrello o acquisto diretto?
    da_carrello = request.form.get('da_carrello') == 'true'
    id_opera = request.form.get('id_opera')
    indirizzo = request.form.get('indirizzo')
    numero_carta = request.form.get('numero_carta')
    scadenza = request.form.get('scadenza')

    conn = get_connection_db()

    try:
        # salvo il prezzo in tabella ORDINE
        cursor = conn.cursor()
        #opere da processare
        if da_carrello:
            opere = cursor.execute("""
                SELECT o.id, o.prezzo FROM in_carrello ic JOIN opera o ON ic.id_opera=o.id
                WHERE ic.id_utente = ? and o.disponibilita=1    
            """, (utente_loggato,)).fetchall()
        else:
            res = cursor.execute("SELECT id, prezzo FROM opera WHERE id = ?", (id_opera,)).fetchone()
            opere = [res] if res else []
            prezzo_opera = res['prezzo'] if res else 0
        if not opere:
            raise Exception("Nessuna opera disponibile per l'acquisto")
        
        prezzo_totale_ordine = sum(float(op['prezzo']) for op in opere)



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
            (data, "Completato", prezzo_totale_ordine, utente_loggato, id_indirizzo_generato)
        )
        id_ordine_generato = cursor.lastrowid

        #CICLO PER OGNI OPERA
        for op in opere:
            cursor.execute("INSERT INTO ordine_opera (id_ordine, id_opera, prezzo_acquisto) VALUES (?, ?, ?)",
                           (id_ordine_generato, op['id'], op['prezzo']))
            
            # Settiamo a non disponibile
            cursor.execute("UPDATE opera SET disponibilita=0 WHERE id=?", (op['id'],))

        conn.commit()
        esito_acquisto = True

    except Exception as e:
        print(f"ERRORE: {e}")
        conn.rollback()
        esito_acquisto = False

    conn.close()
    return render_template("/form_acquisto.html", acquistato=esito_acquisto)

# -----------------------------------------------------------------------

#pagina carrello
@app.route('/carrello.html')
def mostra_carrello():
    """
    Mostra la pagina del carrello utilizzando jinja2 per il rendering dinamico dei dati in database
    """
    
    utente_loggato = session.get('username')
    if not utente_loggato:
        return redirect("/form_login.html")
    
    conn = get_connection_db()
    query = """
        SELECT o.id, o.nome, o.prezzo, o.immagine
        FROM in_carrello ic JOIN opera o ON ic.id_opera=o.id
        WHERE ic.id_utente = ? and o.disponibilita=1
    """#prendo tutte le opere che sono nel carrello dell'utente loggato e che sono ancora disponibili (disponibilita=1)
    opere_in_carrello = conn.execute(query, (utente_loggato,)).fetchall()
    totale = sum(opera['prezzo'] for opera in opere_in_carrello)

    conn.close()
    return render_template("carrello.html", opere=opere_in_carrello,totale=totale)


#aggiungi al carrello
@app.route('/aggiungi_al_carrello/<int:id_opera>')
def aggiungi_al_carrello(id_opera):
    """
    Aggiunge alla tabella "in_carrello" l'opera identificata da "id_opera"
    """
    
    username = session.get('username')
    if not username:
        return redirect("/form_login.html")
    conn = get_connection_db()
    try:
        conn.execute("INSERT INTO in_carrello (id_opera, id_utente) VALUES (?, ?)", (id_opera, username))
        conn.commit()
    except sqlite3.IntegrityError:
        pass    
    conn.close()
    return redirect(url_for('mostra_carrello'))


#rimuovi dal carrello
@app.route('/rimuovi_dal_carrello/<int:id_opera>')
def rimuovi_dal_carrello(id_opera):
    """
    Rimuove dalla tabella "in_carrello" l'opera identificata da "id_opera"
    """

    username = session.get('username')
    if not username:
        return redirect("/form_login.html")
    conn = get_connection_db()
    conn.execute("DELETE FROM in_carrello WHERE id_opera = ? AND id_utente = ?", (id_opera, username))
    conn.commit()
    conn.close()
    return redirect(url_for('mostra_carrello'))





# -----------------------------AUTENTICAZIONE E PROFILO -----------------------------------------
# -----------------------------------------------------------------------

# pagina registrazione
@app.route('/form_registrazione.html')
def registra():
    """
    Mostra la pagina del form di registrazione
    """
    
    return render_template("form_registrazione.html")



# registrazione
@app.route('/registrazione', methods=["POST"])
def registazione():
    """
    Inserisce in database i dati di registrazione del form
    """

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
    # Controlla se l'email esiste già
    email_esistente = conn.execute("SELECT * FROM utente WHERE email = ?", (email,)).fetchone()
    if email_esistente:
        conn.close()
        return "ERRORE! email già esistente",400
    #genera hash della password e salva utente
    password_hash = generate_password_hash(password)
    conn.execute("INSERT INTO utente (nome, cognome, username, email, password) VALUES (?, ?, ?, ?, ?)", (nome, cognome, username, email, password_hash))
    conn.commit()
    conn.close()
    return render_template("/form_registrazione.html", registrato=True)


#endpoint per testare se email o utente esistono già durante la registrazione
@app.route('/verifica-unicita', methods=['POST'])
def verifica_unicita():
    """
    Verifica che username e email che vengono inserite siano univoche
    """

    data = request.get_json()
    campo = data.get('campo')
    valore = data.get('valore')
    if campo not in ['username', 'email']:
        return jsonify({"errore": "Campo non valido"}), 400
    conn = get_connection_db()
    #basta una riga 
    query = f"SELECT 1 FROM utente WHERE {campo} = ?"
    #controllo 
    risultato = conn.execute(query, (valore,)).fetchone()
    conn.close()
    return jsonify({"disponibile": risultato is None})


# -----------------------------------------------------------------------

#pagina login
@app.route("/form_login.html")
def login():
    """
    Mostra la pagina del form di login
    """

    session.clear()
    return render_template("form_login.html")


#login 
@app.route("/login", methods=["POST"])
def effettua_login():
    """
    Effettua il login con i dati inseriti. Se sono corretti crea la sessione della durata di 60 minuti
    """

    session.permanent = True    # attiva il timer della sessione
    username = request.form["username"]
    password = request.form["password"]
    conn = get_connection_db()
    utente = conn.execute("SELECT * FROM utente WHERE username = ?", (username,)).fetchone()
    conn.close()
    if utente and check_password_hash(utente['password'],password):
        session['username'] = utente['username']
        return jsonify({"success": True, "redirect": "/vetrina.html"}), 200
    else:
        return jsonify({"success": False, "message": "username o password errati"}), 401


# -----------------------------------------------------------------------
            
# logout
@app.route('/logout')
def logout():
   """
   Cancella la sessione corrente
   """

   session.clear() # Azzera completamente la sessione
   return redirect('/vetrina.html')


# -----------------------------------------------------------------------

# profilo
@app.route('/profilo.html')
def mostra_profilo():
    """
    Mostra la pagina del profilo dell'utente in sessione
    """

    utente_loggato = session.get('username')
    if not utente_loggato:
        return redirect("/form_login.html")
    
    conn = get_connection_db()

    query_acquisti = """
        SELECT o.id_ordine, op.id AS id_opera, o.data, oo.prezzo_acquisto AS prezzo, op.nome, op.immagine, op.autore
        FROM ordine o JOIN ordine_opera oo on o.id_ordine=oo.id_ordine JOIN opera op ON oo.id_opera=op.id
        WHERE o.id_utente = ? AND IFNULL(oo.rimosso, 0)=0
        ORDER BY o.data DESC
    """

    query_vendite = """
        SELECT op.nome, op.immagine, op.autore, oo.prezzo_acquisto AS prezzo, o.data
        FROM opera op JOIN ordine_opera oo ON op.id=oo.id_opera JOIN ordine o ON oo.id_ordine=o.id_ordine
        WHERE op.autore = ?
        ORDER BY o.data DESC
    """

    lista_acquisti = conn.execute(query_acquisti, (utente_loggato,)).fetchall()
    lista_vendite = conn.execute(query_vendite, (utente_loggato,)).fetchall()
    conn.close()
    
    return render_template("profilo.html", acquisti=lista_acquisti, vendite=lista_vendite)


@app.route('/rimuovi/<int:id_ordine>/<int:id_opera>')
def rimuovi_da_collezione(id_ordine, id_opera):
    """
    Effettua il soft-delete dell'opera in database passata in input aggiornando a 1 il valore del flag "rimosso"
    """

    conn = get_connection_db()
    conn.execute("UPDATE ordine_opera SET rimosso=1 WHERE id_ordine=? AND id_opera=?", (id_ordine, id_opera))
    conn.commit()
    conn.close()
    return redirect("/profilo.html")




# ------------------------------ ASSISTENZA ----------------------------------------
# -----------------------------------------------------------------------

# pagina assistenza
@app.route('/form_assistenza.html', methods=['GET', 'POST'])
def assistenza():
    """
    Mostra la pagina dell'assistenza
    """

    if request.method == 'POST':
        oggetto = request.form['oggetto']
        mess = request.form['messaggio']

        print('-- Ricevuta nuova richiesta assistenza --')
        print(f'Oggetto: {oggetto}')
        print(f'Messaggio: {mess}')

        return render_template("form_assistenza.html", inviato=True)

    return render_template("form_assistenza.html", inviato=False)

#----------------------------blocca cache---------------------------
@app.after_request
def add_header(response):
    """
    Blocca la cache del browser per le pagine html impedendo all'utente di tornare indietro su form già compilati
    """

    if 'text/html' in response.content_type:
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0' #indica al browser di non memorizzare la pagina nella cache
        response.headers['Pragma'] = 'no-cache' #indica al browser di non memorizzare la pagina nella cache (per compatibilità con HTTP/1.0)
        response.headers['Expires'] = '-1' #indica al browser che la pagina è già scaduta e non deve essere memorizzata nella cache
    return response

# -----------------------------------------------------------------------


if __name__=="__main__":
    app.run(host='0.0.0.0', port=5500, debug=True)
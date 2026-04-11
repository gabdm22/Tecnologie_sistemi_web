from flask import Flask, request, render_template, redirect, session
import sqlite3
import os

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
@app.route('/form_upload.html')
def vendi():
    return render_template("form_upload.html")


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

        return redirect("/vetrina.html")
    else:
        return "ERRORE! nessuna immagine ricevuta"




















if __name__=="__main__":
    app.run(debug=True)
import sqlite3

conn = sqlite3.connect('mova_db.db')
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

# 1. UTENTE
cursor.execute('''
    CREATE TABLE IF NOT EXISTS utente(
        id_utente INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        nome TEXT NOT NULL,
        cognome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

# 2. INDIRIZZO 
cursor.execute('''
    CREATE TABLE IF NOT EXISTS indirizzo(
        id_indirizzo INTEGER PRIMARY KEY AUTOINCREMENT,
        via TEXT NOT NULL,
        citta TEXT NOT NULL,
        cap TEXT NOT NULL,
        interno TEXT,
        id_utente INTEGER NOT NULL,
        FOREIGN KEY (id_utente) REFERENCES utente(id_utente)
    )
''')

# 3. OPERA
cursor.execute('''
    CREATE TABLE IF NOT EXISTS opera(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT NOT NULL,
        dimensioni TEXT,
        id_venditore INTEGER NOT NULL,
        prezzo REAL NOT NULL,
        disponibilita INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (id_venditore) REFERENCES utente(id_utente)
    )
''')

# 4. ORDINE 
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ordine(
        id_ordine INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        stato TEXT NOT NULL,
        totale REAL NOT NULL,
        id_utente INTEGER NOT NULL,
        id_indirizzo INTEGER NOT NULL,
        FOREIGN KEY (id_utente) REFERENCES utente(id_utente),
        FOREIGN KEY (id_indirizzo) REFERENCES indirizzo(id_indirizzo)
    )
''')

# 5. INCARELLO 
cursor.execute('''
    CREATE TABLE IF NOT EXISTS incarello(
        id_utente INTEGER NOT NULL,
        id_opera INTEGER NOT NULL,
        quantita INTEGER DEFAULT 1,
        PRIMARY KEY (id_utente, id_opera),
        FOREIGN KEY (id_utente) REFERENCES utente(id_utente),
        FOREIGN KEY (id_opera) REFERENCES opera(id)
    )
''')

# 6. ORDINE_OPERA
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ordine_opera(
        id_ordine INTEGER NOT NULL,
        id_opera INTEGER NOT NULL,
        prezzo_acquisto REAL NOT NULL,
        quantita INTEGER NOT NULL,
        PRIMARY KEY (id_ordine, id_opera),
        FOREIGN KEY (id_ordine) REFERENCES ordine(id_ordine),
        FOREIGN KEY (id_opera) REFERENCES opera(id)
    )
''')

# 7. METODO PAGAMENTO
cursor.execute('''
    CREATE TABLE IF NOT EXISTS metodo_pagamento(
        id_metodo INTEGER PRIMARY KEY AUTOINCREMENT,
        provider TEXT NOT NULL,
        scadenza TEXT NOT NULL,
        ultime_4_cifre TEXT NOT NULL,
        token_pagamento TEXT NOT NULL,
        id_utente INTEGER NOT NULL,
        FOREIGN KEY (id_utente) REFERENCES utente(id_utente)
    )
''')

conn.commit()
conn.close()
print("Database creato correttamente con vincoli di integrità.\n")
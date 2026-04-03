import sqlite3

conn = sqlite3.connect('mova_db.db')
cursor = conn.cursor()

#crea tabella UTENTE per registrazioni e login
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS utente(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cognome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    '''
)


#crea tabella OPERA per upload (vendita) e acquisto
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS opera(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT NOT NULL,
        dimensioni TEXT,
        venditore TEXT NOT NULL REFERENCES utente(id),
        prezzo REAL NOT NULL
    )
    '''
)


#crea tabella ACQUISTO che mettere in relazione utente e opera
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS acquisto(
        utente TEXT NOT NULL REFERENCES utente(id),
        opera TEXT NOT NULL REFERENCES opera(id),
        data_acquisto TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    '''
)


conn.commit()
conn.close()
print("database creato\n")
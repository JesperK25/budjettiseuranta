import sqlite3

def get_connection():

    conn = sqlite3.connect("budjetti.db")

    conn.row_factory = sqlite3.Row
    return conn

def luo_taulut():

    conn = get_connection()

    conn.execute("""
                 CREATE TABLE IF NOT EXISTS merkinta (
                     id         INTEGER PRIMARY KEY AUTOINCREMENT,
                     tyyppi     TEXT NOT NULL,         --'tulo' tai 'meno'
                     kategoria  TEXT NOT NULL,         -- esim. 'ruoka' , 'palkka'
                     summa      REAL NOT NULL,         -- desimaaliluku, esim. 45.50
                     kuvaus     TEXT,                  -- vapaaehtoinen selitys
                      paivamaara TEXT NOT NULL         -- tallennetaan tekstinä: '2026-05-27'
                 )
   """)
    conn.commit()
    conn.close()
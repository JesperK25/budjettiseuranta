from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)
database.luo_taulut()

@app.route("/")
def etusivu():
    conn = database.get_connection()

    merkinnat = conn.execute(
        "SELECT * FROM merkinta ORDER BY paivamaara DESC"
    ).fetchall()

    tulot = conn.execute(
        "SELECT SUM(summa) FROM merkinta WHERE tyyppi = 'tulo'"
    ).fetchone()[0] or 0

    menot = conn.execute(
        "SELECT SUM(summa) FROM merkinta WHERE tyyppi = 'meno'"
    ).fetchone()[0] or 0


    conn.close()

    saldo = tulot - menot

    return render_template("index.html",
                           merkinnat=merkinnat,
                           tulot=tulot,
                           menot=menot,
                           saldo=saldo)

@app.route("/lisaa", methods=["GET", "POST"])
def lisaa_merkinta():
    """
    methods=["GET", "POST"] tarkoittaa että tämä reitti hyväksyy molemmat HTTP-metodit:
    -GET: käyttäjä avaa sivun (näytetään lomake)
    -POST: käyttäjä lähetti lomakkeen (tallennetaan tietokantaan)
    """
    if request.method == "POST":

        tyyppi  = request.form["tyyppi"]
        kategoria  = request.form["kategoria"]
        summa  = float(request.form["summa"])
        kuvaus  = request.form["kuvaus"]
        paivamaara  = request.form["paivamaara"]

        conn = database.get_connection()
        conn.execute(
            """INSERT INTO merkinta (tyyppi, kategoria, summa, kuvaus, paivamaara)
            VALUES (?, ?, ?, ?, ?)""",
            (tyyppi, kategoria, summa, kuvaus, paivamaara)


        )
        conn.commit()
        conn.close()

        return redirect(url_for("etusivu"))
    
    return render_template("lisaa.html")

@app.route("/poista/<int:id>")
def poista_merkinta(id):
    conn = database.get_connection()
    conn.execute("DELETE FROM merkinta WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("etusivu"))


if __name__ == "__main__":
    app.run(debug=True)
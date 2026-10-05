import sqlite3
from flask import Flask, request

app = Flask(__name__)
FLAG = "CTF{sql_1njection_b4sics}"


def db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (username TEXT, password TEXT, secret TEXT)")
    conn.execute("INSERT INTO users VALUES ('guest','guest','rien ici')")
    conn.execute("INSERT INTO users VALUES ('admin','Zx9!not-guessable-7731','%s')" % FLAG)
    return conn


@app.route("/", methods=["GET", "POST"])
def index():
    msg = ""
    if request.method == "POST":
        u = request.form.get("username", "")
        p = request.form.get("password", "")
        q = "SELECT username, secret FROM users WHERE username='%s' AND password='%s'" % (u, p)
        try:
            row = db().execute(q).fetchone()
            msg = "Connecté en tant que %s. Secret : %s" % row if row else "Identifiants invalides"
        except Exception as e:
            msg = "Erreur : %s" % e
    return """<h1>Intranet ACME</h1>
    <form method=post><input name=username placeholder=login>
    <input name=password type=password placeholder=mot-de-passe><button>OK</button></form>
    <p>%s</p>""" % msg


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

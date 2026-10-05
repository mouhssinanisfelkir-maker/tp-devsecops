"""Application Flask VOLONTAIREMENT VULNERABLE - usage pédagogique uniquement.

Ne jamais déployer cette application sur un réseau exposé.
"""
import os
import sqlite3
import subprocess

from flask import Flask, request, render_template_string

app = Flask(__name__)

# Vulnérabilité : secret codé en dur (détectable par CodeQL / revue de code)
app.config["SECRET_KEY"] = "super-secret-key-123"
ADMIN_PASSWORD = "admin123"

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    c.execute("DELETE FROM users")
    c.execute("INSERT INTO users (username, password) VALUES ('admin', ?)", (ADMIN_PASSWORD,))
    c.execute("INSERT INTO users (username, password) VALUES ('alice', 'alice-pass')")
    c.execute("INSERT INTO users (username, password) VALUES ('bob', 'bob-pass')")
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return """
    <h1>TP DevSecOps - App vulnérable</h1>
    <ul>
      <li><a href="/login">Login (SQLi)</a></li>
      <li><a href="/upload">Upload</a></li>
      <li><a href="/ping">Ping (commande shell)</a></li>
      <li><a href="/hello?name=World">Hello (XSS)</a></li>
    </ul>
    """


# --- 1) Injection SQL : requête construite par concaténation -----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        conn = sqlite3.connect(DB_PATH)
        query = "SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (username, password)
        try:
            row = conn.execute(query).fetchone()
        except sqlite3.Error as exc:
            row = None
            message = "Erreur SQL : %s" % exc
        conn.close()
        if row:
            message = "Bienvenue %s !" % row[1]
    return render_template_string(
        """
        <h2>Login</h2>
        <form method="post">
          <input name="username" placeholder="username">
          <input name="password" type="password" placeholder="password">
          <button>Connexion</button>
        </form>
        <p>{{ message }}</p>
        """,
        message=message,
    )


# --- 2) Upload sans contrôle (extension, type, contenu) ---------------------
@app.route("/upload", methods=["GET", "POST"])
def upload():
    msg = ""
    if request.method == "POST":
        f = request.files.get("file")
        if f:
            # Vulnérabilité : nom de fichier utilisé tel quel (path traversal + pas de filtre)
            path = os.path.join(UPLOAD_DIR, f.filename)
            f.save(path)
            msg = "Fichier envoyé : /uploads/%s" % f.filename
    return """
    <h2>Upload</h2>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file"><button>Envoyer</button>
    </form>
    <p>%s</p>
    """ % msg


@app.route("/uploads/<path:name>")
def uploaded(name):
    # Vulnérabilité : exécute les fichiers .py déposés (simule une exécution côté serveur)
    path = os.path.join(UPLOAD_DIR, name)
    if name.endswith(".py"):
        out = subprocess.run(["python", path], capture_output=True, text=True)
        return "<pre>%s%s</pre>" % (out.stdout, out.stderr)
    with open(path, "rb") as fh:
        return fh.read()


# --- 3) Injection de commande shell -----------------------------------------
@app.route("/ping", methods=["GET", "POST"])
def ping():
    output = ""
    if request.method == "POST":
        host = request.form.get("host", "")
        # Vulnérabilité : shell=True avec entrée utilisateur non filtrée
        output = subprocess.getoutput("ping -c 1 " + host)
    return render_template_string(
        """
        <h2>Ping</h2>
        <form method="post"><input name="host" placeholder="127.0.0.1"><button>Ping</button></form>
        <pre>{{ output }}</pre>
        """,
        output=output,
    )


# --- 4) XSS réfléchi ---------------------------------------------------------
@app.route("/hello")
def hello():
    name = request.args.get("name", "")
    # Vulnérabilité : l'entrée est injectée dans le template sans échappement
    return render_template_string("<h2>Bonjour " + name + "</h2>")


if __name__ == "__main__":
    init_db()
    # Vulnérabilité : debug=True et écoute sur toutes les interfaces
    app.run(host="0.0.0.0", port=5000, debug=True)

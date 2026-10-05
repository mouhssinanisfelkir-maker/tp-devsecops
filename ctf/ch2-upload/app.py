import os
import subprocess
from flask import Flask, request

app = Flask(__name__)
UP = "/app/uploads"
os.makedirs(UP, exist_ok=True)
# Le flag est dans /app/flag.txt (à lire via le fichier uploadé)
with open("/app/flag.txt", "w") as f:
    f.write("CTF{unr3stricted_upl0ad_rce}\n")


@app.route("/", methods=["GET", "POST"])
def index():
    msg = ""
    if request.method == "POST":
        f = request.files.get("file")
        if f:
            f.save(os.path.join(UP, f.filename))
            msg = 'Envoyé : <a href="/files/%s">/files/%s</a>' % (f.filename, f.filename)
    return """<h1>Galerie photo</h1>
    <p>Envoyez vos images (.jpg, .png)... enfin, c'est ce que dit la page.</p>
    <form method=post enctype=multipart/form-data><input type=file name=file><button>Envoyer</button></form>
    <p>%s</p>""" % msg


@app.route("/files/<name>")
def files(name):
    p = os.path.join(UP, name)
    if name.endswith(".py"):  # simulation d'un serveur qui exécute les scripts déposés
        r = subprocess.run(["python", p], capture_output=True, text=True, timeout=5)
        return "<pre>%s%s</pre>" % (r.stdout, r.stderr)
    return open(p, "rb").read()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

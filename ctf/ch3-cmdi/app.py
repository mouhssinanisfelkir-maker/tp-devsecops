import subprocess
from flask import Flask, request

app = Flask(__name__)
# Le flag est dans /flag.txt, créé au build
BANNED = [";", "|", "&&"]  # filtre incomplet volontairement


@app.route("/", methods=["GET", "POST"])
def index():
    out = ""
    if request.method == "POST":
        host = request.form.get("host", "")
        if any(b in host for b in BANNED):
            out = "Caractères interdits !"
        else:
            out = subprocess.getoutput("nslookup " + host)
    return """<h1>Outil DNS</h1>
    <form method=post><input name=host placeholder=example.com><button>Résoudre</button></form>
    <pre>%s</pre>""" % out


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

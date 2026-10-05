# Guide pas à pas — TP DevSecOps (sécurité proactive / web)

Ce dépôt contient tout le nécessaire pour réaliser le TP : une application volontairement
vulnérable, les workflows GitHub Actions (démo, CodeQL, Trivy), Dependabot, un mini CTF
(3 challenges), une configuration CTFd, et un quiz. Ce guide donne les commandes exactes,
étape par étape, dans l'ordre du sujet.

⚠️ Tout ce qui est "vulnérable" ici est fait exprès, pour le TP. Ne déployez ces services
que sur votre machine ou un réseau isolé, jamais exposés sur Internet.

---

## 0. Prérequis

- Un compte GitHub personnel.
- Git, Docker et Docker Compose installés en local.
- (Optionnel) un compte Kahoot pour le quiz.

---

## 1. Créer le dépôt GitHub et pousser le code

1. Sur GitHub : **New repository** → nom par exemple `tp-devsecops` → ne cochez aucune
   case d'initialisation (pas de README auto, on a déjà tout) → **Create repository**.
2. En local, dans le dossier de ce projet :

   ```bash
   cd tp-devsecops
   git init
   git add .
   git commit -m "Initial commit: app vulnérable + pipeline DevSecOps"
   git branch -M main
   git remote add origin https://github.com/<votre-compte>/tp-devsecops.git
   git push -u origin main
   ```

3. Allez dans l'onglet **Actions** du dépôt : le workflow `GitHub Actions Demo`
   (`.github/workflows/github-actions-demo.yml`) doit s'être déclenché automatiquement
   sur le push. C'est la validation demandée par l'étape 1 du sujet (quickstart officiel :
   https://docs.github.com/en/actions/get-started/quickstart).

**Capture à faire pour le rapport** : onglet Actions montrant le run réussi.

---

## 2. CodeQL (SAST)

Le workflow est déjà prêt dans `.github/workflows/codeql.yml` (langage `python`,
requêtes `security-extended`, déclenché sur push/PR et toutes les semaines).

1. Poussez (ou re-poussez) sur `main` pour déclencher le scan :
   ```bash
   git commit --allow-empty -m "Trigger CodeQL"
   git push
   ```
2. Onglet **Security → Code scanning alerts** : au bout de quelques minutes, les
   vulnérabilités du fichier `app/app.py` doivent apparaître, par exemple :
   - `py/sql-injection` (route `/login`)
   - `py/command-line-injection` (route `/ping`)
   - `py/flask-debug` (debug activé)
   - `py/hardcoded-credentials` (mot de passe admin en dur)

**Capture à faire** : liste des alertes CodeQL, puis le détail d'une alerte (ex: SQLi)
montrant la ligne de code pointée.

---

## 3. Dependabot

Le fichier `.github/dependabot.yml` est déjà présent (pip pour `/app`, Docker, et
github-actions, fréquence hebdomadaire). Les dépendances dans `app/requirements.txt`
sont volontairement anciennes (Flask 1.1.2, Jinja2 2.11.2, Werkzeug 1.0.1, PyYAML 5.3.1,
requests 2.19.0, Pillow 8.1.0) pour générer des alertes.

1. Sur GitHub : **Settings → Code security** du dépôt → vérifiez que *Dependabot alerts*
   et *Dependabot security updates* sont activés (ils le sont par défaut dès que le
   fichier `dependabot.yml` est présent sur un dépôt public ; sinon activez-les
   manuellement).
2. Attendez quelques minutes, puis onglet **Security → Dependabot alerts** : vous devez
   voir apparaître des CVE sur les paquets ci-dessus.
3. Onglet **Pull requests** : Dependabot propose normalement une ou plusieurs PR de mise
   à jour automatique.

**Capture à faire** : liste des alertes Dependabot + une PR automatique générée.

---

## 4. Trivy (scan de l'image Docker)

Le `Dockerfile` à la racine part de `python:3.8-buster` (image ancienne, volontairement
non à jour) pour que Trivy trouve des CVE côté système d'exploitation. Le workflow
`.github/workflows/trivy.yml` :
- construit l'image,
- publie un rapport SARIF complet (HIGH+CRITICAL) dans l'onglet Sécurité,
- puis relance un scan qui **échoue le pipeline (`exit-code: 1`) s'il existe au moins
  une vulnérabilité CRITICAL**.

### 4.1 Tester en local (optionnel mais recommandé)

```bash
docker build -t tp-devsecops:local .
# Installer trivy localement si besoin : https://aquasecurity.github.io/trivy/latest/getting-started/installation/
trivy image --severity HIGH,CRITICAL tp-devsecops:local
```

### 4.2 Déclencher le workflow

```bash
git commit --allow-empty -m "Trigger Trivy scan"
git push
```

Onglet **Actions → Trivy - scan de l'image Docker** : le job doit échouer (rouge) à
cause de CVE CRITICAL sur l'image `python:3.8-buster` (ex : vulnérabilités OpenSSL,
glibc, etc. selon la base Debian Buster, obsolète).

**Capture à faire** : run du workflow en échec + extrait de la table Trivy listant les
CVE CRITICAL.

### 4.3 Rapport SARIF

Onglet **Security → Code scanning alerts** : les résultats Trivy apparaissent aussi ici
(catégorie `trivy`), avec le lien direct par CVE.

### 4.4 Corriger (à faire en seconde partie du TP, pour la section "remédiation")

Dans `Dockerfile`, remplacez :
```dockerfile
FROM python:3.8-buster
```
par :
```dockerfile
FROM python:3.12-slim
```
et mettez à jour `app/requirements.txt` avec des versions récentes (Flask>=3.0,
Jinja2>=3.1, Werkzeug>=3.0, PyYAML>=6.0, requests>=2.32, Pillow>=10.3), puis repoussez :
```bash
git add Dockerfile app/requirements.txt
git commit -m "Remediation: base image et dépendances à jour"
git push
```
Relancez le workflow et montrez dans le rapport la différence **avant / après**
(nombre de CVE CRITICAL/HIGH, pipeline qui passe au vert).

---

## 5. Exploitation des résultats (à mettre dans le rapport)

Pour chaque vulnérabilité trouvée par CodeQL, Dependabot et Trivy, documentez dans le
rapport (modèle fourni dans `docs/RAPPORT_TEMPLATE.md`) :
- l'outil qui l'a détectée,
- la gravité,
- une explication courte du risque,
- la correction apportée (ou à apporter) avec un extrait de code avant/après.

Le code de `app/app.py` contient volontairement 4 failles commentées dans le code
(`# Vulnérabilité : ...`) pour faciliter cette analyse :
1. Injection SQL (`/login`) — requête construite par concaténation.
2. Upload sans contrôle + exécution de fichiers `.py` déposés (`/upload`, `/uploads/<name>`).
3. Injection de commande shell (`/ping`) via `subprocess.getoutput`.
4. XSS réfléchi (`/hello?name=...`) — entrée injectée sans échappement dans le HTML.
Plus : secret codé en dur, et `debug=True` / écoute sur `0.0.0.0`.

---

## 6. Mini CTF (3 challenges)

Les 3 challenges demandés par le sujet sont dans `ctf/` :
- `ctf/ch1-sqli` — injection SQL simple
- `ctf/ch2-upload` — upload de fichier malveillant
- `ctf/ch3-cmdi` — exécution de commande shell via vulnérabilité

### 6.1 Lancer les challenges en local

```bash
cd ctf
docker compose up -d --build
```
- Challenge 1 : http://localhost:8081
- Challenge 2 : http://localhost:8082
- Challenge 3 : http://localhost:8083

Les énoncés, indices progressifs, solutions détaillées et flags (`CTF{...}`) ainsi que
les corrections de sécurité sont dans **`ctf/SOLUTIONS.md`**. C'est le document à fournir
aux "formés" (demandé par le sujet : "fournissez les instructions de résolution").

Pour arrêter : `docker compose down`.

---

## 7. Déploiement de CTFd et intégration des challenges

### 7.1 Lancer CTFd en local

```bash
cd ctfd
docker compose up -d
```
Ouvrez http://localhost:8000 → un assistant de configuration apparaît (nom du CTF,
compte administrateur, etc.). Suivez-le pour créer votre compte admin.

### 7.2 Créer les 3 challenges dans CTFd

Pour chacun des 3 challenges (`ch1-sqli`, `ch2-upload`, `ch3-cmdi`) :

1. **Admin Panel → Challenges → Create**.
2. Type : `standard`. Catégorie : `Web`. Nom : ex. "Injection SQL simple".
3. Description : collez l'énoncé correspondant depuis `ctf/SOLUTIONS.md` (sans la
   solution !), et indiquez l'URL d'accès (ex. `http://<ip-de-votre-machine>:8081`).
4. Valeur en points : 100 (ch1), 200 (ch2), 200 (ch3) — modifiable.
5. Flag : type `static`, collez le flag exact (ex. `CTF{sql_1njection_b4sics}`).
6. Onglet **Hints** : ajoutez les indices progressifs (coût en points optionnel).
7. **Create**.

Répétez pour les 2 autres challenges, puis **Admin Panel → Challenges** pour vérifier
que les 3 sont visibles et activés.

### 7.3 Ressources pédagogiques dans CTFd

Dans chaque challenge ou dans une page CTFd dédiée (**Admin Panel → Pages**), ajoutez
un lien vers des ressources sur le type de faille (ex : OWASP Injection, OWASP
Unrestricted File Upload, OWASP Command Injection) pour accompagner la résolution,
comme demandé par le sujet.

**Capture à faire** : page d'accueil CTFd avec les 3 challenges, et un exemple de
soumission de flag validée ("Correct!").

---

## 8. Quiz interactif (Kahoot)

Le contenu des 15 questions (QCM, bonne réponse marquée ✅) est dans `quiz/quiz.md`.

1. Allez sur https://kahoot.com → **Create** → **Kahoot**.
2. Donnez un titre ("Sécurité web & DevSecOps").
3. Ajoutez chaque question manuellement (type "Quiz", 4 réponses, 20 secondes), ou
   utilisez l'import Excel proposé par Kahoot (**Create → Import questions**) en
   collant le contenu de `quiz/quiz.md` dans leur modèle.
4. **Save**, puis **Play** (mode "Classic" ou "Team") pour obtenir un PIN de partie que
   vous pouvez tester seul ou avec votre binôme.

**Capture à faire** : l'écran du quiz créé dans Kahoot (liste des questions) et un
écran de partie en cours.

---

## 9. Récapitulatif des livrables à joindre au rapport Teams

- Captures GitHub Actions (demo, CodeQL, Trivy avant/après correction).
- Captures des alertes CodeQL et Dependabot.
- Extraits de code vulnérable + corrigé (avant/après) pour chaque faille.
- Lien (ou export) du dépôt GitHub.
- Captures CTFd (challenges + résolution).
- Captures du quiz Kahoot.
- Le rapport rédigé à partir de `docs/RAPPORT_TEMPLATE.md`.

Bon TP !

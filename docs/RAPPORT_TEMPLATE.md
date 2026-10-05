# Rapport TP — Pratiques proactives de sécurité web / DevSecOps

**Nom(s) / binôme :**
**Date :**
**Dépôt GitHub :** https://github.com/<votre-compte>/tp-devsecops

---

## 1. Introduction

Contexte du TP, objectifs (intégrer la sécurité tôt dans le cycle de développement,
"shift-left"), présentation rapide de l'application choisie (ici : une petite
application Flask volontairement vulnérable, avec SQLi, upload non contrôlé,
injection de commande, XSS, secret en dur et image Docker obsolète).

## 2. Mise en place de l'environnement GitHub

- Capture : création du dépôt.
- Capture : premier run du workflow de démonstration (`github-actions-demo.yml`)
  déclenché automatiquement sur push.
- Difficultés rencontrées (le cas échéant).

## 3. Intégration des outils de sécurité automatisée

### 3.1 CodeQL (SAST)
- Configuration utilisée (langage, requêtes `security-extended`).
- Captures des alertes trouvées dans l'onglet Sécurité.
- Tableau des vulnérabilités détectées :

| Règle CodeQL | Fichier / ligne | Gravité | Description | Correction apportée |
|---|---|---|---|---|
| py/sql-injection | app/app.py:/login | High | Requête SQL construite par concaténation | Requêtes paramétrées |
| py/command-line-injection | app/app.py:/ping | High | `subprocess.getoutput` avec entrée utilisateur | `subprocess.run([...], shell=False)` |
| py/flask-debug | app/app.py | Medium | `debug=True` en production | Désactivé / variable d'environnement |
| py/hardcoded-credentials | app/app.py | Medium | Mot de passe/secret en dur | Variables d'environnement / gestionnaire de secrets |

### 3.2 Dependabot
- Captures des alertes de dépendances (CVE, paquet, version corrigée).
- Captures d'une ou plusieurs pull requests automatiques.
- Tableau avant/après mise à jour :

| Paquet | Version initiale | CVE | Version corrigée |
|---|---|---|---|
| Flask | 1.1.2 | ... | >=3.0 |
| Jinja2 | 2.11.2 | ... | >=3.1 |
| Werkzeug | 1.0.1 | ... | >=3.0 |
| PyYAML | 5.3.1 | ... | >=6.0 |
| requests | 2.19.0 | ... | >=2.32 |
| Pillow | 8.1.0 | ... | >=10.3 |

### 3.3 Trivy (scan Docker)
- Image de base initiale : `python:3.8-buster`.
- Capture : run du pipeline en échec (`exit-code: 1`) sur détection de CVE CRITICAL.
- Extrait de la table de vulnérabilités (quelques lignes représentatives).
- Correction : passage à `python:3.12-slim`.
- Capture : run après correction, pipeline au vert, comparaison du nombre de CVE
  avant/après (graphique ou tableau).

### 3.4 Synthèse des résultats
- Analyse critique : quels outils ont été les plus utiles, les limites de chacun
  (faux positifs, bruit, délai de détection), complémentarité SAST / gestion de
  dépendances / scan de conteneurs.

## 4. Sensibilisation par la pratique

### 4.1 Quiz Kahoot
- Capture des questions / de la partie jouée.
- Retour d'expérience : ce que le quiz permet de faire passer comme messages clés.

### 4.2 Mini CTF (3 challenges)
Pour chaque challenge : énoncé, démarche de résolution, capture de la validation du
flag, et recommandation de correction.

| Challenge | Vulnérabilité | Flag | Correction recommandée |
|---|---|---|---|
| ch1-sqli | Injection SQL | CTF{sql_1njection_b4sics} | Requêtes paramétrées, hachage des mots de passe |
| ch2-upload | Upload de fichier malveillant | CTF{unr3stricted_upl0ad_rce} | Liste blanche d'extensions, vérification du type réel, pas d'exécution des fichiers uploadés |
| ch3-cmdi | Injection de commande shell | CTF{c0mmand_1njection_pwn3d} | Pas de shell, validation stricte de l'entrée |

### 4.3 Déploiement CTFd
- Captures : page d'accueil CTFd, configuration des 3 challenges, résolution réussie.
- Retour d'expérience sur l'outil (facilité de déploiement, personnalisation,
  limites).

## 5. Analyse critique et recommandations pour une culture DevSecOps

- Ce qu'apporte l'automatisation de la sécurité (détection précoce, réduction du
  coût de correction, traçabilité).
- Limites observées (faux positifs, bruit d'alertes, nécessité de trier/prioriser,
  dette de sécurité si les alertes ne sont pas traitées).
- Recommandations concrètes pour une équipe : politique de gating (bloquer sur
  CRITICAL), revue régulière des alertes Dependabot, formation continue des
  développeurs (quiz/CTF), intégration de la sécurité dès la conception
  ("security by design"), répartition des rôles dev/ops/sécurité.

## 6. Conclusion

Bilan global du TP, compétences acquises, ouverture (DAST, analyse d'IaC, SBOM,
gestion de secrets, etc.).

## Annexes

- Liste des captures d'écran.
- Liens vers le dépôt GitHub et éventuellement la plateforme CTFd si accessible.

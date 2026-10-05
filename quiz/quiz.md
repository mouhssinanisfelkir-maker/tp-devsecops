# Quiz Kahoot - Sécurité web et DevSecOps (15 questions)

Format Kahoot : 4 réponses max, une seule bonne (✅), 20 s par question.

1. Que signifie SAST ?
   - ✅ Static Application Security Testing
   - Server Application Security Test
   - Secure Authentication Session Token
   - System Access Security Tool

2. Quelle injection permet de lire une base de données via un formulaire mal protégé ?
   - XSS
   - CSRF
   - ✅ Injection SQL
   - Clickjacking

3. Quelle est la meilleure défense contre l'injection SQL ?
   - Filtrer l'apostrophe
   - ✅ Requêtes paramétrées
   - Cacher les messages d'erreur uniquement
   - Mettre le site en HTTPS

4. Que fait Dependabot ?
   - Analyse le code source avec des requêtes sémantiques
   - ✅ Détecte les dépendances vulnérables et propose des pull requests de mise à jour
   - Scanne les images Docker
   - Chiffre les secrets

5. CodeQL est un outil de type :
   - DAST
   - ✅ SAST
   - WAF
   - SIEM

6. Que scanne Trivy ?
   - Uniquement les mots de passe
   - ✅ Images de conteneurs, dépendances, fichiers IaC
   - Le trafic réseau en temps réel
   - Les logs Apache

7. Pourquoi faire échouer le pipeline sur une CVE CRITICAL ?
   - Pour ralentir les développeurs
   - ✅ Pour empêcher le déploiement d'une image à risque (shift-left)
   - Pour économiser des minutes GitHub Actions
   - Ce n'est pas utile

8. Que signifie « shift-left » ?
   - Déplacer la sécurité en production
   - ✅ Intégrer la sécurité le plus tôt possible dans le cycle de développement
   - Sécuriser uniquement la gauche de l'écran
   - Externaliser la sécurité

9. Quel est le risque d'un upload de fichier sans contrôle ?
   - Aucun
   - ✅ Dépôt d'un webshell et exécution de code à distance
   - Uniquement un manque d'espace disque
   - Une panne DNS

10. Quelle pratique protège contre l'injection de commande ?
    - Utiliser `shell=True` avec un filtre sur `;`
    - ✅ Éviter le shell et valider l'entrée par liste blanche
    - Mettre l'entrée en majuscules
    - Désactiver les logs

11. Que signifie CVE ?
    - Common Vulnerability Exploit
    - ✅ Common Vulnerabilities and Exposures
    - Certified Vulnerability Evaluation
    - Code Verification Engine

12. Un secret (mot de passe, clé API) codé en dur dans le dépôt est :
    - ✅ Une mauvaise pratique : il faut utiliser des variables d'environnement ou un gestionnaire de secrets
    - Acceptable si le dépôt est privé pour toujours
    - Obligatoire pour GitHub Actions
    - Sans risque

13. Que désigne un faux positif dans un scanner ?
    - Une vulnérabilité réelle non détectée
    - ✅ Une alerte qui ne correspond pas à une vraie vulnérabilité
    - Une mise à jour automatique
    - Une faille 0-day

14. Quelle faille consiste à injecter du script dans une page vue par d'autres utilisateurs ?
    - SQLi
    - ✅ XSS
    - SSRF
    - XXE

15. Quel est l'objectif principal du DevSecOps ?
    - Remplacer l'équipe sécurité
    - ✅ Automatiser et partager la responsabilité de la sécurité tout au long du cycle de vie
    - Déployer plus lentement
    - Supprimer les tests

## Import dans Kahoot
Créer un compte sur https://kahoot.com > Create > Kahoot > ajouter les questions manuellement (ou importer via le modèle Excel proposé par Kahoot), puis Play pour obtenir le code de partie. Ajouter une capture d'écran du quiz en annexe du rapport.

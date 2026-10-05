# TP DevSecOps — Sécurité web proactive

Projet prêt à l'emploi pour le TP "pratiques proactives de sécurité web" :

- `app/` + `Dockerfile` : petite application Flask **volontairement vulnérable**
  (injection SQL, upload non contrôlé, injection de commande, XSS, secret en dur)
  avec une image de base et des dépendances volontairement obsolètes.
- `.github/workflows/` : workflow de démonstration, CodeQL (SAST), Trivy (scan de
  l'image Docker, échoue sur CRITICAL).
- `.github/dependabot.yml` : Dependabot pour pip, Docker et GitHub Actions.
- `ctf/` : mini CTF avec 3 challenges (SQLi, upload malveillant, injection de
  commande) + `ctf/SOLUTIONS.md` (énoncés, indices, solutions, corrections).
- `ctfd/` : `docker-compose.yml` pour déployer CTFd en local.
- `quiz/quiz.md` : 15 questions de quiz (à importer dans Kahoot).
- `docs/RAPPORT_TEMPLATE.md` : modèle de rapport à compléter.

➡️ **Suivez `GUIDE.md`** pour toutes les étapes, dans l'ordre, avec les commandes
exactes et ce qu'il faut capturer pour le rapport.

⚠️ Usage pédagogique uniquement, en environnement isolé. Ne déployez jamais ces
services sur un réseau exposé ou en production.

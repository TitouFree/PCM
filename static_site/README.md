# Paris Carrelages et Matériaux — Site statique (GitHub Pages)

Site vitrine statique et autonome du négoce **Paris Carrelages et Matériaux** — Alfortville (94).
Aucun backend, aucune dépendance de build : du HTML, du CSS et du JavaScript purs, prêts à être servis par GitHub Pages.

## Contenu du dépôt

```
index.html              Accueil (hero, téléchargements, 11 familles, showroom)
entreprise.html         L'entreprise (présentation, services, showroom)
parcours.html           Les 11 familles de produits dans l'ordre du chantier
catalogue.html          Visionneuse PDF (plaquettes + catalogue + magazine) et téléchargements
fabricants.html         Marques et fabricants présents au comptoir
contact.html            Coordonnées, horaires, livraison, carte, demande de devis
404.html                Page d'erreur (redirection vers l'accueil du site)
css/style.css           Feuille de style unique
js/main.js              Menu mobile, animations, modale devis (mailto), visionneuse PDF
assets/                 Logo, visuels, polices locales (assets/fonts/)
documents/              Les PDF téléchargeables (voir ci-dessous)
favicon.svg             Favicon (marque « A » tour)
```

### Documents PDF (documents/)

- `PCM_Plaquette_Courte.pdf` + `PCM_Plaquette_Courte_Email.pdf` — plaquette courte (8 pages, nouvelle composition)
- `PCM_Plaquette_Complete.pdf` + `PCM_Plaquette_Complete_Email.pdf` — plaquette complète (56 pages, catalogue réorganisé sous les 11 familles)
- `Catalogue_General_PCM.pdf` — catalogue général d'origine (37 pages)
- `Ebauche_Magazine_PCM.pdf` — ébauche « Le Magazine » d'origine (4 pages)

## Mise en ligne sur GitHub Pages

1. Créer un dépôt sur GitHub (par ex. `pcm-site`).
2. Pousser **tout le contenu de ce dossier à la racine** de la branche `main`
   (`index.html` doit se trouver à la racine du dépôt, pas dans un sous-dossier) :
   ```bash
   git init
   git add .
   git commit -m "Site PCM — version statique"
   git branch -M main
   git remote add origin https://github.com/<moncompte>/<nom-du-depot>.git
   git push -u origin main
   ```
3. Sur GitHub : **Settings → Pages → Build and deployment → Deploy from a branch → Branch: `main` → Folder: `/ (root)` → Save**.
4. Après 1 à 2 minutes, le site est disponible sur :
   `https://<moncompte>.github.io/<nom-du-depot>/`

Tous les liens du site sont **relatifs** : le site fonctionne tel quel depuis un
sous-dossier de type `github.io/<nom-du-depot>/`, sans aucune modification.

## Notes techniques

- **Formulaire de devis** : sans serveur, le formulaire ouvre le logiciel e-mail du
  visiteur avec un message pré-rempli adressé à `snpariscm@gmail.com` (mailto).
- **Visionneuse PDF** : lecteur PDF natif du navigateur (iframe + `#page=` / `#zoom=`).
  Sur mobile, le bouton « Ouvrir le PDF » donne une lecture plein écran.
- **Taille du dépôt** : ~115 Mo au total, chaque fichier fait moins de 100 Mo
  (limite GitHub). Le site reste léger à charger : seules les pages HTML/CSS/JS et
  images sont téléchargées à la visite ; les PDF ne partent qu'au clic.
- **Carte** : OpenStreetMap en iframe (aucune clé requise) + lien itinéraire Google Maps.

## Test local avant de pousser

```bash
# depuis ce dossier
python3 -m http.server 8080
# puis ouvrir http://localhost:8080/
# pour simuler le sous-dossier GitHub Pages :
mkdir -p /tmp/ghp && ln -sfn "$PWD" /tmp/ghp/nom-du-depot
cd /tmp/ghp && python3 -m http.server 8081
# puis ouvrir http://localhost:8081/nom-du-depot/
```

## Coordonnées affichées sur le site

Paris Carrelages et Matériaux — 110 rue Édouard Vaillant, 94140 Alfortville
01 43 68 83 80 · snpariscm@gmail.com · pariscarrelages.fr · Instagram @pariscarrelages

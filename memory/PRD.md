# PRD — Paris Carrelages et Matériaux : plaquettes PDF + site catalogue

## Problème initial (verbatim, résumé structuré)
Créer DEUX plaquettes commerciales PDF (livrable principal) + un site catalogue (livrable complémentaire) pour Paris Carrelages et Matériaux, négoce à Alfortville (94), slogan « Des fondations aux finitions ». Sources officielles : « Ebauche 4 - Le Magazine.pdf » (identité) et « Catalogue general PCM.pdf » (37 pages, références). Ne jamais convertir les PDF en JPEG, ne supprimer aucune page/référence, ne rien inventer (références, marques, dimensions). Exports : plaquette courte HQ + e-mail, plaquette complète HQ + e-mail, site responsive avec boutons de téléchargement, formulaire de devis.

## Décisions confirmées par le client
- « Ebauche 4 - Le Magazine.pdf » = source d'identité graphique (le brief mentionnait Ebauche-2, non fourni).
- Formulaire devis : envoi e-mail à snpariscm@gmail.com via Resend géré Emergent (pas de clé à fournir).
- Catalogue : visionneuse PDF intégrée, page par page + zoom + téléchargement.
- Recherche de références : UNIQUEMENT si extraction fiable → catalogue 100 % image (aucun texte extractible), recherche DONC DÉSACTIVÉE (note explicative affichée sur la page Catalogue).

## Identité extraite des PDF sources
- Navy #0D3A5C (couverture catalogue), terracotta #A8623E (accents magazine), sable #F6F4ED, encre #1F2226.
- Typographies : Playfair Display (titres) / Source Sans 3 (corps) / JetBrains Mono (eyebrows), instanciées en TTF statiques (les variable fonts Google cassaient ReportLab).
- Logo original extrait de la couverture du magazine (version navy/blanc + version blanche recolorée pour fonds sombres).
- Photos originales extraites des PDF (bâtons rompus, échafaudage, isolation, peinture, marbre, faïence, carreaux ciment, ouvrier, plan d'accès, maison en chantier).
- 13 marques identifiées sur les bandeaux d'origine : Cifre Cerámica, Recer, Navarti, Weber, Mapei, PRB, Placo, Isover, Siniat, Rockwool, Unikalo, Makita (+ un logo triangle orange non identifié → non nommé).

## Architecture
- /app/scripts/build_pdfs.py : génère les 2 plaquettes (ReportLab) + fusionne les 37 pages d'origine du catalogue via pypdf (pages PDF natives, jamais converties) + variantes e-mail (photos JPEG compressées + pymupdf rewrite_images).
- Livrables servis statiquement : /app/frontend/public/documents/ (6 PDF).
- Assets : /app/frontend/public/assets/ (logo, photos, bandeaux marques), polices : /public/fonts + /src/fonts (bundlées).
- Backend FastAPI : POST /api/devis (validation, Mongo devis_requests, e-mail via proxy integrations.emergentagent.com avec garde-fous G1-G5, reply-to = demandeur), GET /api/health.
- Frontend React : 6 pages, framer-motion (hero cinétique masked lines, reveals), lenis (smooth scroll), react-pdf (visionneuse), sonner (toasts).

## Implémenté (24/09/2026)
- Plaquette courte 8 p. A4 portrait : couverture, présentation (textes d'origine), services (6), familles 01-11 (descriptions d'origine), fabricants + coordonnées + horaires + CTA « PASSEZ AU COMPTOIR ». HQ 13 Mo + e-mail 0,8 Mo.
- Plaquette complète 56 p. : couverture, présentation, services, sommaire paginé, parcours du chantier, 11 pages familles, fabricants, puis les 37 pages du catalogue général reprises à l'identique, contact final. HQ 51 Mo + e-mail 20 Mo.
- Site : Accueil (hero parallax + reveal, marquee, stats, bento téléchargements HQ/e-mail, 11 familles, showroom), L'Entreprise, Parcours du chantier (11 étapes alternées), Catalogue (visionneuse 4 documents : courte/complète/catalogue/magazine, page par page, zoom 50-250 %, téléchargement, note recherche désactivée), Fabricants (bandeaux d'origine + 12 marques nommées), Contact (adresse, tél, e-mail, Instagram, horaires, zones livraison, plan, formulaire devis).
- Formulaire devis : modal global + carte contact, envoi e-mail réel au comptoir (testé, email_id retourné), stockage Mongo.

## Vérifié
- curl /api/health OK ; POST /api/devis OK (e-mail parti à snpariscm@gmail.com).
- Screenshots 375/768/1366 px : hero, downloads, familles, visionneuse (page 2/37, zoom 120 %, changement de document), fabricants, contact, formulaire rempli + toast succès.
- 6 URLs /documents/*.pdf répondent 206.
- Pages plaquettes rendues et inspectées visuellement (couvertures, présentation, services, familles, sommaire, parcours, fabricants, page catalogue fusionnée, contact).

## Backlog priorisé
- P0 : rien de bloquant.
- P1 : logo triangle orange non identifié à confirmer par le client puis nommer sur la page Fabricants ; numérotation des pages catalogue par famille dans la plaquette complète (nécessite lecture manuelle du catalogue image).
- P2 : recherche de références si une version texte du catalogue est fournie un jour ; version EN ; espace pro avec tarifs.

## Prochaines tâches
1. Recueillir le nom du fabricant au logo triangle orange.
2. Re-générer les plaquettes si nouveaux visuels/catalogue fournis (python3 scripts/build_pdfs.py).
3. Déploiement production quand le client valide l'aperçu.

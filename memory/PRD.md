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
- Plaquette complète 56 p. : couverture, présentation, services, sommaire paginé AVEC index précis du catalogue (23 sections, numéros de pages plaquette), parcours du chantier, 11 pages familles avec renvoi « Les références au catalogue général » (sections + pages), fabricants, puis les 37 pages du catalogue général reprises à l'identique, contact final. HQ 51 Mo + e-mail 20 Mo.
- Index du catalogue lu page par page sur les en-têtes d'origine (catalogue 100 % image) : couverture 1, index 2, blocs béton 3-4, ciments 5-6, ferraillage 7, bois/charpente 8-9, toiture 10, isolation 11-12, plâtre 13-14, enduits/ragréages 15-16, carrelage 17, colles/joints 18-20, outillage carreleur 21, assainissement 22, peinture 23-25, outillage & machines 26-28, visserie 29-30, installation chantier/EPI 31-32, menuiserie 33, livraison 34, nous trouver 35, notes 36, 4e couv. 37. Page plaquette = page catalogue + 18.
- Site : Accueil (hero parallax + reveal, marquee, stats, bento téléchargements HQ/e-mail, 11 familles, showroom), L'Entreprise, Parcours du chantier (11 étapes + sections catalogue par famille + liens profonds /catalogue?doc=catalogue&page=N), Catalogue (visionneuse 4 documents, page par page, zoom, accès direct par section, note recherche désactivée), Fabricants (bandeaux d'origine + 12 marques nommées ; le logo triangle orange reste visuel dans le bandeau, SANS nom, à la demande du client), Contact (carte OpenStreetMap interactive avec marqueur au 110 rue Édouard Vaillant + bouton itinéraire Google Maps, horaires, zones livraison, formulaire devis).
- Formulaire devis : modal global + carte contact, envoi e-mail réel au comptoir (testé, email_id retourné), stockage Mongo.

## Itération 3 (24/09/2026) — VRAIES plaquettes fusionnées (demande corrective du client)
Le client a exigé de vrais documents fusionnés, pas la juxtaposition ébauche+catalogue. Reconstruction complète (/app/scripts/build_pdfs.py) :
- PCM_Plaquette_Courte.pdf (8 p. A4 portrait, 13 Mo) + _Email (0,5 Mo) : nouvelle composition ; chaque famille porte les noms RÉELS de ses sections du catalogue (« Au catalogue : … »).
- PCM_Plaquette_Complete.pdf (56 p., 55,8 Mo) + _Email (3,8 Mo) : catalogue RÉORGANISÉ sous les 11 familles dans l'ordre du chantier ; chaque page du catalogue d'origine (37/37) est rendue en 150 dpi et recadrée SANS MODIFICATION dans la maquette uniforme (bandeau famille navy, marges sable, pagination continue, pied PCM) en A4 paysage pour préserver la lisibilité (~87 % de l'échelle d'origine) ; sommaire avec plages de pages par famille ; 6 pages hors familles conservées en annexes (couverture 1, index 2, livraison 34, nous trouver 35, notes 36, 4e couv. 37).
- Pagination complète : front p1-5, familles 01→11 : 06-08 / 09-13 / 14-20 / 21-22 / 23-25 / 26-28 / 29-30 / 31-36 / 37-40 / 41-44 / 45-47, annexes 48-54, fabricants 55, contact 56.
- Anciens fichiers Paris_Carrelages_Materiaux_Plaquette_* SUPPRIMÉS. Site : section téléchargement = 2 plaquettes fusionnées (HQ + e-mail + feuilletage) + bloc « Documents sources » séparé (catalogue + magazine d'origine) ; visionneuse : 4 onglets (2 fusionnées + 2 sources) ; footer mis à jour.
- Vérifié : rendus visuels des pages clés (couverture, sommaire, dividers, pages références recadrées lisibles, annexes, fabricants, contact) ; 6 URL /documents répondent 206 ; visionneuse charge la plaquette complète fusionnée (56 p.) et navigue jusqu'à p. 15/56.
## Itération 4 (24/09/2026) — renommage
À la demande du client, le mot « fusionnée » est retiré : fichiers renommés PCM_Plaquette_Courte.pdf / PCM_Plaquette_Complete.pdf (+_Email), libellés site et visionneuse mis à jour (« Plaquette courte », « Plaquette complète »). build_pdfs.py régénère désormais ces noms. Vérifié : 4 URL 206, plus aucune occurrence de « fusionnée » dans le frontend.

## Itération 2 (24/09/2026) — demandes client (historique)
1. Logo triangle orange : conservé comme simple visuel dans les bandeaux fabricants, aucun nom attribué.
2. Catalogue numéroté par famille : sommaire de la plaquette complète enrichi d'un index précis (23 sections + pages) ; chaque page famille liste ses sections catalogue avec numéros de pages ; site Parcours + Catalogue mis à jour en cohérence (liens profonds testés : page 11/37 via URL, saut à 23/37 via l'index). Aucune référence modifiée, aucune page supprimée.
3. Plan d'accès image remplacé par carte OpenStreetMap interactive cliquable (marqueur géocodé 48.8086324, 2.4188248) + bouton itinéraire ; adresse écrite conservée dans les deux plaquettes PDF.
4. Pas de mise en ligne pour le moment (non déployé).

## Vérifié
- curl /api/health OK ; POST /api/devis OK (e-mail parti à snpariscm@gmail.com).
- Screenshots 375/768/1366 px : hero, downloads, familles, visionneuse (page 2/37, zoom 120 %, changement de document), fabricants, contact, formulaire rempli + toast succès.
- 6 URLs /documents/*.pdf répondent 206.
- Pages plaquettes rendues et inspectées visuellement (couvertures, présentation, services, familles, sommaire, parcours, fabricants, page catalogue fusionnée, contact).

## Backlog priorisé
- P0 : rien de bloquant.
- P1 : déploiement production quand le client le demandera (explicitement reporté par le client le 24/09/2026).
- P2 : recherche de références si une version texte du catalogue est fournie un jour ; version EN ; espace pro avec tarifs.

## Prochaines tâches
1. Attendre la validation client de l'aperçu avant toute mise en ligne.
2. Re-générer les plaquettes si nouveaux visuels/catalogue fournis (python3 scripts/build_pdfs.py).
3. Si le client confirme un jour le nom du logo triangle orange, l'ajouter à la liste Fabricants.

export const COMPANY = {
  name: "Paris Carrelages et Matériaux",
  baseline: "Des fondations aux finitions",
  hook: "Votre partenaire de proximité pour tous vos projets de construction et de rénovation",
  founded: 2011,
  address1: "110 rue Édouard Vaillant",
  address2: "94140 Alfortville",
  phone: "01 43 68 83 80",
  phoneHref: "tel:+33143688380",
  email: "snpariscm@gmail.com",
  website: "pariscarrelages.fr",
  instagram: "@pariscarrelages",
  instagramHref: "https://www.instagram.com/pariscarrelages",
};

export const HOURS = [
  { day: "Lundi – Jeudi", time: "6 h 30 – 18 h (pause 12 h – 13 h)" },
  { day: "Vendredi", time: "6 h 30 – 17 h (pause 12 h – 13 h)" },
  { day: "Samedi", time: "8 h – 12 h" },
  { day: "Dimanche", time: "Fermé" },
];

export const DELIVERY = {
  zones: ["Val-de-Marne", "Paris", "Seine-Saint-Denis", "Hauts-de-Seine", "Essonne"],
  note: "Partout en Île-de-France sur demande.",
  fleet: "Camion 27 t avec grue, plateau 3,5 t.",
};

export const SERVICES = [
  { title: "Conseil technique", text: "Le bon produit et la bonne méthode de pose, expliqués au comptoir." },
  { title: "Stock sur place", text: "Vous repartez avec la marchandise. Devis rapide pour le reste." },
  { title: "Showroom", text: "Le carrelage se choisit en le touchant : six aspects à comparer en vrai à Alfortville — pierre, bois, marbre, béton, carreau ciment, décor." },
  { title: "Livraison sous 24 h", text: "Toute l'Île-de-France : Val-de-Marne, Paris, Seine-Saint-Denis, Hauts-de-Seine, Essonne, et partout ailleurs sur demande." },
  { title: "Camion-grue 27 t", text: "Un camion 27 tonnes équipé d'une grue pour décharger directement sur votre chantier." },
  { title: "Plateau 3,5 t", text: "Un plateau 3,5 tonnes complète la flotte pour les livraisons urbaines." },
];

export const FAMILIES = [
  { num: "01", title: "Installation & protection de chantier", desc: "Protections de chantier, équipements de protection individuelle (EPI).", img: "/assets/ouvrier_chantier.png",
    catalogue: [{ section: "Installation de chantier, protection & EPI", pages: "p. 49 – 50", catPage: 31 }] },
  { num: "02", title: "Machines & outillage", desc: "Électroportatif, outils de pose, découpe, mélange.", img: null,
    catalogue: [{ section: "Outillage du carreleur", pages: "p. 39", catPage: 21 }, { section: "Outillage & machines", pages: "p. 44 – 46", catPage: 26 }] },
  { num: "03", title: "Gros œuvre & maçonnerie", desc: "Parpaing, ciment, mortier, sable, béton, cales à béton.", img: "/assets/chantier_echafaudage.png",
    catalogue: [{ section: "Blocs béton, briques & terre cuite", pages: "p. 21 – 22", catPage: 3 }, { section: "Ciments, chaux, plâtres, bétons & mortiers", pages: "p. 23 – 24", catPage: 5 }, { section: "Ferraillage & acier", pages: "p. 25", catPage: 7 }, { section: "Assainissement, PVC & géotextiles", pages: "p. 40", catPage: 22 }] },
  { num: "04", title: "Toiture & couverture", desc: "Tuiles et accessoires de couverture.", img: "/assets/maison_chantier.png",
    catalogue: [{ section: "Toiture, couverture & zinguerie", pages: "p. 28", catPage: 10 }] },
  { num: "05", title: "Isolation", desc: "Laines minérales, isolation thermique et acoustique.", img: "/assets/isolation_mur.png",
    catalogue: [{ section: "Isolation", pages: "p. 29 – 30", catPage: 11 }] },
  { num: "06", title: "Plâtrerie & cloisons", desc: "Plaques de plâtre et systèmes de cloisons.", img: null,
    catalogue: [{ section: "Plaques de plâtre, ossatures & carreaux de plâtre", pages: "p. 31 – 32", catPage: 13 }] },
  { num: "07", title: "Carrelage & faïence", desc: "Grès cérame et faïence : pierre, bois, marbre, béton, carreau ciment, décor.", img: "/assets/carrelage_marbre.png",
    catalogue: [{ section: "Carrelage & faïence", pages: "p. 35", catPage: 17 }] },
  { num: "08", title: "Colles, joints & ragréage", desc: "Colles, joints, ragréage, primaires, nattes, étanchéité.", img: "/assets/faience_niche.png",
    catalogue: [{ section: "Enduits, ragréages & mortiers techniques", pages: "p. 33 – 34", catPage: 15 }, { section: "Colles, joints & accessoires de pose", pages: "p. 36 – 38", catPage: 18 }] },
  { num: "09", title: "Peinture", desc: "Peintures et produits de finition.", img: "/assets/peinture_rouleaux.png",
    catalogue: [{ section: "Peinture & finition", pages: "p. 41 – 43", catPage: 23 }] },
  { num: "10", title: "Menuiserie", desc: "Fenêtres de toit et menuiseries.", img: null,
    catalogue: [{ section: "Bois de coffrage, charpente & panneaux", pages: "p. 26 – 27", catPage: 8 }, { section: "Menuiserie", pages: "p. 51", catPage: 33 }] },
  { num: "11", title: "Quincaillerie & accessoires de pose", desc: "Profilés, croisillons, nivellement, petit colisage en libre-service.", img: "/assets/carreaux_ciment.png",
    catalogue: [{ section: "Visserie, fixation & chimie du bâtiment", pages: "p. 47 – 48", catPage: 29 }, { section: "Colles, joints & accessoires de pose", pages: "p. 36 – 38", catPage: 18 }] },
];

export const CATALOGUE_SECTIONS = [
  { name: "Blocs béton, briques & terre cuite", page: 3 },
  { name: "Ciments, chaux, plâtres, bétons & mortiers", page: 5 },
  { name: "Ferraillage & acier", page: 7 },
  { name: "Bois de coffrage, charpente & panneaux", page: 8 },
  { name: "Toiture, couverture & zinguerie", page: 10 },
  { name: "Isolation", page: 11 },
  { name: "Plaques de plâtre, ossatures & carreaux de plâtre", page: 13 },
  { name: "Enduits, ragréages & mortiers techniques", page: 15 },
  { name: "Carrelage & faïence", page: 17 },
  { name: "Colles, joints & accessoires de pose", page: 18 },
  { name: "Outillage du carreleur", page: 21 },
  { name: "Assainissement, PVC & géotextiles", page: 22 },
  { name: "Peinture & finition", page: 23 },
  { name: "Outillage & machines", page: 26 },
  { name: "Visserie, fixation & chimie du bâtiment", page: 29 },
  { name: "Installation de chantier, protection & EPI", page: 31 },
  { name: "Menuiserie", page: 33 },
  { name: "Livraison & services", page: 34 },
];

export const DOWNLOADS = [
  {
    id: "courte",
    title: "Plaquette courte",
    subtitle: "Nouvelle composition · 8 pages A4",
    detail: "Présentation du négoce, services, showroom et les 11 familles avec leurs sections du catalogue. Pour la prospection, l'impression et l'e-mail.",
    href: "/documents/PCM_Plaquette_Courte.pdf",
    emailHref: "/documents/PCM_Plaquette_Courte_Email.pdf",
    size: "13 Mo",
    emailSize: "0,5 Mo",
  },
  {
    id: "complete",
    title: "Plaquette complète",
    subtitle: "Nouvelle composition · 56 pages",
    detail: "Présentation + catalogue général réorganisé sous les 11 familles : toutes les références, conditionnements et marques, recadrés dans la maquette PCM.",
    href: "/documents/PCM_Plaquette_Complete.pdf",
    emailHref: "/documents/PCM_Plaquette_Complete_Email.pdf",
    size: "56 Mo",
    emailSize: "3,8 Mo",
  },
];

export const SOURCES = [
  {
    id: "catalogue",
    title: "Catalogue général (source)",
    subtitle: "Document d'origine · 37 pages",
    href: "/documents/Catalogue_General_PCM.pdf",
    size: "31,5 Mo",
  },
  {
    id: "magazine",
    title: "Le Magazine (source)",
    subtitle: "Ébauche d'origine · 4 pages",
    href: "/documents/Ebauche_Magazine_PCM.pdf",
    size: "8,1 Mo",
  },
];

export const BRANDS = [
  "Cifre Cerámica", "Recer", "Navarti Cerámica", "Weber (Saint-Gobain)", "Mapei", "PRB",
  "Placo (Saint-Gobain)", "Isover (Saint-Gobain)", "Siniat", "Rockwool", "Unikalo", "Makita",
];

export const MARQUEE_ITEMS = [
  "Des fondations aux finitions",
  "Négoce indépendant depuis 2011",
  "Comptoir ouvert dès 6 h 30",
  "Stock sur place",
  "Livraison 24 h Île-de-France",
  "Camion-grue 27 t",
  "Showroom carrelage à Alfortville",
  "Pros & particuliers",
];

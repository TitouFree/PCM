#!/usr/bin/env python3
"""Génère les deux plaquettes PDF de Paris Carrelages et Matériaux.
Sources officielles : Ebauche 4 - Le Magazine.pdf + Catalogue general PCM.pdf.
Aucune référence, marque ou caractéristique inventée : les pages du catalogue
général sont fusionnées telles quelles (pages PDF d'origine, non converties).
"""
import io
import os

import pymupdf
from PIL import Image
from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

SRC = "/app/assets_src"
FINAL = f"{SRC}/final"
FONTS = f"{SRC}/fonts"
OUT = "/app/frontend/public/documents"
os.makedirs(OUT, exist_ok=True)

W, H = 595.27, 841.89  # A4 portrait

NAVY = HexColor("#0D3A5C")
TERRA = HexColor("#A8623E")
SAND = HexColor("#F6F4ED")
INK = HexColor("#1F2226")
SLATE = HexColor("#5A5F66")
STONE = HexColor("#8E949D")
LINE = HexColor("#DDD8D0")
WHITE = HexColor("#FFFFFF")

for name, fn in [
    ("Playfair", "PlayfairDisplay-400.ttf"), ("Playfair-It", "PlayfairDisplay-400-Italic.ttf"),
    ("Playfair-Md", "PlayfairDisplay-500.ttf"), ("Playfair-MdIt", "PlayfairDisplay-500-Italic.ttf"),
    ("Playfair-SB", "PlayfairDisplay-600.ttf"), ("Playfair-Bd", "PlayfairDisplay-700.ttf"),
    ("Sans", "SourceSans3-400.ttf"), ("Sans-SB", "SourceSans3-600.ttf"), ("Sans-Bd", "SourceSans3-700.ttf"),
    ("Mono", "JetBrainsMono-400.ttf"), ("Mono-Bd", "JetBrainsMono-700.ttf"),
]:
    pdfmetrics.registerFont(TTFont(name, f"{FONTS}/{fn}"))

FAMILIES = [
    ("01", "Installation & protection de chantier",
     "Protections de chantier, équipements de protection individuelle (EPI).", "ouvrier_chantier"),
    ("02", "Machines & outillage",
     "Électroportatif, outils de pose, découpe, mélange.", None),
    ("03", "Gros œuvre & maçonnerie",
     "Parpaing, ciment, mortier, sable, béton, cales à béton.", "chantier_echafaudage"),
    ("04", "Toiture & couverture",
     "Tuiles et accessoires de couverture.", "maison_chantier"),
    ("05", "Isolation",
     "Laines minérales, isolation thermique et acoustique.", "isolation_mur"),
    ("06", "Plâtrerie & cloisons",
     "Plaques de plâtre et systèmes de cloisons.", None),
    ("07", "Carrelage & faïence",
     "Grès cérame et faïence : pierre, bois, marbre, béton, carreau ciment, décor.", "carrelage_marbre"),
    ("08", "Colles, joints & ragréage",
     "Colles, joints, ragréage, primaires, nattes, étanchéité.", None),
    ("09", "Peinture",
     "Peintures et produits de finition.", "peinture_rouleaux"),
    ("10", "Menuiserie",
     "Fenêtres de toit et menuiseries.", "faience_niche"),
    ("11", "Quincaillerie & accessoires de pose",
     "Profilés, croisillons, nivellement, petit colisage en libre-service.", "carreaux_ciment"),
]

# Index réel du catalogue général (lu page par page sur les en-têtes d'origine).
# page plaquette = page catalogue + 18 (18 pages éditoriales avant le catalogue).
CATALOG_OFFSET = 18
CATALOG_SECTIONS = [
    ("Couverture", 1, 1),
    ("Index", 2, 2),
    ("Blocs béton, briques & terre cuite", 3, 4),
    ("Ciments, chaux, plâtres, bétons & mortiers", 5, 6),
    ("Ferraillage & acier", 7, 7),
    ("Bois de coffrage, charpente & panneaux", 8, 9),
    ("Toiture, couverture & zinguerie", 10, 10),
    ("Isolation", 11, 12),
    ("Plaques de plâtre, ossatures & carreaux de plâtre", 13, 14),
    ("Enduits, ragréages & mortiers techniques", 15, 16),
    ("Carrelage & faïence", 17, 17),
    ("Colles, joints & accessoires de pose", 18, 20),
    ("Outillage du carreleur", 21, 21),
    ("Assainissement, PVC & géotextiles", 22, 22),
    ("Peinture & finition", 23, 25),
    ("Outillage & machines", 26, 28),
    ("Visserie, fixation & chimie du bâtiment", 29, 30),
    ("Installation de chantier, protection & EPI", 31, 32),
    ("Menuiserie", 33, 33),
    ("Livraison & services", 34, 34),
    ("Nous trouver", 35, 35),
    ("Notes", 36, 36),
    ("4e de couverture", 37, 37),
]

# Famille (01-11) -> indices des sections du catalogue qui la couvrent.
FAMILY_SECTIONS = {
    "01": [17],
    "02": [12, 15],
    "03": [2, 3, 4, 13],
    "04": [6],
    "05": [7],
    "06": [8],
    "07": [10],
    "08": [9, 11],
    "09": [14],
    "10": [5, 18],
    "11": [16, 11],
}


def cat_pages_str(a, b):
    pa, pb = a + CATALOG_OFFSET, b + CATALOG_OFFSET
    return f"p. {pa}" if a == b else f"p. {pa} – {pb}"


SERVICES = [
    ("Conseil technique", "Le bon produit et la bonne méthode de pose, expliqués au comptoir."),
    ("Stock sur place", "Vous repartez avec la marchandise. Devis rapide pour le reste."),
    ("Showroom", "Le carrelage se choisit en le touchant : six aspects à comparer en vrai à Alfortville — pierre, bois, marbre, béton, carreau ciment, décor."),
    ("Livraison sous 24 h", "Toute l'Île-de-France : Val-de-Marne, Paris, Seine-Saint-Denis, Hauts-de-Seine, Essonne, et partout ailleurs sur demande."),
    ("Camion-grue 27 t", "Un camion 27 tonnes équipé d'une grue pour décharger directement sur votre chantier."),
    ("Plateau 3,5 t", "Un plateau 3,5 tonnes complète la flotte pour les livraisons urbaines."),
]

CONTACT = {
    "adresse": ["110 rue Édouard Vaillant", "94140 Alfortville"],
    "tel": "01 43 68 83 80",
    "web": "pariscarrelages.fr",
    "email": "snpariscm@gmail.com",
    "insta": "Instagram @pariscarrelages",
    "horaires": [
        ("Lundi – Jeudi", "6 h 30 – 18 h  (pause 12 h – 13 h)"),
        ("Vendredi", "6 h 30 – 17 h  (pause 12 h – 13 h)"),
        ("Samedi", "8 h – 12 h"),
        ("Dimanche", "Fermé"),
    ],
    "livraison": "Val-de-Marne, Paris, Seine-Saint-Denis, Hauts-de-Seine, Essonne. Partout en Île-de-France sur demande.",
    "pour_qui": "Professionnels du bâtiment et particuliers. Réseau de poseurs de confiance sur demande.",
}

FOOTER = "Paris Carrelages & Matériaux  ·  110 rue Édouard Vaillant, 94140 Alfortville  ·  01 43 68 83 80  ·  pariscarrelages.fr"


def wrap(text, font, size, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if pdfmetrics.stringWidth(t, font, size) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def para(c, text, x, y, max_w, font="Sans", size=10, leading=None, color=INK, align="left"):
    leading = leading or size * 1.45
    c.setFont(font, size)
    c.setFillColor(color)
    for ln in wrap(text, font, size, max_w):
        if align == "center":
            c.drawCentredString(x + max_w / 2, y, ln)
        else:
            c.drawString(x, y, ln)
        y -= leading
    return y


def eyebrow(c, text, x, y, color=TERRA, size=8.2, spacing=2.6):
    t = c.beginText(x, y)
    t.setFont("Mono-Bd", size)
    t.setFillColor(color)
    t.setCharSpace(spacing)
    t.textOut(text.upper())
    t.setCharSpace(0)
    c.drawText(t)


def fill_image(c, path, x, y, w, h):
    """Scale to fill the frame, center-cropped — jamais déformée."""
    img = Image.open(path)
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    nw, nh = iw * scale, ih * scale
    c.saveState()
    p = c.beginPath()
    p.rect(x, y, w, h)
    c.clipPath(p, stroke=0)
    c.drawImage(ImageReader(img), x - (nw - w) / 2, y - (nh - h) / 2, nw, nh)
    c.restoreState()


def footer(c, page_no):
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(50, 46, W - 50, 46)
    c.setFont("Sans", 7)
    c.setFillColor(STONE)
    c.drawString(50, 34, FOOTER)
    c.setFont("Mono", 7.5)
    c.drawRightString(W - 50, 34, f"{page_no:02d}")


def logo_box(c, x, y, w, variant="navy"):
    img = f"{FINAL}/logo_navy_white.png" if variant == "navy" else f"{FINAL}/logo_white_alpha.png"
    iw, ih = Image.open(img).size
    if variant == "navy":
        pad = w * 0.09
        c.setFillColor(WHITE)
        c.rect(x, y, w, w * 0.52, stroke=0, fill=1)
        c.drawImage(ImageReader(img), x + pad, y + pad * 0.6, w - 2 * pad,
                    (w - 2 * pad) * ih / iw, mask="auto")
    else:
        c.drawImage(ImageReader(img), x, y, w, w * ih / iw, mask="auto")


class Doc:
    def __init__(self, img_dir):
        self.buf = io.BytesIO()
        self.c = canvas.Canvas(self.buf, pagesize=(W, H))
        self.img_dir = img_dir
        self.page = 0

    def photo(self, name):
        return f"{self.img_dir}/{name}.jpg"

    def new_page(self, bg=SAND):
        if self.page:
            self.c.showPage()
        self.page += 1
        self.c.setFillColor(bg)
        self.c.rect(0, 0, W, H, stroke=0, fill=1)

    def save(self):
        self.c.save()
        self.buf.seek(0)
        return self.buf


def page_cover(d, doc_label):
    d.new_page(bg=NAVY)
    c = d.c
    fill_image(c, d.photo("cover_herringbone"), 0, 0, W, H)
    c.setFillColor(NAVY)
    c.setFillAlpha(0.45)
    c.rect(0, 0, W, 300, stroke=0, fill=1)
    c.setFillAlpha(1)
    logo_box(c, 46, H - 46 - 88, 170)
    eyebrow(c, "Paris Carrelages & Matériaux — Alfortville", 50, 236, color=WHITE, size=8.5, spacing=2.8)
    c.setFillColor(WHITE)
    c.setFont("Playfair-Md", 47)
    c.drawString(48, 176, "Des fondations")
    c.setFont("Playfair-MdIt", 47)
    c.drawString(48, 122, "aux finitions.")
    para(c, "Votre partenaire de proximité pour tous vos projets de construction "
            "et de rénovation.", 50, 92, 340, font="Sans", size=10.5, leading=15, color=WHITE)
    c.setFillColor(NAVY)
    c.rect(0, 0, W, 40, stroke=0, fill=1)
    c.setFillColor(WHITE)
    t = c.beginText(50, 16)
    t.setFont("Mono-Bd", 7.5)
    t.setCharSpace(2)
    t.textOut(doc_label.upper())
    t.setCharSpace(0)
    c.drawText(t)
    c.setFont("Mono-Bd", 7.5)
    c.drawRightString(W - 50, 16, "PARISCARRELAGES.FR")


def page_presentation(d):
    d.new_page()
    c = d.c
    eyebrow(c, "Négoce de matériaux · Alfortville (94)", 50, H - 80)
    c.setFillColor(INK)
    c.setFont("Playfair-Md", 26)
    c.drawString(50, H - 122, "Un seul fournisseur")
    c.drawString(50, H - 154, "pour tout le chantier.")
    c.setStrokeColor(TERRA)
    c.setLineWidth(2)
    c.line(50, H - 176, 96, H - 176)
    y = para(c, "Installation de chantier, machines, gros œuvre, toiture, isolation, "
                "plâtrerie, carrelage, peinture. Un seul fournisseur pour tout le "
                "chantier, livré sous 24 h.", 50, H - 208, 250, size=10.5, leading=16, color=SLATE)
    y = para(c, "Vous n'avez plus à courir d'un dépôt à l'autre. Chaque étape a sa "
                "rangée chez nous, du parpaing à la dernière couche de peinture, en "
                "stock ou livrée sous 24 h.", 50, y - 10, 250, size=10.5, leading=16, color=SLATE)
    para(c, "Et s'il manque quelque chose, demandez au comptoir : on le trouve.",
         50, y - 10, 250, size=10.5, leading=16, color=SLATE)
    fill_image(c, d.photo("chantier_echafaudage"), 330, H - 460, W - 330 - 50, 330)
    c.setFillColor(NAVY)
    c.rect(50, 300, W - 100, 110, stroke=0, fill=1)
    eyebrow(c, "Pros & particuliers · Depuis 2011", 74, 380, color=HexColor("#E9C29F"), size=8)
    para(c, "Votre partenaire de proximité pour tous vos projets de construction "
            "et de rénovation.", 74, 352, W - 148, font="Playfair-MdIt", size=15, leading=21, color=WHITE)
    c.setFillColor(WHITE)
    c.rect(50, 210, W - 100, 66, stroke=0, fill=1)
    c.setStrokeColor(LINE)
    c.rect(50, 210, W - 100, 66, stroke=1, fill=0)
    eyebrow(c, "Notre métier d'origine", 74, 254, size=7.5)
    para(c, "Le carrelage se choisit en le touchant. Grès cérame et faïence de "
            "fabricants reconnus, six aspects à comparer en vrai dans notre showroom.",
         74, 236, W - 148, size=9.5, leading=13.5, color=SLATE)
    footer(c, d.page)


def page_services(d):
    d.new_page()
    c = d.c
    eyebrow(c, "Services", 50, H - 80)
    c.setFillColor(INK)
    c.setFont("Playfair-Md", 30)
    c.drawString(50, H - 122, "Le comptoir, le stock,")
    c.drawString(50, H - 156, "la livraison.")
    c.setStrokeColor(TERRA)
    c.setLineWidth(2)
    c.line(50, H - 178, 96, H - 178)
    para(c, "Conseil, stock, showroom et livraison : tout est pensé pour faire "
            "avancer votre chantier sans perdre une journée.", 50, H - 208, 440,
         size=10.5, leading=16, color=SLATE)
    top = H - 250
    col_w, row_h, gap = (W - 100 - 20) / 2, 136, 10
    for i, (title, txt) in enumerate(SERVICES):
        cx = 50 + (i % 2) * (col_w + 20)
        cy = top - (i // 2) * (row_h + gap) - row_h
        c.setFillColor(WHITE)
        c.rect(cx, cy, col_w, row_h, stroke=0, fill=1)
        c.setStrokeColor(LINE)
        c.rect(cx, cy, col_w, row_h, stroke=1, fill=0)
        c.setFillColor(TERRA)
        c.rect(cx, cy, 3, row_h, stroke=0, fill=1)
        c.setFillColor(INK)
        c.setFont("Sans-Bd", 12.5)
        c.drawString(cx + 20, cy + row_h - 32, title)
        para(c, txt, cx + 20, cy + row_h - 52, col_w - 40, size=9.3, leading=13, color=SLATE)
    y = top - 3 * (row_h + gap) - 30
    c.setFillColor(NAVY)
    c.rect(50, y - 66, W - 100, 66, stroke=0, fill=1)
    eyebrow(c, "Disponibilité & devis", 74, y - 26, color=HexColor("#E9C29F"), size=7.5)
    para(c, "Devis rapide au comptoir, par téléphone au 01 43 68 83 80 ou par "
            "e-mail à snpariscm@gmail.com.", 74, y - 44, W - 148, size=9.8, leading=14, color=WHITE)
    footer(c, d.page)


def page_families_short(d, fams, photo, first_no):
    d.new_page()
    c = d.c
    fill_image(c, d.photo(photo), 50, H - 270, W - 100, 200)
    eyebrow(c, "Le parcours du chantier", 50, H - 300)
    c.setFillColor(INK)
    c.setFont("Playfair-Md", 22)
    c.drawString(50, H - 330, f"Nos familles de produits · {fams[0][0]} à {fams[-1][0]}")
    y = H - 372
    for num, title, desc, _ in fams:
        c.setFont("Playfair-MdIt", 15)
        c.setFillColor(TERRA)
        c.drawString(50, y, num)
        c.setFont("Sans-Bd", 12.5)
        c.setFillColor(INK)
        c.drawString(92, y, title)
        para(c, desc, 92, y - 20, W - 142, size=9.6, leading=13.5, color=SLATE)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.6)
        c.line(92, y - 52, W - 50, y - 52)
        y -= 78
    footer(c, d.page)


def page_family_divider(d, fam):
    num, title, desc, photo = fam
    d.new_page()
    c = d.c
    if photo:
        fill_image(c, d.photo(photo), 0, H - 330, W, 330)
        top = H - 330
    else:
        c.setFillColor(NAVY)
        c.rect(0, H - 330, W, 330, stroke=0, fill=1)
        c.setFont("Playfair-Md", 150)
        c.setFillColor(HexColor("#17486F"))
        c.drawRightString(W - 50, H - 280, num)
        top = H - 330
    eyebrow(c, f"Famille {num} / 11", 50, top - 46)
    c.setFillColor(INK)
    c.setFont("Playfair-Md", 27)
    for i, ln in enumerate(wrap(title, "Playfair-Md", 27, W - 100)):
        c.drawString(50, top - 82 - i * 34, ln)
        nlines = i + 1
    y = para(c, desc, 50, top - 82 - nlines * 34 - 14, 400, size=11, leading=16.5, color=SLATE)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(50, y - 24, W - 50, y - 24)
    eyebrow(c, "Les références au catalogue général", 50, y - 52, size=7.5)
    yy = y - 76
    for idx in FAMILY_SECTIONS[num]:
        name, a, b = CATALOG_SECTIONS[idx]
        c.setFont("Sans-SB", 10)
        c.setFillColor(INK)
        c.drawString(50, yy, f"« {name} »")
        c.setFont("Mono-Bd", 9)
        c.setFillColor(TERRA)
        c.drawRightString(W - 50, yy, cat_pages_str(a, b))
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.line(50, yy - 8, W - 50, yy - 8)
        yy -= 26
    para(c, "Toutes les références, dimensions et conditionnements figurent sur "
            "ces pages, reprises à l'identique dans la seconde partie de cette plaquette.",
         50, yy - 6, 400, size=9.2, leading=13.5, color=STONE)
    footer(c, d.page)


def page_brands_contact(d, complete=False):
    d.new_page()
    c = d.c
    eyebrow(c, "Certains de nos fabricants", 50, H - 80)
    c.setFillColor(INK)
    c.setFont("Playfair-Md", 26)
    c.drawString(50, H - 116, "Des marques reconnues,")
    c.drawString(50, H - 148, "au comptoir comme en livraison.")
    row_w = W - 100
    row_h = row_w * 166 / 2088
    for i, row in enumerate(["brands_row1", "brands_row2"]):
        img = f"{FINAL}/{row}.png"
        c.drawImage(ImageReader(img), 50, H - 185 - row_h - i * (row_h + 12),
                    row_w, row_h, mask="auto")
    block_top = H - 185 - 2 * row_h - 12 - 28
    c.setFillColor(NAVY)
    c.rect(50, 185, W - 100, block_top - 185, stroke=0, fill=1)
    eyebrow(c, "Passez au comptoir", 74, block_top - 30, color=HexColor("#E9C29F"), size=8.5)
    c.setFont("Playfair-Md", 19)
    c.setFillColor(WHITE)
    c.drawString(74, block_top - 58, "Le comptoir est ouvert dès 6 h 30.")
    c.setFont("Sans-SB", 10.5)
    c.drawString(74, block_top - 82, CONTACT["adresse"][0] + ", " + CONTACT["adresse"][1])
    c.setFont("Sans", 9.5)
    c.drawString(74, block_top - 99, CONTACT["tel"] + "  ·  " + CONTACT["email"])
    c.drawString(74, block_top - 114, CONTACT["web"] + "  ·  " + CONTACT["insta"])
    yy = block_top - 140
    c.setFont("Mono-Bd", 7.2)
    c.setFillColor(HexColor("#E9C29F"))
    c.drawString(74, yy, "HORAIRES")
    c.setFillColor(WHITE)
    for day, hrs in CONTACT["horaires"]:
        yy -= 15
        c.setFont("Sans-SB", 9.2)
        c.drawString(74, yy, day)
        c.setFont("Sans", 9.2)
        c.drawRightString(W - 74, yy, hrs)
    yy -= 26
    c.setFont("Mono-Bd", 7.2)
    c.setFillColor(HexColor("#E9C29F"))
    c.drawString(74, yy, "NOUS LIVRONS")
    yy = para(c, CONTACT["livraison"], 74, yy - 16, W - 148, size=9.2, leading=13, color=WHITE)
    c.setFillColor(TERRA)
    c.rect(50, 128, W - 100, 38, stroke=0, fill=1)
    c.setFillColor(WHITE)
    label = "PASSEZ AU COMPTOIR — DEVIS RAPIDE SUR PLACE OU PAR TÉLÉPHONE"
    t = c.beginText(0, 141)
    t.setFont("Sans-Bd", 12)
    t.setCharSpace(1.2)
    tw = pdfmetrics.stringWidth(label, "Sans-Bd", 12) + 1.2 * (len(label) - 1)
    t.setTextOrigin(W / 2 - tw / 2, 141)
    t.textOut(label)
    t.setCharSpace(0)
    c.drawText(t)
    footer(c, d.page)


def page_sommaire(d, cat_start, contact_page):
    d.new_page()
    c = d.c
    eyebrow(c, "Sommaire", 50, H - 80)
    c.setFillColor(INK)
    c.setFont("Playfair-Md", 30)
    c.drawString(50, H - 122, "Le chantier, de A à Z.")
    entries = [
        ("Présentation", "Un seul fournisseur pour tout le chantier", "02"),
        ("Services", "Conseil, stock, showroom, livraison 24 h", "03"),
        ("Le parcours du chantier", "Onze familles, dans l'ordre du chantier", "05"),
        ("Les 11 familles de produits", "Une page par famille", "06"),
        ("Fabricants", "Les marques présentes au comptoir", "17"),
        ("Catalogue général", "Toutes les références, pages d'origine", f"{cat_start:02d}"),
        ("Contact & horaires", "Passez au comptoir", f"{contact_page:02d}"),
    ]
    y = H - 176
    for title, sub, no in entries:
        c.setFont("Playfair-Md", 13.5)
        c.setFillColor(INK)
        c.drawString(50, y, title)
        c.setFont("Sans", 8.8)
        c.setFillColor(SLATE)
        c.drawString(50, y - 14, sub)
        c.setFont("Playfair-MdIt", 13.5)
        c.setFillColor(TERRA)
        c.drawRightString(285, y, no)
        c.setStrokeColor(LINE)
        c.line(50, y - 26, 285, y - 26)
        y -= 46
    # Index précis du catalogue général (colonne droite)
    x2 = 320
    eyebrow(c, "Index du catalogue général", x2, H - 176, size=7.5)
    yy = H - 200
    for name, a, b in CATALOG_SECTIONS:
        c.setFont("Sans", 8.8)
        c.setFillColor(INK)
        label = name if pdfmetrics.stringWidth(name, "Sans", 8.8) <= 185 else name[:44] + "…"
        c.drawString(x2, yy, label)
        c.setFont("Mono", 8)
        c.setFillColor(TERRA)
        c.drawRightString(W - 50, yy, cat_pages_str(a, b).replace("p. ", ""))
        c.setStrokeColor(LINE)
        c.setLineWidth(0.4)
        c.line(x2, yy - 6.5, W - 50, yy - 6.5)
        yy -= 21.5
    footer(c, d.page)


def page_parcours(d):
    d.new_page()
    c = d.c
    eyebrow(c, "Le parcours du chantier", 50, H - 80)
    c.setFillColor(INK)
    c.setFont("Playfair-Md", 30)
    c.drawString(50, H - 122, "Onze familles,")
    c.drawString(50, H - 156, "dans l'ordre du chantier.")
    c.setStrokeColor(TERRA)
    c.setLineWidth(2)
    c.line(50, H - 178, 96, H - 178)
    para(c, "Du premier film de protection au dernier profilé de finition, chaque "
            "étape a sa rangée chez nous. Suivez le fil.", 50, H - 208, 440,
         size=10.5, leading=16, color=SLATE)
    y = H - 252
    for num, title, desc, _ in FAMILIES:
        c.setFont("Playfair-MdIt", 12)
        c.setFillColor(TERRA)
        c.drawString(50, y, num)
        c.setFont("Sans-Bd", 11)
        c.setFillColor(INK)
        c.drawString(88, y, title)
        para(c, desc, 88, y - 16, W - 138, size=8.8, leading=12, color=SLATE)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.line(88, y - 36, W - 50, y - 36)
        y -= 47.5
    footer(c, d.page)


def page_catalog_divider(d, cat_pages):
    d.new_page(bg=NAVY)
    c = d.c
    logo_box(c, 50, H - 150, 150, variant="white")
    eyebrow(c, "Seconde partie", 50, H - 240, color=HexColor("#E9C29F"))
    c.setFillColor(WHITE)
    c.setFont("Playfair-Md", 34)
    c.drawString(50, H - 288, "Catalogue général.")
    para(c, f"Les {cat_pages} pages du catalogue général sont reprises en "
            "intégralité dans les pages suivantes, telles qu'éditées : aucune "
            "référence supprimée, aucune page retirée.",
         50, H - 330, 420, size=11, leading=17, color=HexColor("#DCE6EE"))
    para(c, "Ciments, chaux, plâtres, bétons & mortiers — et l'ensemble des "
            "familles du parcours du chantier, avec conditionnements et marques.",
         50, H - 400, 420, size=10, leading=15, color=HexColor("#9FB4C6"))
    fill_image(c, d.photo("maison_chantier"), 50, 120, W - 100, 300)
    c.setFillColor(WHITE)
    t = c.beginText(50, 84)
    t.setFont("Mono-Bd", 7.5)
    t.setCharSpace(2)
    t.textOut("CATALOGUE GÉNÉRAL — PAGES D'ORIGINE REPRISES SANS MODIFICATION")
    t.setCharSpace(0)
    c.drawText(t)


def page_contact_final(d):
    d.new_page()
    c = d.c
    logo_box(c, 50, H - 140, 150)
    eyebrow(c, "Contact", 50, H - 200)
    c.setFillColor(INK)
    c.setFont("Playfair-Md", 30)
    c.drawString(50, H - 242, "Le comptoir est ouvert")
    c.drawString(50, H - 276, "dès 6 h 30.")
    fill_image(c, f"{FINAL}/plan_acces.png", 330, H - 470, W - 330 - 50, 210)
    y = H - 330
    blocks = [
        ("ADRESSE", ["110 rue Édouard Vaillant", "94140 Alfortville"]),
        ("TÉLÉPHONE", ["01 43 68 83 80"]),
        ("EN LIGNE", ["pariscarrelages.fr", "snpariscm@gmail.com", "Instagram @pariscarrelages"]),
    ]
    for label, lines in blocks:
        eyebrow(c, label, 50, y, size=7.2)
        c.setFillColor(INK)
        c.setFont("Sans-SB", 11.5)
        for ln in lines:
            y -= 20
            c.drawString(50, y, ln)
        y -= 30
    c.setFillColor(WHITE)
    c.rect(50, 210, W - 100, 190, stroke=0, fill=1)
    c.setStrokeColor(LINE)
    c.rect(50, 210, W - 100, 190, stroke=1, fill=0)
    eyebrow(c, "Horaires", 74, 376, size=7.2)
    yy = 356
    for day, hrs in CONTACT["horaires"]:
        c.setFont("Sans", 9.8)
        c.setFillColor(INK)
        c.drawString(74, yy, day)
        c.setFillColor(SLATE)
        c.drawRightString(W - 74, yy, hrs)
        yy -= 20
    eyebrow(c, "Nous livrons", 74, yy - 8, size=7.2)
    para(c, CONTACT["livraison"], 74, yy - 26, W - 148, size=9.4, leading=13.5, color=SLATE)
    eyebrow(c, "Pour qui", 74, 172, size=7.2)
    para(c, CONTACT["pour_qui"], 74, 154, W - 148, size=9.4, leading=13.5, color=SLATE)
    c.setFillColor(TERRA)
    c.rect(50, 74, W - 100, 38, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("Sans-Bd", 13)
    label = "PASSEZ AU COMPTOIR"
    t = c.beginText(0, 100)
    t.setFont("Sans-Bd", 13)
    t.setCharSpace(1.5)
    tw = pdfmetrics.stringWidth(label, "Sans-Bd", 13) + 1.5 * (len(label) - 1)
    t.setTextOrigin(W / 2 - tw / 2, 87)
    t.textOut(label)
    t.setCharSpace(0)
    c.drawText(t)
    footer(c, d.page)


def prep_images(quality, max_dim):
    """Photos en JPEG (pas de déformation), logo et bandeaux en PNG d'origine."""
    out = f"/tmp/pcm_imgs_{quality}"
    os.makedirs(out, exist_ok=True)
    names = ["cover_herringbone", "chantier_echafaudage", "isolation_mur", "peinture_rouleaux",
             "carrelage_marbre", "faience_niche", "carreaux_ciment", "ouvrier_chantier",
             "maison_chantier"]
    q = 88 if quality == "hq" else 52
    md = 2200 if quality == "hq" else 1100
    for n in names:
        img = Image.open(f"{FINAL}/{n}.png").convert("RGB")
        if max(img.size) > md:
            r = md / max(img.size)
            img = img.resize((int(img.width * r), int(img.height * r)), Image.LANCZOS)
        img.save(f"{out}/{n}.jpg", quality=q, optimize=True)
    return out


def build_short(img_dir):
    d = Doc(img_dir)
    page_cover(d, "Plaquette commerciale · Alfortville")
    page_presentation(d)
    page_services(d)
    groups = [(FAMILIES[0:3], "ouvrier_chantier"), (FAMILIES[3:6], "isolation_mur"),
              (FAMILIES[6:8], "carrelage_marbre"), (FAMILIES[8:11], "peinture_rouleaux")]
    for fams, photo in groups:
        page_families_short(d, fams, photo, fams[0][0])
    page_brands_contact(d)
    return d.save()


def build_complete_front(img_dir, cat_pages):
    d = Doc(img_dir)
    page_cover(d, "Plaquette complète & catalogue général")
    page_presentation(d)
    page_services(d)
    contact_page = 18 + cat_pages + 1
    page_sommaire(d, cat_start=19, contact_page=contact_page)
    page_parcours(d)
    for fam in FAMILIES:
        page_family_divider(d, fam)
    page_brands_contact(d, complete=True)
    page_catalog_divider(d, cat_pages)
    return d


def build_complete_back(img_dir):
    d = Doc(img_dir)
    page_contact_final(d)
    return d.save()


def merge(front_buf, catalog_path, back_buf, out_path):
    w = PdfWriter()
    w.append(PdfReader(front_buf))
    w.append(PdfReader(catalog_path))
    w.append(PdfReader(back_buf))
    with open(out_path, "wb") as f:
        w.write(f)


def compress_email(src, dst):
    doc = pymupdf.open(src)
    try:
        doc.rewrite_images(dpi_threshold=160, dpi_target=110, quality=55)
    except Exception as e:
        print("rewrite_images indisponible:", e)
    doc.save(dst, garbage=4, deflate=True)
    doc.close()


def main():
    catalog = f"{SRC}/catalogue_pcm.pdf"
    cat_pages = PdfReader(catalog).get_num_pages()
    print("pages catalogue:", cat_pages)

    for quality, suffix in [("hq", ""), ("email", "_Email")]:
        img_dir = prep_images(quality, 2200 if quality == "hq" else 1100)

        short = build_short(img_dir)
        short_path = f"{OUT}/Paris_Carrelages_Materiaux_Plaquette_Courte{suffix}.pdf"
        with open(short_path, "wb") as f:
            f.write(short.getvalue())

        front = build_complete_front(img_dir, cat_pages)
        back = build_complete_back(img_dir)
        complete_path = f"{OUT}/Paris_Carrelages_Materiaux_Plaquette_Complete{suffix}.pdf"
        merge(front.save(), catalog, back, complete_path)

        if quality == "hq":
            compress_email(short_path, f"{OUT}/tmp_short_email.pdf")
            compress_email(complete_path, f"{OUT}/tmp_complete_email.pdf")

        print(quality, "ok")

    # La compression pymupdf des versions HQ génère les variantes e-mail des pages
    # fusionnées ; on conserve les versions reconstruites (images déjà optimisées)
    # si plus légères.
    for base, tmp in [("Paris_Carrelages_Materiaux_Plaquette_Courte", "tmp_short_email.pdf"),
                      ("Paris_Carrelages_Materiaux_Plaquette_Complete", "tmp_complete_email.pdf")]:
        rebuilt = f"{OUT}/{base}_Email.pdf"
        compressed = f"{OUT}/{tmp}"
        if os.path.exists(compressed) and os.path.getsize(compressed) < os.path.getsize(rebuilt):
            os.replace(compressed, rebuilt)
        elif os.path.exists(compressed):
            os.remove(compressed)

    for f in sorted(os.listdir(OUT)):
        print(f, f"{os.path.getsize(f'{OUT}/{f}') / 1e6:.1f} Mo")


if __name__ == "__main__":
    main()

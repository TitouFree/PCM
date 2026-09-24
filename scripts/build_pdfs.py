#!/usr/bin/env python3
"""Génère les DEUX NOUVELLES plaquettes fusionnées de Paris Carrelages et Matériaux.

Sources officielles : « Ebauche 4 - Le Magazine.pdf » (identité, textes, visuels)
et « Catalogue general PCM.pdf » (37 pages de références, 100 % image).

Principe : nouvelle composition graphique (ReportLab) ; le contenu-références du
catalogue est réorganisé sous les 11 familles du parcours du chantier. Chaque page
du catalogue d'origine est reprise SANS MODIFICATION de contenu, rendue en haute
définition et recadrée dans la maquette uniforme (bandeau famille, marges,
pagination, pied de page PCM). Aucune référence inventée, aucune page supprimée.
"""
import io
import os

import pymupdf
from PIL import Image
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

W, H = 595.27, 841.89   # A4 portrait
LW, LH = 841.89, 595.28  # A4 paysage (pages de références, lisibilité préservée)

NAVY = HexColor("#0D3A5C")
TERRA = HexColor("#A8623E")
SAND = HexColor("#F6F4ED")
INK = HexColor("#1F2226")
SLATE = HexColor("#5A5F66")
STONE = HexColor("#8E949D")
LINE = HexColor("#DDD8D0")
WHITE = HexColor("#FFFFFF")
SAND_SOFT = HexColor("#E9C29F")

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

# Réorganisation RÉELLE du catalogue (lu page par page sur les en-têtes d'origine) :
# famille -> [(nom de section d'origine, page catalogue début, page catalogue fin)]
FAMILY_PAGES = {
    "01": [("Installation de chantier, protection & EPI", 31, 32)],
    "02": [("Outillage du carreleur", 21, 21), ("Outillage & machines", 26, 28)],
    "03": [("Blocs béton, briques & terre cuite", 3, 4),
           ("Ciments, chaux, plâtres, bétons & mortiers", 5, 6),
           ("Ferraillage & acier", 7, 7),
           ("Assainissement, PVC & géotextiles", 22, 22)],
    "04": [("Toiture, couverture & zinguerie", 10, 10)],
    "05": [("Isolation", 11, 12)],
    "06": [("Plaques de plâtre, ossatures & carreaux de plâtre", 13, 14)],
    "07": [("Carrelage & faïence", 17, 17)],
    "08": [("Enduits, ragréages & mortiers techniques", 15, 16),
           ("Colles, joints & accessoires de pose", 18, 20)],
    "09": [("Peinture & finition", 23, 25)],
    "10": [("Bois de coffrage, charpente & panneaux", 8, 9), ("Menuiserie", 33, 33)],
    "11": [("Visserie, fixation & chimie du bâtiment", 29, 30)],
}

# Pages du catalogue hors familles, conservées en annexes (aucune page supprimée).
ANNEX_PAGES = [
    ("Couverture du catalogue d'origine", 1),
    ("Index du catalogue d'origine", 2),
    ("Livraison & services", 34),
    ("Nous trouver", 35),
    ("Notes", 36),
    ("4e de couverture du catalogue d'origine", 37),
]

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
FOOTER_SHORT = "Paris Carrelages & Matériaux · Alfortville · 01 43 68 83 80 · pariscarrelages.fr"


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


def spaced(c, x, y, text, font="Mono-Bd", size=8.2, spacing=2.6, color=TERRA):
    t = c.beginText(x, y)
    t.setFont(font, size)
    t.setFillColor(color)
    t.setCharSpace(spacing)
    t.textOut(text.upper())
    t.setCharSpace(0)
    c.drawText(t)


def eyebrow(c, text, x, y, color=TERRA, size=8.2, spacing=2.6):
    spaced(c, x, y, text, size=size, spacing=spacing, color=color)


def centered_spaced(c, y, label, font="Sans-Bd", size=13, spacing=1.5, color=WHITE, page_w=W):
    t = c.beginText(0, y)
    t.setFont(font, size)
    t.setFillColor(color)
    t.setCharSpace(spacing)
    tw = pdfmetrics.stringWidth(label, font, size) + spacing * (len(label) - 1)
    t.setTextOrigin(page_w / 2 - tw / 2, y)
    t.textOut(label)
    t.setCharSpace(0)
    c.drawText(t)


def fill_image(c, path, x, y, w, h):
    """Remplit le cadre en recadrant au centre — jamais déformée."""
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

    def cat(self, page_no):
        return f"{self.img_dir}/cat_p{page_no}.jpg"

    def new_page(self, bg=SAND):
        if self.page:
            self.c.showPage()
            self.c.setPageSize((W, H))
        self.page += 1
        self.c.setFillColor(bg)
        self.c.rect(0, 0, W, H, stroke=0, fill=1)

    def new_landscape_page(self):
        if self.page:
            self.c.showPage()
        self.c.setPageSize((LW, LH))
        self.page += 1
        self.c.setFillColor(SAND)
        self.c.rect(0, 0, LW, LH, stroke=0, fill=1)

    def save(self):
        self.c.save()
        self.buf.seek(0)
        return self.buf


# ---------------------------------------------------------------- pages portrait

def page_cover(d, doc_label, subtitle=None):
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
    spaced(c, 50, 16, doc_label, size=7.5, spacing=2, color=WHITE)
    c.setFillColor(WHITE)
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
    eyebrow(c, "Pros & particuliers · Depuis 2011", 74, 380, color=SAND_SOFT, size=8)
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
    eyebrow(c, "Disponibilité & devis", 74, y - 26, color=SAND_SOFT, size=7.5)
    para(c, "Devis rapide au comptoir, par téléphone au 01 43 68 83 80 ou par "
            "e-mail à snpariscm@gmail.com.", 74, y - 44, W - 148, size=9.8, leading=14, color=WHITE)
    footer(c, d.page)


def family_catalog_names(num):
    return "  ·  ".join(name for name, _, _ in FAMILY_PAGES[num])


def page_families_short(d, fams, photo):
    """Plaquette courte : 11 familles + infos essentielles du catalogue (sections réelles)."""
    d.new_page()
    c = d.c
    fill_image(c, d.photo(photo), 50, H - 262, W - 100, 192)
    eyebrow(c, "Le parcours du chantier", 50, H - 292)
    c.setFillColor(INK)
    c.setFont("Playfair-Md", 22)
    c.drawString(50, H - 322, f"Nos familles de produits · {fams[0][0]} à {fams[-1][0]}")
    y = H - 362
    for num, title, desc, _ in fams:
        c.setFont("Playfair-MdIt", 15)
        c.setFillColor(TERRA)
        c.drawString(50, y, num)
        c.setFont("Sans-Bd", 12.5)
        c.setFillColor(INK)
        c.drawString(92, y, title)
        para(c, desc, 92, y - 20, W - 142, size=9.6, leading=13, color=SLATE)
        eyebrow(c, "Au catalogue :", 92, y - 48, size=6.4, spacing=1.2, color=STONE)
        para(c, family_catalog_names(num), 168, y - 48, W - 218, size=8.2, leading=11, color=SLATE)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.6)
        c.line(92, y - 78, W - 50, y - 78)
        y -= 104
    footer(c, d.page)


def page_family_divider(d, fam, ref_start, ref_end):
    """Plaquette complète : page famille + renvoi précis aux pages de références."""
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
    nlines = 0
    for i, ln in enumerate(wrap(title, "Playfair-Md", 27, W - 100)):
        c.drawString(50, top - 82 - i * 34, ln)
        nlines = i + 1
    y = para(c, desc, 50, top - 82 - nlines * 34 - 14, 400, size=11, leading=16.5, color=SLATE)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(50, y - 24, W - 50, y - 24)
    eyebrow(c, f"Les références — pages {ref_start} à {ref_end} de cette plaquette", 50, y - 52, size=7.5)
    yy = y - 76
    for name, a, b in FAMILY_PAGES[num]:
        c.setFont("Sans-SB", 10)
        c.setFillColor(INK)
        c.drawString(50, yy, f"« {name} »")
        c.setFont("Mono", 7.5)
        c.setFillColor(STONE)
        orig = f"catalogue d'origine p. {a}" if a == b else f"catalogue d'origine p. {a} à {b}"
        c.drawRightString(W - 50, yy, orig)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.line(50, yy - 8, W - 50, yy - 8)
        yy -= 26
    para(c, "Toutes les références, dimensions et conditionnements figurent sur les "
            "pages suivantes, reprises sans modification du catalogue général.",
         50, yy - 6, 400, size=9.2, leading=13.5, color=STONE)
    footer(c, d.page)


def page_catalog_reframed(d, orig_page, band_label, section_name):
    """Page du catalogue d'origine recadrée dans la maquette uniforme (paysage)."""
    d.new_landscape_page()
    c = d.c
    c.setFillColor(NAVY)
    c.rect(0, LH - 34, LW, 34, stroke=0, fill=1)
    spaced(c, 24, LH - 22, band_label, size=7.2, spacing=1.6, color=WHITE)
    c.setFillColor(WHITE)
    c.setFont("Sans-SB", 10)
    c.drawRightString(LW - 24, LH - 22, f"« {section_name} »")
    img = Image.open(d.cat(orig_page))
    iw, ih = img.size
    max_w, max_h = LW - 48, LH - 34 - 20 - 24
    scale = min(max_w / iw, max_h / ih)
    nw, nh = iw * scale, ih * scale
    c.drawImage(ImageReader(img), (LW - nw) / 2, 20 + (max_h - nh) / 2, nw, nh)
    c.setFillColor(NAVY)
    c.rect(0, 0, LW, 20, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("Sans", 7)
    c.drawString(24, 7, f"Catalogue général d'origine, page {orig_page} — reprise sans modification  ·  {FOOTER_SHORT}")
    c.setFont("Mono", 8)
    c.drawRightString(LW - 24, 7, f"{d.page:02d}")


def page_brands_contact(d):
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
    eyebrow(c, "Passez au comptoir", 74, block_top - 30, color=SAND_SOFT, size=8.5)
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
    c.setFillColor(SAND_SOFT)
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
    c.setFillColor(SAND_SOFT)
    c.drawString(74, yy, "NOUS LIVRONS")
    para(c, CONTACT["livraison"], 74, yy - 16, W - 148, size=9.2, leading=13, color=WHITE)
    c.setFillColor(TERRA)
    c.rect(50, 128, W - 100, 38, stroke=0, fill=1)
    centered_spaced(c, 141, "PASSEZ AU COMPTOIR — DEVIS RAPIDE SUR PLACE OU PAR TÉLÉPHONE", size=12, spacing=1.2)
    footer(c, d.page)


def page_sommaire(d, fam_range, annex_divider, fabricants_page, contact_page):
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
    ]
    y = H - 172
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
    tail = [
        ("Annexes du catalogue", "Pages d'origine conservées", f"{annex_divider:02d}"),
        ("Fabricants", "Les marques présentes au comptoir", f"{fabricants_page:02d}"),
        ("Contact & horaires", "Passez au comptoir", f"{contact_page:02d}"),
    ]
    for title, sub, no in tail:
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
    x2 = 320
    eyebrow(c, "Les 11 familles & leurs références", x2, H - 172, size=7.5)
    yy = H - 196
    for num, title, _, _ in FAMILIES:
        a, b = fam_range[num]
        c.setFont("Sans-SB", 9.2)
        c.setFillColor(INK)
        c.drawString(x2, yy, f"{num} · {title}")
        c.setFont("Mono", 8)
        c.setFillColor(TERRA)
        c.drawRightString(W - 50, yy, f"p. {a:02d} – {b:02d}")
        c.setStrokeColor(LINE)
        c.setLineWidth(0.4)
        c.line(x2, yy - 7, W - 50, yy - 7)
        yy -= 24
    para(c, "Le catalogue général est réorganisé sous ces onze familles : chaque page "
            "de références est reprise sans modification dans la maquette de cette "
            "plaquette.", x2, yy - 10, W - 50 - x2, size=8.6, leading=12.5, color=SLATE)
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


def page_annex_divider(d, annex_pages_start):
    d.new_page(bg=NAVY)
    c = d.c
    logo_box(c, 50, H - 150, 150, variant="white")
    eyebrow(c, "Annexes", 50, H - 240, color=SAND_SOFT)
    c.setFillColor(WHITE)
    c.setFont("Playfair-Md", 34)
    c.drawString(50, H - 288, "Pages d'origine du catalogue.")
    para(c, "Les pages d'information générale du catalogue d'origine sont conservées "
            "ici, sans modification : couverture, index, livraison & services, "
            "coordonnées et page de notes.", 50, H - 330, 420, size=11, leading=17,
         color=HexColor("#DCE6EE"))
    yy = H - 420
    for name, p in ANNEX_PAGES:
        c.setFont("Sans-SB", 10.5)
        c.setFillColor(WHITE)
        c.drawString(50, yy, name)
        c.setFont("Mono", 8)
        c.setFillColor(SAND_SOFT)
        c.drawRightString(W - 50, yy, f"catalogue d'origine p. {p} · plaquette p. {annex_pages_start + ANNEX_PAGES.index((name, p)):02d}")
        c.setStrokeColor(HexColor("#17486F"))
        c.setLineWidth(0.6)
        c.line(50, yy - 9, W - 50, yy - 9)
        yy -= 30
    fill_image(c, d.photo("maison_chantier"), 50, 60, W - 100, 200)


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
    centered_spaced(c, 87, "PASSEZ AU COMPTOIR", size=13, spacing=1.5)
    footer(c, d.page)


# ---------------------------------------------------------------- construction

def prep_images(quality):
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


def render_catalog(quality):
    """Rend chaque page du catalogue d'origine en image HD (contenu inchangé)."""
    out = f"/tmp/pcm_imgs_{quality}"
    dpi, q = (150, 85) if quality == "hq" else (100, 65)
    doc = pymupdf.open(f"{SRC}/catalogue_pcm.pdf")
    for i in range(doc.page_count):
        path = f"{out}/cat_p{i+1}.jpg"
        if os.path.exists(path):
            continue
        pix = doc[i].get_pixmap(dpi=dpi)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        img.save(path, quality=q, optimize=True)
    doc.close()


def build_short(img_dir):
    d = Doc(img_dir)
    page_cover(d, "Plaquette commerciale · Alfortville")
    page_presentation(d)
    page_services(d)
    groups = [(FAMILIES[0:3], "ouvrier_chantier"), (FAMILIES[3:6], "isolation_mur"),
              (FAMILIES[6:8], "carrelage_marbre"), (FAMILIES[8:11], "peinture_rouleaux")]
    for fams, photo in groups:
        page_families_short(d, fams, photo)
    page_brands_contact(d)
    return d.save()


def build_complete(img_dir):
    d = Doc(img_dir)
    fam_refs = {num: [p for _, a, b in FAMILY_PAGES[num] for p in range(a, b + 1)]
                for num, _, _, _ in FAMILIES}
    fam_range, cursor = {}, 6
    for num, _, _, _ in FAMILIES:
        fam_range[num] = (cursor, cursor + len(fam_refs[num]))
        cursor += len(fam_refs[num]) + 1
    annex_divider = cursor
    annex_start = cursor + 1
    fabricants_page = annex_start + len(ANNEX_PAGES)
    contact_page = fabricants_page + 1

    page_cover(d, "Plaquette complète · présentation & catalogue réorganisé")
    page_presentation(d)
    page_services(d)
    page_sommaire(d, fam_range, annex_divider, fabricants_page, contact_page)
    page_parcours(d)
    for fam in FAMILIES:
        num = fam[0]
        a, b = fam_range[num]
        page_family_divider(d, fam, a + 1, b)
        for orig_page in fam_refs[num]:
            section = next(n for n, x, y in FAMILY_PAGES[num] if x <= orig_page <= y)
            page_catalog_reframed(d, orig_page,
                                  f"Famille {num} · {fam[1]}", section)
    page_annex_divider(d, annex_start)
    for name, p in ANNEX_PAGES:
        page_catalog_reframed(d, p, "Annexe · catalogue d'origine", name)
    page_brands_contact(d)
    page_contact_final(d)
    return d.save()


def compress_email(src, dst):
    doc = pymupdf.open(src)
    try:
        doc.rewrite_images(dpi_threshold=160, dpi_target=110, quality=55)
    except Exception as e:
        print("rewrite_images indisponible:", e)
    doc.save(dst, garbage=4, deflate=True)
    doc.close()


def main():
    import shutil
    shutil.rmtree("/tmp/pcm_imgs_hq", ignore_errors=True)
    shutil.rmtree("/tmp/pcm_imgs_email", ignore_errors=True)
    for quality, suffix in [("hq", ""), ("email", "_Email")]:
        img_dir = prep_images(quality)
        render_catalog(quality)

        short = build_short(img_dir)
        with open(f"{OUT}/PCM_Plaquette_Courte_Fusionnee{suffix}.pdf", "wb") as f:
            f.write(short.getvalue())

        complete = build_complete(img_dir)
        with open(f"{OUT}/PCM_Plaquette_Complete_Fusionnee{suffix}.pdf", "wb") as f:
            f.write(complete.getvalue())
        print(quality, "ok")

    # Passe de compression finale sur les versions e-mail (images ré-échantillonnées).
    for base in ["PCM_Plaquette_Courte_Fusionnee", "PCM_Plaquette_Complete_Fusionnee"]:
        p = f"{OUT}/{base}_Email.pdf"
        tmp = f"{OUT}/_tmp_email.pdf"
        compress_email(p, tmp)
        if os.path.getsize(tmp) < os.path.getsize(p):
            os.replace(tmp, p)
        else:
            os.remove(tmp)

    for f in sorted(os.listdir(OUT)):
        if f.startswith("PCM_"):
            print(f, f"{os.path.getsize(f'{OUT}/{f}') / 1e6:.1f} Mo")


if __name__ == "__main__":
    main()

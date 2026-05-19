#!/usr/bin/env python3
"""Add SEO meta tags to all Autohaus HTML pages."""

import re
import os

BASE_URL = "https://150606-git.github.io/Autohaus"
OG_DEFAULT_IMAGE = f"{BASE_URL}/og-default.jpg"

MAIN_PAGES = {
    "index.html": {
        "title": "Autohaus – Vente & Export de Véhicules",
        "description": "Autohaus – Spécialiste de la vente et export de véhicules d'occasion. Berlines, SUV, utilitaires. Livraison partout en France et à l'international. Garantie 4 ans.",
        "keywords": "voiture occasion, vente véhicule, export voiture, SUV occasion, berline occasion, Autohaus",
        "og_image": OG_DEFAULT_IMAGE,
    },
    "boutique.html": {
        "title": "Galerie – Autohaus",
        "description": "Découvrez notre sélection de véhicules d'exception disponibles à la vente et à l'export. SUV, berlines, utilitaires — garantie 4 ans incluse.",
        "keywords": "galerie voitures, véhicules occasion, vente voiture, Autohaus boutique",
        "og_image": OG_DEFAULT_IMAGE,
    },
    "contact.html": {
        "title": "Contact – Autohaus",
        "description": "Contactez Autohaus – Notre équipe répond sous 24h. Téléphone, email ou formulaire de contact pour toute demande d'information sur nos véhicules.",
        "keywords": "contact Autohaus, demande information voiture, achat véhicule, export voiture France",
        "og_image": OG_DEFAULT_IMAGE,
    },
    "conditions.html": {
        "title": "Conditions d'Export – Autohaus",
        "description": "Conditions d'exportation Autohaus – Livraison, paiement, garanties, retours. Tout savoir sur notre processus d'achat et d'export de véhicules.",
        "keywords": "conditions vente, export voiture, garantie véhicule, livraison internationale, Autohaus",
        "og_image": OG_DEFAULT_IMAGE,
    },
}


def extract_text(pattern, html, group=1, default=""):
    m = re.search(pattern, html, re.DOTALL)
    return m.group(group).strip() if m else default


def build_vehicle_meta(html, filename):
    title = extract_text(r'<h1 class="vd-title">(.*?)</h1>', html)
    price = extract_text(r'<div class="vd-price">(.*?)</div>', html)
    annee = extract_text(r'<tr><th>Ann[eé]e</th><td>(.*?)</td></tr>', html)
    km = extract_text(r'<tr><th>Kilom[eé]trage</th><td>(.*?)</td></tr>', html)
    puissance = extract_text(r'<tr><th>Puissance</th><td>(.*?)</td></tr>', html)
    carburant = extract_text(r'<tr><th>Carburant</th><td>(.*?)</td></tr>', html)
    og_image = extract_text(r'<img id="vdMainImg" src="([^"]+)"', html)

    if not og_image:
        og_image = OG_DEFAULT_IMAGE

    # Build description parts
    parts = [title] if title else ["Véhicule"]
    detail_parts = []
    if annee:
        detail_parts.append(annee)
    if km:
        detail_parts.append(km)
    if puissance:
        detail_parts.append(puissance)
    if carburant:
        detail_parts.append(carburant)
    if detail_parts:
        parts.append(" — " + ", ".join(detail_parts))
    if price:
        parts.append(f". Prix : {price}")
    parts.append(". Garantie 4 ans.")

    description = "".join(parts)
    # Keep description under 160 chars
    if len(description) > 160:
        description = description[:157] + "..."

    page_title = extract_text(r'<title>(.*?)</title>', html)
    if not page_title:
        page_title = f"{title} – Autohaus" if title else "Autohaus"

    keywords_parts = []
    if title:
        keywords_parts.append(title)
    if carburant:
        keywords_parts.append(carburant.lower())
    keywords_parts += ["voiture occasion", "Autohaus", "export voiture"]
    keywords = ", ".join(keywords_parts)

    page_url = f"{BASE_URL}/{filename}"

    return {
        "title": page_title,
        "description": description,
        "keywords": keywords,
        "og_image": og_image,
        "page_url": page_url,
    }


def build_seo_block(meta, page_url=None):
    url = page_url or meta.get("page_url", BASE_URL)
    lines = [
        f'  <meta name="description" content="{meta["description"]}" />',
        f'  <meta name="keywords" content="{meta["keywords"]}" />',
        f'  <meta name="robots" content="index, follow" />',
        f'  <meta property="og:type" content="website" />',
        f'  <meta property="og:url" content="{url}" />',
        f'  <meta property="og:title" content="{meta["title"]}" />',
        f'  <meta property="og:description" content="{meta["description"]}" />',
        f'  <meta property="og:image" content="{meta["og_image"]}" />',
    ]
    return "\n".join(lines)


def inject_meta(html, seo_block):
    # Remove existing meta description, keywords, robots, og tags
    html = re.sub(r'\s*<meta name="description"[^>]*/>\n?', '', html)
    html = re.sub(r'\s*<meta name="keywords"[^>]*/>\n?', '', html)
    html = re.sub(r'\s*<meta name="robots"[^>]*/>\n?', '', html)
    html = re.sub(r'\s*<meta property="og:[^"]*"[^>]*/>\n?', '', html)

    # Insert after viewport meta tag
    html = re.sub(
        r'(<meta name="viewport"[^>]*/>)',
        r'\1\n' + seo_block + '\n',
        html,
        count=1
    )
    return html


def process_file(filepath):
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    if filename in MAIN_PAGES:
        info = MAIN_PAGES[filename]
        page_url = f"{BASE_URL}/{filename}"
        seo_block = build_seo_block(info, page_url)
    elif filename.endswith('.html'):
        meta = build_vehicle_meta(html, filename)
        seo_block = build_seo_block(meta, meta["page_url"])
    else:
        return False

    new_html = inject_meta(html, seo_block)
    if new_html != html:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        return True
    return False


def main():
    html_dir = os.path.dirname(os.path.abspath(__file__))
    files = sorted(f for f in os.listdir(html_dir) if f.endswith('.html'))

    updated = []
    skipped = []
    for filename in files:
        filepath = os.path.join(html_dir, filename)
        if process_file(filepath):
            updated.append(filename)
            print(f"  ✓ {filename}")
        else:
            skipped.append(filename)
            print(f"  - {filename} (no change)")

    print(f"\nDone: {len(updated)} updated, {len(skipped)} unchanged.")


if __name__ == "__main__":
    main()

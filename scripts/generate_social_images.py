#!/usr/bin/env python3
"""Generate unique 1200x630 social images and attach robust Open Graph metadata."""

from __future__ import annotations

import hashlib
import re
import sys
from html import unescape
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1200
HEIGHT = 630
SITE_URL = "https://quickagecalc.com"
FONT_BOLD = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
FONT_REGULAR = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")

PALETTES = [
    ((245, 248, 255), (37, 99, 235), (15, 23, 42)),
    ((250, 245, 255), (124, 58, 237), (30, 27, 75)),
    ((240, 253, 250), (13, 148, 136), (19, 78, 74)),
    ((255, 247, 237), (234, 88, 12), (124, 45, 18)),
    ((255, 241, 242), (225, 29, 72), (76, 5, 25)),
]

IMAGE_META_PATTERNS = [
    r'\s*<meta\s+property=["\']og:image(?:[:][^"\']+)?["\'][^>]*>\s*',
    r'\s*<meta\s+name=["\']twitter:image(?:[:][^"\']+)?["\'][^>]*>\s*',
    r'\s*<link\s+rel=["\']image_src["\'][^>]*>\s*',
]


def find_meta(text: str, pattern: str, default: str) -> str:
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if not match:
        return default
    return re.sub(r"\s+", " ", unescape(match.group(1))).strip()


def safe_slug(page_url: str) -> str:
    path = urlparse(page_url).path.strip("/")
    if not path:
        return "home"
    slug = re.sub(r"[^a-z0-9]+", "-", path.lower()).strip("-")
    return slug or "home"


def category_for(slug: str) -> str:
    if slug.startswith("born-in-"):
        return "AGE BY BIRTH YEAR"
    if "generation" in slug:
        return "GENERATIONS"
    if "pregnancy" in slug or "due-date" in slug:
        return "PREGNANCY & BABY"
    if "dog-age" in slug:
        return "DOG AGE"
    if "retirement" in slug:
        return "RETIREMENT"
    if "date-difference" in slug:
        return "DATE CALCULATOR"
    if "birthday" in slug:
        return "BIRTHDAY"
    return "AGE & DATE CALCULATOR"


def wrap_pixels(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=font) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def shorten_title(title: str) -> str:
    title = re.sub(r"\s*[|–—-]\s*QuickAgeCalc\s*$", "", title, flags=re.IGNORECASE)
    return title.strip() or "QuickAgeCalc"


def apply_targeted_page_updates(html_path: Path, text: str) -> str:
    """Apply reviewed, page-specific search snippet improvements during build."""
    page_updates = {
        "born-in-1964/index.html": {
            "title": "1964 to 2026 Age: 61 or 62 + Exact Calculator",
            "description": (
                "From 1964 to 2026 is 62 years. If you were born in 1964, you are 61 "
                "before your birthday and 62 after it. Calculate your exact age."
            ),
            "old_h1": "<h1>Born in 1964?<br><span>Age in 2026, Days Old &amp; Baby Boomer Facts</span></h1>",
            "new_h1": "<h1>1964 to 2026 Age:<br><span>61 or 62 Years Old</span></h1>",
            "old_intro": "<p>Exact age calculation for anyone born in 1964 — years, months, days, and hours.</p>",
            "new_intro": "<p>See the direct 1964-to-2026 answer first, then calculate your exact age from your complete birth date.</p>",
            "reviewed": "Last reviewed July 31, 2026",
        },
        "born-in-1963/index.html": {
            "title": "1963 to 2026 Age: 62 or 63 + Exact Calculator",
            "description": (
                "From 1963 to 2026 is 63 years. If you were born in 1963, you are 62 "
                "before your birthday and 63 after it. Calculate your exact age."
            ),
            "old_h1": "<h1>Born in 1963?<br><span>Age in 2026, Days Old &amp; Baby Boomer Facts</span></h1>",
            "new_h1": "<h1>1963 to 2026 Age:<br><span>62 or 63 Years Old</span></h1>",
            "old_intro": "<p>Exact age calculation for anyone born in 1963 — years, months, days, and hours.</p>",
            "new_intro": "<p>See the direct 1963-to-2026 answer first, then calculate your exact age from your complete birth date.</p>",
            "reviewed": "Last reviewed August 1, 2026",
        },
        "born-in-1960/index.html": {
            "title": "1960 to 2026 Age: 65 or 66 + Exact Calculator",
            "description": (
                "From 1960 to 2026 is 66 years. If you were born in 1960, you are 65 "
                "before your birthday and 66 after it. Calculate your exact age."
            ),
            "old_h1": "<h1>Born in 1960?<br><span>Age in 2026, Days Old &amp; Baby Boomer Facts</span></h1>",
            "new_h1": "<h1>1960 to 2026 Age:<br><span>65 or 66 Years Old</span></h1>",
            "old_intro": "<p>Exact age calculation for anyone born in 1960 — years, months, days, and hours.</p>",
            "new_intro": "<p>See the direct 1960-to-2026 answer first, then calculate your exact age from your complete birth date.</p>",
            "reviewed": "Last reviewed August 1, 2026",
        },
    }

    matched_path = next(
        (suffix for suffix in page_updates if html_path.as_posix().endswith(suffix)),
        None,
    )
    if matched_path is None:
        return text

    update = page_updates[matched_path]
    snippet_title = update["title"]
    snippet_description = update["description"]

    text = re.sub(
        r"<title>.*?</title>",
        f"<title>{snippet_title}</title>",
        text,
        count=1,
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = re.sub(
        r'<meta name="description" content=".*?">',
        f'<meta name="description" content="{snippet_description}">',
        text,
        count=1,
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = re.sub(
        r'<meta property="og:title" content=".*?">',
        f'<meta property="og:title" content="{snippet_title}">',
        text,
        count=1,
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = re.sub(
        r'<meta property="og:description" content=".*?">',
        f'<meta property="og:description" content="{snippet_description}">',
        text,
        count=1,
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = re.sub(
        r'<meta name="twitter:title" content=".*?">',
        f'<meta name="twitter:title" content="{snippet_title}">',
        text,
        count=1,
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = re.sub(
        r'<meta name="twitter:description" content=".*?">',
        f'<meta name="twitter:description" content="{snippet_description}">',
        text,
        count=1,
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = text.replace(update["old_h1"], update["new_h1"], 1)
    text = text.replace(update["old_intro"], update["new_intro"], 1)
    text = text.replace(
        '<div class="updated">Updated for 2026</div>',
        f'<div class="updated">{update["reviewed"]}</div>',
        1,
    )
    return text


def generate_card(image_path: Path, slug: str, title: str, description: str) -> None:
    palette_index = int(hashlib.sha256(slug.encode("utf-8")).hexdigest()[:2], 16) % len(PALETTES)
    background, accent, dark = PALETTES[palette_index]

    image = Image.new("RGB", (WIDTH, HEIGHT), background)
    draw = ImageDraw.Draw(image)

    light_accent = tuple((channel + 255) // 2 for channel in accent)
    draw.ellipse((850, -180, 1350, 320), fill=accent)
    draw.ellipse((930, 350, 1250, 670), fill=light_accent)
    draw.rounded_rectangle((60, 60, 1140, 570), radius=36, fill=(255, 255, 255))

    bold_path = str(FONT_BOLD if FONT_BOLD.exists() else FONT_REGULAR)
    regular_path = str(FONT_REGULAR if FONT_REGULAR.exists() else FONT_BOLD)
    brand_font = ImageFont.truetype(bold_path, 30)
    label_font = ImageFont.truetype(bold_path, 26)
    title_font = ImageFont.truetype(bold_path, 58)
    description_font = ImageFont.truetype(regular_path, 29)

    draw.text((100, 105), "QUICKAGECALC", font=brand_font, fill=accent)
    draw.text((100, 165), category_for(slug), font=label_font, fill=(100, 116, 139))

    clean_title = shorten_title(title)
    title_lines = wrap_pixels(draw, clean_title, title_font, 760)[:3]
    y = 220
    for line in title_lines:
        draw.text((100, y), line, font=title_font, fill=dark)
        y += 70

    clean_description = re.sub(r"\s+", " ", description).strip()
    description_lines = wrap_pixels(draw, clean_description, description_font, 760)[:2]
    for line in description_lines:
        draw.text((100, y + 6), line, font=description_font, fill=(71, 85, 105))
        y += 40

    image_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(image_path, format="JPEG", quality=90, optimize=True, progressive=True)


def replace_social_metadata(text: str, image_url: str, alt_text: str) -> str:
    for pattern in IMAGE_META_PATTERNS:
        text = re.sub(pattern, "\n", text, flags=re.IGNORECASE)

    escaped_alt = alt_text.replace('"', "&quot;")
    tags = f'''<meta property="og:image" content="{image_url}">
<meta property="og:image:url" content="{image_url}">
<meta property="og:image:secure_url" content="{image_url}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="{WIDTH}">
<meta property="og:image:height" content="{HEIGHT}">
<meta property="og:image:alt" content="{escaped_alt}">
<link rel="image_src" href="{image_url}">
<meta name="twitter:image" content="{image_url}">
<meta name="twitter:image:alt" content="{escaped_alt}">'''

    if "</head>" not in text:
        raise ValueError("HTML document does not contain </head>")
    return text.replace("</head>", tags + "\n</head>", 1)


def main() -> None:
    public_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "public")
    social_dir = public_dir / "social-images"
    html_files = sorted(public_dir.rglob("*.html"))

    if not html_files:
        raise SystemExit(f"No HTML files found under {public_dir}")

    generated = 0
    for html_path in html_files:
        text = html_path.read_text(encoding="utf-8")
        text = apply_targeted_page_updates(html_path, text)
        title = find_meta(text, r"<title>(.*?)</title>", "QuickAgeCalc")
        description = find_meta(
            text,
            r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\'][^>]*>',
            "Free online age and date calculators.",
        )
        page_url = find_meta(
            text,
            r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\'][^>]*>',
            SITE_URL + "/",
        )

        slug = safe_slug(page_url)
        image_path = social_dir / f"{slug}.jpg"
        image_url = f"{SITE_URL}/social-images/{slug}.jpg"
        alt_text = f"QuickAgeCalc social preview: {shorten_title(title)}"

        generate_card(image_path, slug, title, description)
        text = replace_social_metadata(text, image_url, alt_text)
        html_path.write_text(text, encoding="utf-8")
        generated += 1

        if slug == "home":
            (public_dir / "social-card.jpg").write_bytes(image_path.read_bytes())

    print(f"Generated {generated} unique 1200x630 social images.")


if __name__ == "__main__":
    main()

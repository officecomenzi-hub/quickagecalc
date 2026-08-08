#!/usr/bin/env python3
"""Run the social-image build and add static internal links to age and birth-year pages."""

from __future__ import annotations

import sys
from pathlib import Path

import generate_social_images_core as core


DECADE_HUBS = ("1960s", "1970s", "1980s", "1990s", "2000s")

STATIC_CONTEXT_STYLE = '''<style id="qac-static-context-style">
.qac-static-context h2,.qac-decade-navigation h2{font-family:'Playfair Display',serif;font-size:1.35rem;margin-bottom:8px}
.qac-static-context>p,.qac-decade-navigation>p{font-size:14px;line-height:1.65;color:#6b7280;margin-bottom:14px}
.qac-static-context-grid,.qac-decade-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.qac-static-context-grid a,.qac-decade-grid a{display:block;border:1px solid #e2e6ea;border-radius:10px;padding:14px;text-decoration:none;color:#1a202c;background:#f7f8fa}
.qac-static-context-grid a:hover,.qac-decade-grid a:hover,.qac-decade-grid a.active{border-color:#2563eb;background:#eff6ff}
.qac-static-context-grid strong,.qac-decade-grid strong{display:block;font-size:14px;margin-bottom:4px}
.qac-static-context-grid span,.qac-decade-grid span{display:block;font-size:12px;line-height:1.5;color:#6b7280}
@media(max-width:540px){.qac-static-context-grid,.qac-decade-grid{grid-template-columns:1fr}}
</style>'''


def generation_for_year(birth_year: int) -> str:
    """Return the generation label already used by QuickAgeCalc birth-year pages."""
    if birth_year <= 1964:
        return "Baby Boomer"
    if birth_year <= 1980:
        return "Generation X"
    if birth_year <= 1996:
        return "Millennial"
    if birth_year <= 2012:
        return "Generation Z"
    return "Generation Alpha"


def primary_context_link(decade_start: int) -> tuple[str, str, str]:
    """Return an existing crawlable hub link for the birth-year decade."""
    if decade_start <= 2000:
        decade_label = f"{decade_start}s"
        return (
            f"/born-in-the-{decade_label}/",
            f"{decade_label} Age Guide",
            f"Compare ages in 2026 for every birth year from {decade_start} to {decade_start + 9}.",
        )

    return (
        "/born-in-year/",
        "Age by Birth Year",
        "Browse birth-year age pages and open another exact age calculator.",
    )


def ensure_static_style(text: str, html_path: Path) -> str:
    """Ensure build-added internal-link sections have crawl-independent styling."""
    if 'id="qac-static-context-style"' in text:
        return text
    if "</head>" not in text:
        raise ValueError(f"{html_path} does not contain </head>")
    return text.replace("</head>", STATIC_CONTEXT_STYLE + "\n</head>", 1)


def add_static_contextual_links(public_dir: Path) -> dict[str, int]:
    """Add crawlable contextual links to supported 1960-2026 birth-year pages after the main build."""
    updated_by_decade: dict[str, int] = {}

    for decade_start in (1960, 1970, 1980, 1990, 2000, 2010, 2020):
        decade_label = f"{decade_start}s"
        decade_end = min(decade_start + 9, 2026)
        updated = 0
        primary_href, primary_label, primary_description = primary_context_link(decade_start)

        for birth_year in range(decade_start, decade_end + 1):
            html_path = public_dir / f"born-in-{birth_year}" / "index.html"
            if not html_path.exists():
                raise FileNotFoundError(f"Expected birth-year page is missing: {html_path}")

            text = html_path.read_text(encoding="utf-8")
            if 'id="qac-contextual-tools"' in text:
                continue

            generation_label = generation_for_year(birth_year)
            section = f'''<section id="qac-contextual-tools" class="card qac-static-context" aria-labelledby="qac-contextual-tools-title">
    <h2 id="qac-contextual-tools-title">Explore More About Your Age</h2>
    <p>Use these related pages to compare birth years, check another year, and confirm your generation.</p>
    <div class="qac-static-context-grid">
      <a href="{primary_href}"><strong>{primary_label}</strong><span>{primary_description}</span></a>
      <a href="/age-in-any-year/"><strong>Age in Any Year</strong><span>See how old someone born in {birth_year} was or will be in any year.</span></a>
      <a href="/what-generation-am-i/"><strong>What Generation Am I?</strong><span>Confirm the {generation_label} range and nearby cutoff years.</span></a>
      <a href="/age-questions/"><strong>Age Questions &amp; Answers</strong><span>Find quick answers and the best calculator for common age questions.</span></a>
    </div>
  </section>'''

            text = ensure_static_style(text, html_path)

            marker = '<div class="card content">'
            if marker not in text:
                raise ValueError(f"{html_path} does not contain the expected content card")

            text = text.replace(marker, section + "\n\n  " + marker, 1)
            html_path.write_text(text, encoding="utf-8")
            updated += 1

        updated_by_decade[decade_label] = updated

    return updated_by_decade


def decade_navigation_section(active_decade: str | None) -> str:
    """Build static decade navigation matching the existing JavaScript fallback."""
    if active_decade:
        intro = "Compare this decade with nearby birth-year guides and open the central age-by-year index."
    else:
        intro = "Open a decade guide to compare ages in 2026 and reach every individual birth-year calculator."

    links = []
    for decade in DECADE_HUBS:
        active_class = ' class="active"' if decade == active_decade else ""
        links.append(
            f'<a href="/born-in-the-{decade}/"{active_class}><strong>{decade}</strong>'
            '<span>Age by year and generation</span></a>'
        )
    links.append('<a href="/born-in-year/"><strong>All years</strong><span>1960 through 2026</span></a>')

    return f'''<section id="qac-decade-navigation" class="card qac-decade-navigation" aria-labelledby="qac-decade-navigation-title">
    <h2 id="qac-decade-navigation-title">Browse Birth-Year Decades</h2>
    <p>{intro}</p>
    <div class="qac-decade-grid">{''.join(links)}</div>
  </section>'''


def add_static_decade_navigation(public_dir: Path) -> dict[str, int]:
    """Make decade-hub navigation crawlable without depending on JavaScript rendering."""
    targets: list[tuple[Path, str | None]] = [
        (public_dir / "born-in-year" / "index.html", None),
        *[
            (public_dir / f"born-in-the-{decade}" / "index.html", decade)
            for decade in DECADE_HUBS
        ],
    ]
    updated: dict[str, int] = {}

    for html_path, active_decade in targets:
        label = active_decade or "born-in-year"
        if not html_path.exists():
            raise FileNotFoundError(f"Expected decade navigation target is missing: {html_path}")

        text = html_path.read_text(encoding="utf-8")
        if 'id="qac-decade-navigation"' in text:
            updated[label] = 0
            continue

        section = decade_navigation_section(active_decade)
        text = ensure_static_style(text, html_path)

        insertion_markers = (
            '<section class="card quick">',
            '<div class="quick-answer">',
            '<div class="ad-slot">',
            '<div class="card">',
        )
        marker = next((candidate for candidate in insertion_markers if candidate in text), None)
        if marker is None:
            raise ValueError(f"{html_path} does not contain a safe decade-navigation insertion marker")

        text = text.replace(marker, section + "\n\n  " + marker, 1)
        html_path.write_text(text, encoding="utf-8")
        updated[label] = 1

    return updated


def main() -> None:
    core.main()
    public_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "public")
    updated_by_decade = add_static_contextual_links(public_dir)
    decade_navigation_updates = add_static_decade_navigation(public_dir)
    summary = ", ".join(
        f"{count} {decade} pages" for decade, count in updated_by_decade.items()
    )
    nav_count = sum(decade_navigation_updates.values())
    print(f"Added static contextual links to {summary}.")
    print(f"Added static decade navigation to {nav_count} hub/index pages.")


if __name__ == "__main__":
    main()

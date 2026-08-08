#!/usr/bin/env python3
"""Run the social-image build and add static contextual links to birth-year pages."""

from __future__ import annotations

import sys
from pathlib import Path

import generate_social_images_core as core


STATIC_CONTEXT_STYLE = '''<style id="qac-static-context-style">
.qac-static-context h2{font-family:'Playfair Display',serif;font-size:1.35rem;margin-bottom:8px}
.qac-static-context>p{font-size:14px;line-height:1.65;color:#6b7280;margin-bottom:14px}
.qac-static-context-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.qac-static-context-grid a{display:block;border:1px solid #e2e6ea;border-radius:10px;padding:14px;text-decoration:none;color:#1a202c;background:#f7f8fa}
.qac-static-context-grid a:hover{border-color:#2563eb;background:#eff6ff}
.qac-static-context-grid strong{display:block;font-size:14px;margin-bottom:4px}
.qac-static-context-grid span{display:block;font-size:12px;line-height:1.5;color:#6b7280}
@media(max-width:540px){.qac-static-context-grid{grid-template-columns:1fr}}
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

            if 'id="qac-static-context-style"' not in text:
                if "</head>" not in text:
                    raise ValueError(f"{html_path} does not contain </head>")
                text = text.replace("</head>", STATIC_CONTEXT_STYLE + "\n</head>", 1)

            marker = '<div class="card content">'
            if marker not in text:
                raise ValueError(f"{html_path} does not contain the expected content card")

            text = text.replace(marker, section + "\n\n  " + marker, 1)
            html_path.write_text(text, encoding="utf-8")
            updated += 1

        updated_by_decade[decade_label] = updated

    return updated_by_decade


def main() -> None:
    core.main()
    public_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "public")
    updated_by_decade = add_static_contextual_links(public_dir)
    summary = ", ".join(
        f"{count} {decade} pages" for decade, count in updated_by_decade.items()
    )
    print(f"Added static contextual links to {summary}.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Run the social-image build and add static enhancements to QuickAgeCalc pages."""

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

COPY_RESULT_STYLE = '''<style id="qac-copy-result-style">
.qac-copy-result{width:100%;margin-top:14px;padding:12px 16px;border:1.5px solid #2563eb;border-radius:9px;background:#fff;color:#2563eb;font:700 14px 'Lato',sans-serif;cursor:pointer;transition:background .2s,color .2s}
.qac-copy-result:hover{background:#2563eb;color:#fff}
.qac-copy-status{min-height:18px;margin-top:7px;text-align:center;font-size:12px;color:#6b7280}
</style>'''

COPY_RESULT_SCRIPT = '''function fallbackCopyAgeResult(text) {
  var area = document.createElement('textarea');
  area.value = text;
  area.setAttribute('readonly', '');
  area.style.position = 'fixed';
  area.style.opacity = '0';
  document.body.appendChild(area);
  area.select();
  var copied = false;
  try { copied = document.execCommand('copy'); } catch (e) { copied = false; }
  document.body.removeChild(area);
  return copied;
}

function copyAgeResult() {
  var years = document.getElementById('ageYears').textContent;
  var status = document.getElementById('qac-copy-status');
  if (!years || years === '—') {
    status.textContent = 'Calculate your exact age first.';
    return;
  }
  var monthSelect = document.getElementById('bMonth');
  var month = monthSelect.options[monthSelect.selectedIndex].text;
  var day = document.getElementById('bDay').value;
  var year = document.getElementById('bYear').value;
  var resultUrl = window.location.origin + window.location.pathname;
  var resultText = 'Born on ' + month + ' ' + day + ', ' + year + ': ' + years +
    ' years old today · ' + document.getElementById('rMonths').textContent + ' total months · ' +
    document.getElementById('rWeeks').textContent + ' total weeks · ' +
    document.getElementById('rDays').textContent + ' total days. Calculated with QuickAgeCalc: ' + resultUrl;
  function showCopied(ok) {
    status.textContent = ok ? 'Result copied to clipboard.' : 'Copy failed. Please select and copy the result manually.';
  }
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(resultText).then(function(){ showCopied(true); }).catch(function(){ showCopied(fallbackCopyAgeResult(resultText)); });
  } else {
    showCopied(fallbackCopyAgeResult(resultText));
  }
}'''

COPY_COUNTDOWN_STYLE = '''<style id="qac-copy-countdown-style">
.qac-copy-countdown{width:100%;margin-top:4px;padding:12px 16px;border:1.5px solid #2563eb;border-radius:9px;background:#fff;color:#2563eb;font:700 14px 'Lato',sans-serif;cursor:pointer;transition:background .2s,color .2s}
.qac-copy-countdown:hover{background:#2563eb;color:#fff}
.qac-copy-countdown-status{min-height:18px;margin-top:7px;text-align:center;font-size:12px;color:#6b7280}
</style>'''

COPY_COUNTDOWN_SCRIPT = '''function fallbackCopyCountdown(text) {
  var area = document.createElement('textarea');
  area.value = text;
  area.setAttribute('readonly', '');
  area.style.position = 'fixed';
  area.style.opacity = '0';
  document.body.appendChild(area);
  area.select();
  var copied = false;
  try { copied = document.execCommand('copy'); } catch (e) { copied = false; }
  document.body.removeChild(area);
  return copied;
}

function copyBirthdayCountdown() {
  var days = document.getElementById('daysLeft').textContent;
  var status = document.getElementById('qac-copy-countdown-status');
  if (!days || days === '—') {
    status.textContent = 'Calculate your birthday countdown first.';
    return;
  }
  var resultUrl = window.location.origin + window.location.pathname;
  var resultText = days + ' days until my next birthday · ' +
    document.getElementById('nextBdDate').textContent + ' · turning ' +
    document.getElementById('rAge').textContent + '. Calculated with QuickAgeCalc: ' + resultUrl;
  function showCopied(ok) {
    status.textContent = ok ? 'Countdown copied to clipboard.' : 'Copy failed. Please select and copy the countdown manually.';
  }
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(resultText).then(function(){ showCopied(true); }).catch(function(){ showCopied(fallbackCopyCountdown(resultText)); });
  } else {
    showCopied(fallbackCopyCountdown(resultText));
  }
}'''


def generation_for_year(birth_year: int) -> str:
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


def add_copy_result_to_birth_years(public_dir: Path, birth_years: tuple[int, ...]) -> dict[int, bool]:
    results: dict[int, bool] = {}
    for birth_year in birth_years:
        html_path = public_dir / f"born-in-{birth_year}" / "index.html"
        if not html_path.exists():
            raise FileNotFoundError(f"Expected {birth_year} page is missing: {html_path}")
        text = html_path.read_text(encoding="utf-8")
        if 'id="qac-copy-result"' in text:
            results[birth_year] = False
            continue
        if 'id="qac-copy-result-style"' not in text:
            if "</head>" not in text:
                raise ValueError(f"{html_path} does not contain </head>")
            text = text.replace("</head>", COPY_RESULT_STYLE + "\n</head>", 1)
        results_marker = '''      <div class="stat-box"><span class="stat-val" id="rSeconds">—</span><div class="stat-lbl">Seconds</div></div>
    </div>
  </div>'''
        results_replacement = '''      <div class="stat-box"><span class="stat-val" id="rSeconds">—</span><div class="stat-lbl">Seconds</div></div>
    </div>
    <button type="button" id="qac-copy-result" class="qac-copy-result" onclick="copyAgeResult()">Copy Result</button>
    <div id="qac-copy-status" class="qac-copy-status" aria-live="polite"></div>
  </div>'''
        if results_marker not in text:
            raise ValueError(f"{html_path} does not contain the expected result grid")
        text = text.replace(results_marker, results_replacement, 1)
        script_marker = "function toggleFaq(el){el.closest('.faq-item').classList.toggle('open');}"
        if script_marker not in text:
            raise ValueError(f"{html_path} does not contain the expected FAQ script marker")
        text = text.replace(script_marker, COPY_RESULT_SCRIPT + "\n\n" + script_marker, 1)
        html_path.write_text(text, encoding="utf-8")
        results[birth_year] = True
    return results


def enhance_1967_page(public_dir: Path) -> bool:
    html_path = public_dir / "born-in-1967" / "index.html"
    text = html_path.read_text(encoding="utf-8")
    old = text
    title = "1967 to 2026 Age: 58 or 59 + Exact Calculator"
    description = "From 1967 to 2026 is 59 years. If you were born in 1967, you are 58 before your birthday and 59 after it. Calculate your exact age and see Gen X milestones."
    replacements = {
        '<title>Born in 1967? Age in 2026, Days Old &amp; Gen X Facts</title>': f'<title>{title}</title>',
        '<meta name="description" content="Born in 1967? Find your exact age in 2026 — years, months, days and hours — plus Gen X facts, key milestones and age by birth month. Free age calculator.">': f'<meta name="description" content="{description}">',
        '<meta property="og:title" content="Born in 1967? Age in 2026, Days Old &amp; Gen X Facts">': f'<meta property="og:title" content="{title}">',
        '<meta property="og:description" content="Find your exact age in 2026 if you were born in 1967 — years, months, days, hours — plus Gen X facts and milestones.">': f'<meta property="og:description" content="{description}">',
        '<meta name="twitter:title" content="Born in 1967? Age in 2026, Days Old &amp; Gen X Facts">': f'<meta name="twitter:title" content="{title}">',
        '<meta name="twitter:description" content="Your exact age in 2026 if born in 1967, plus Gen X facts and milestones. Free calculator.">': f'<meta name="twitter:description" content="{description}">',
        '<h1>Born in 1967?<br><span>Age in 2026, Days Old &amp; Gen X Facts</span></h1>': '<h1>1967 to 2026 Age:<br><span>58 or 59 Years Old</span></h1>',
        '<p>Exact age calculation for anyone born in 1967 — years, months, days, and hours.</p>': '<p>See the direct 1967-to-2026 answer first, then calculate your exact age from your complete birth date.</p>',
        '<div class="updated">Updated for 2026</div>': '<div class="updated">Last reviewed August 9, 2026</div>',
        '<li><span>Age in 2026</span><span>59</span></li>': '<li><span>Age in 2026</span><span>58 or 59</span></li>',
        '<li><span>Age in 2032</span><span>65 · retirement age</span></li>': '<li><span>Turns 65</span><span>2032</span></li>',
        '<p>Someone born in 1967 reaches <strong>65 in 2032</strong> and 67 in 2034. Full retirement age is 66–67 in most countries (67 in the US, UK, Australia and Germany; 65 in Canada). Use the <a href="/retirement-calculator/">retirement calculator</a> to find your exact pensionable age and retirement date by country.</p>': '<p>Someone born in 1967 reaches <strong>65 in 2032</strong> and 67 in 2034. State-pension or Social Security eligibility depends on your country, date of birth, contribution record, and program rules. Use the <a href="/retirement-calculator/">retirement calculator</a> for a country reference, then confirm eligibility with the relevant official authority.</p>',
        '<a class="tool-card" href="/born-in-year/"><span class="tc-icon">👥</span><div class="tc-name">What Generation Am I?</div><div class="tc-desc">Find your generation</div></a>': '<a class="tool-card" href="/what-generation-am-i/"><span class="tc-icon">👥</span><div class="tc-name">What Generation Am I?</div><div class="tc-desc">Find your generation</div></a>',
    }
    for source, target in replacements.items():
        if source not in text:
            raise ValueError(f"1967 page is missing expected text: {source[:80]}")
        text = text.replace(source, target, 1)
    old_retirement = "Most countries set full retirement between 65 and 67. Someone born in 1967 turns 65 in 2032. Check your exact pensionable age and retirement date with the retirement calculator."
    new_retirement = "Someone born in 1967 turns 65 in 2032 and 67 in 2034. Pension or Social Security eligibility varies by country, date of birth, contribution record, and program rules, so use the retirement calculator as a reference and confirm with the relevant official authority."
    if old_retirement not in text:
        raise ValueError("1967 retirement FAQ text was not found")
    text = text.replace(old_retirement, new_retirement)
    html_path.write_text(text, encoding="utf-8")
    return text != old


def enhance_birthday_countdown(public_dir: Path) -> bool:
    html_path = public_dir / "birthday-countdown" / "index.html"
    text = html_path.read_text(encoding="utf-8")
    old = text
    if 'id="qac-copy-countdown-style"' not in text:
        text = text.replace("</head>", COPY_COUNTDOWN_STYLE + "\n</head>", 1)
    zodiac_marker = '''    <div class="zodiac-box">
      <div class="z-sign" id="zodiacSign">—</div>
      <div class="z-label" id="zodiacLabel">—</div>
    </div>
  </div>'''
    zodiac_replacement = '''    <div class="zodiac-box">
      <div class="z-sign" id="zodiacSign">—</div>
      <div class="z-label" id="zodiacLabel">—</div>
    </div>
    <button type="button" id="qac-copy-countdown" class="qac-copy-countdown" onclick="copyBirthdayCountdown()">Copy Countdown</button>
    <div id="qac-copy-countdown-status" class="qac-copy-countdown-status" aria-live="polite"></div>
  </div>'''
    if zodiac_marker not in text:
        raise ValueError("Birthday Countdown result marker was not found")
    text = text.replace(zodiac_marker, zodiac_replacement, 1)
    replacements = {
        'For example, if your birthday is July 15 and today is May 24, 2026, your birthday is 51 days away. If your birthday was March 10, it already passed — your next birthday is March 10, 2027, which is 290 days away.': 'For example, if the next occurrence of your birthday is 30 calendar days from today, the countdown is 30 days. If this year’s birthday has already passed, the calculator automatically uses the same month and day in the following year.',
        'What Day of the Week Is My Birthday This Year?': 'What Day of the Week Is My Next Birthday?',
        'Your birthday falls on a different day of the week each year. Birthdays shift forward by 1 day each year, and by 2 days after a leap year. The calculator above shows you exactly what day of the week your birthday falls on in 2026.': 'Your birthday falls on a different weekday from year to year. The calculator uses the next occurrence of your birthday, so if this year’s date has already passed it shows the weekday for next year instead.',
        '<h2>How Many Days Until My Birthday — By Month</h2>\n    <p>Approximate days until upcoming birthdays from late May 2026:</p>\n    <ul>\n      <li>June birthday: approximately 7 to 37 days away</li>\n      <li>July birthday: approximately 38 to 68 days away</li>\n      <li>August birthday: approximately 69 to 99 days away</li>\n      <li>September birthday: approximately 100 to 129 days away</li>\n      <li>December birthday: approximately 191 to 221 days away</li>\n    </ul>': '<h2>Why the Birthday Countdown Changes Every Day</h2>\n    <p>The number of days remaining changes at midnight as the calendar moves forward. Your birth year is used to calculate the age you will turn, while your birth month and day determine the next birthday date.</p>\n    <ul>\n      <li>If your birthday is still ahead this year, the countdown ends on this year’s birthday.</li>\n      <li>If it has already passed, the countdown automatically rolls forward to next year.</li>\n      <li>The result also shows weeks away, hours away, the weekday, and the age you will turn.</li>\n    </ul>',
        'Your Zodiac sign is determined by your birthday. The calculator above shows your sign automatically. Birthdays in late May fall under Gemini (May 21 to June 20). Each sign has different date ranges that shift slightly depending on the exact time of year.': 'Your Zodiac sign is determined by your birth month and day. The calculator displays the corresponding sign alongside your countdown so the result stays useful without relying on a particular month of the year.',
        '<h2>The Most Common Birthday Month</h2>\n    <p>September is statistically the most common birth month globally. The most common single birthday in the United States is September 9. The least common birthday is February 29, which only exists in leap years — meaning people born on that date only have a real birthday every 4 years.</p>': '<h2>Leap Day Birthdays</h2>\n    <p>February 29 only appears in leap years. If you were born on leap day, your legal or customary birthday treatment in non-leap years can vary by jurisdiction and personal convention, so use the countdown as a calendar tool rather than legal guidance.</p>',
        'How many days until my birthday if I was born in July?': 'What happens if my birthday already passed this year?',
        'If you were born in July and today is late May 2026, your birthday is approximately 38 to 68 days away depending on your exact birth date. Enter your date above for the precise countdown.': 'The calculator automatically moves to the same month and day next year, so the result always counts down to your next birthday.',
        'What day of the week is my birthday this year?': 'What day of the week is my next birthday?',
        'Enter your birth date in the calculator above. It will show you exactly what day of the week your birthday falls on in 2026, along with your Zodiac sign.': 'Enter your birth date in the calculator above. It will show the weekday for your next birthday, along with your Zodiac sign.',
        'If you were born in July and today is late May 2026, your birthday is approximately 30-60 days away. Enter your exact birth date above for a precise countdown.': 'If your birthday has already passed this year, the calculator automatically counts down to the same month and day next year.',
    }
    for source, target in replacements.items():
        if source in text:
            text = text.replace(source, target, 1)
    script_marker = "function toggleFaq(el){el.closest('.faq-item').classList.toggle('open');}"
    if script_marker not in text:
        raise ValueError("Birthday Countdown FAQ script marker was not found")
    text = text.replace(script_marker, COPY_COUNTDOWN_SCRIPT + "\n\n" + script_marker, 1)
    html_path.write_text(text, encoding="utf-8")
    return text != old


def enhance_pregnancy_page(public_dir: Path) -> bool:
    html_path = public_dir / "pregnancy-due-date" / "index.html"
    text = html_path.read_text(encoding="utf-8")
    old = text
    if 'id="qac-how-far-along"' not in text:
        marker = '<h2>How is the Due Date Calculated?</h2>'
        if marker not in text:
            raise ValueError("Pregnancy methodology heading was not found")
        block = '''<h2 id="qac-how-far-along">How Far Along Am I?</h2>
    <p>When you calculate from your last menstrual period, gestational age is counted from the first day of that period. The result above shows your estimated weeks pregnant and trimester alongside the due date. If your dates are uncertain, your cycles are irregular, or an ultrasound gives different dating, follow the estimate confirmed by your healthcare provider.</p>

    '''
        text = text.replace(marker, block + marker, 1)
    html_path.write_text(text, encoding="utf-8")
    return text != old


def enhance_birth_year_hub(public_dir: Path) -> bool:
    html_path = public_dir / "born-in-year" / "index.html"
    text = html_path.read_text(encoding="utf-8")
    old = text
    if 'id="qac-featured-birth-years"' not in text:
        marker = '<div class="ad-slot">Advertisement (728×90)</div>'
        if marker not in text:
            raise ValueError("Birth-year hub advertisement marker was not found")
        featured = '''<section id="qac-featured-birth-years" class="card" aria-labelledby="qac-featured-birth-years-title">
    <h2 id="qac-featured-birth-years-title" style="font-family:'Playfair Display',serif;font-size:1.35rem;margin-bottom:8px;">Featured Birth-Year Guides</h2>
    <p style="font-size:14px;color:var(--muted);line-height:1.6;margin-bottom:14px;">Start with birth-year pages that answer common generation, milestone, and age questions in more detail.</p>
    <div class="years-grid" style="margin-bottom:0;">
      <a class="year-link" href="/born-in-1965/"><span class="yl-year">1965</span><span class="yl-age">Gen X starting-year guide</span><span class="yl-gen gen-x">Gen X</span></a>
      <a class="year-link" href="/born-in-1967/"><span class="yl-year">1967</span><span class="yl-age">Age timeline &amp; milestones</span><span class="yl-gen gen-x">Gen X</span></a>
      <a class="year-link" href="/born-in-1999/"><span class="yl-year">1999</span><span class="yl-age">Generation cutoff guide</span><span class="yl-gen gen-z">Gen Z</span></a>
      <a class="year-link" href="/born-in-2000/"><span class="yl-year">2000</span><span class="yl-age">Age &amp; generation guide</span><span class="yl-gen gen-z">Gen Z</span></a>
    </div>
  </section>'''
        text = text.replace(marker, marker + "\n\n  " + featured, 1)
    html_path.write_text(text, encoding="utf-8")
    return text != old


def apply_analytics_priority_enhancements(public_dir: Path) -> dict[str, bool]:
    return {
        "born-in-1967": enhance_1967_page(public_dir),
        "birthday-countdown": enhance_birthday_countdown(public_dir),
        "pregnancy-due-date": enhance_pregnancy_page(public_dir),
        "born-in-year": enhance_birth_year_hub(public_dir),
    }


def main() -> None:
    public_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "public")
    priority_updates = apply_analytics_priority_enhancements(public_dir)
    core.main()
    updated_by_decade = add_static_contextual_links(public_dir)
    copy_results = add_copy_result_to_birth_years(public_dir, tuple(range(1961, 1990)))
    priority_summary = ", ".join(f"{page}: {'updated' if changed else 'unchanged'}" for page, changed in priority_updates.items())
    print(f"Analytics-priority enhancements: {priority_summary}.")
    summary = ", ".join(f"{count} {decade} pages" for decade, count in updated_by_decade.items())
    print(f"Added static contextual links to {summary}.")
    copy_summary = ", ".join(f"{year}: {'added' if added else 'already present'}" for year, added in copy_results.items())
    print(f"Copy-result controls: {copy_summary}.")


if __name__ == "__main__":
    main()

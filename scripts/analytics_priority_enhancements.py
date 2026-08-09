#!/usr/bin/env python3
"""Apply data-led content and UX enhancements to selected built pages."""

from __future__ import annotations

from pathlib import Path


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


def _replace_once(text: str, source: str, target: str) -> str:
    return text.replace(source, target, 1) if source in text else text


def enhance_1967_page(public_dir: Path) -> bool:
    html_path = public_dir / "born-in-1967" / "index.html"
    text = html_path.read_text(encoding="utf-8")
    old = text
    title = "1967 to 2026 Age: 58 or 59 + Exact Calculator"
    description = "From 1967 to 2026 is 59 years. If you were born in 1967, you are 58 before your birthday and 59 after it. Calculate your exact age and see Gen X milestones."

    replacements = (
        ('<title>Born in 1967? Age in 2026, Days Old &amp; Gen X Facts</title>', f'<title>{title}</title>'),
        ('<meta name="description" content="Born in 1967? Find your exact age in 2026 — years, months, days and hours — plus Gen X facts, key milestones and age by birth month. Free age calculator.">', f'<meta name="description" content="{description}">'),
        ('<meta property="og:title" content="Born in 1967? Age in 2026, Days Old &amp; Gen X Facts">', f'<meta property="og:title" content="{title}">'),
        ('<meta property="og:description" content="Find your exact age in 2026 if you were born in 1967 — years, months, days, hours — plus Gen X facts and milestones.">', f'<meta property="og:description" content="{description}">'),
        ('<meta name="twitter:title" content="Born in 1967? Age in 2026, Days Old &amp; Gen X Facts">', f'<meta name="twitter:title" content="{title}">'),
        ('<meta name="twitter:description" content="Your exact age in 2026 if born in 1967, plus Gen X facts and milestones. Free calculator.">', f'<meta name="twitter:description" content="{description}">'),
        ('<h1>Born in 1967?<br><span>Age in 2026, Days Old &amp; Gen X Facts</span></h1>', '<h1>1967 to 2026 Age:<br><span>58 or 59 Years Old</span></h1>'),
        ('<p>Exact age calculation for anyone born in 1967 — years, months, days, and hours.</p>', '<p>See the direct 1967-to-2026 answer first, then calculate your exact age from your complete birth date.</p>'),
        ('<div class="updated">Updated for 2026</div>', '<div class="updated">Last reviewed August 9, 2026</div>'),
        ('<li><span>Age in 2026</span><span>59</span></li>', '<li><span>Age in 2026</span><span>58 or 59</span></li>'),
        ('<li><span>Age in 2032</span><span>65 · retirement age</span></li>', '<li><span>Turns 65</span><span>2032</span></li>'),
        ('<p>Someone born in 1967 reaches <strong>65 in 2032</strong> and 67 in 2034. Full retirement age is 66–67 in most countries (67 in the US, UK, Australia and Germany; 65 in Canada). Use the <a href="/retirement-calculator/">retirement calculator</a> to find your exact pensionable age and retirement date by country.</p>', '<p>Someone born in 1967 reaches <strong>65 in 2032</strong> and 67 in 2034. State-pension or Social Security eligibility depends on your country, date of birth, contribution record, and program rules. Use the <a href="/retirement-calculator/">retirement calculator</a> for a country reference, then confirm eligibility with the relevant official authority.</p>'),
        ('<a class="tool-card" href="/born-in-year/"><span class="tc-icon">👥</span><div class="tc-name">What Generation Am I?</div><div class="tc-desc">Find your generation</div></a>', '<a class="tool-card" href="/what-generation-am-i/"><span class="tc-icon">👥</span><div class="tc-name">What Generation Am I?</div><div class="tc-desc">Find your generation</div></a>'),
    )
    for source, target in replacements:
        text = _replace_once(text, source, target)

    old_retirement = "Most countries set full retirement between 65 and 67. Someone born in 1967 turns 65 in 2032. Check your exact pensionable age and retirement date with the retirement calculator."
    new_retirement = "Someone born in 1967 turns 65 in 2032 and 67 in 2034. Pension or Social Security eligibility varies by country, date of birth, contribution record, and program rules, so use the retirement calculator as a reference and confirm with the relevant official authority."
    text = text.replace(old_retirement, new_retirement)

    required = (title, "58 or 59</span></li>", "/what-generation-am-i/", "State-pension or Social Security eligibility")
    if not all(item in text for item in required):
        raise ValueError("1967 priority enhancement did not produce the expected output")

    html_path.write_text(text, encoding="utf-8")
    return text != old


def enhance_birthday_countdown(public_dir: Path) -> bool:
    html_path = public_dir / "birthday-countdown" / "index.html"
    text = html_path.read_text(encoding="utf-8")
    old = text

    if 'id="qac-copy-countdown-style"' not in text:
        if "</head>" not in text:
            raise ValueError("Birthday Countdown page is missing </head>")
        text = text.replace("</head>", COPY_COUNTDOWN_STYLE + "\n</head>", 1)

    if 'id="qac-copy-countdown"' not in text:
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
            raise ValueError("Birthday Countdown page is missing the result zodiac marker")
        text = text.replace(zodiac_marker, zodiac_replacement, 1)

    replacements = (
        ('For example, if your birthday is July 15 and today is May 24, 2026, your birthday is 51 days away. If your birthday was March 10, it already passed — your next birthday is March 10, 2027, which is 290 days away.', 'For example, if the next occurrence of your birthday is 30 calendar days from today, the countdown is 30 days. If this year’s birthday has already passed, the calculator automatically uses the same month and day in the following year.'),
        ('What day of the week is my birthday this year?', 'What day of the week is my next birthday?'),
        ('What Day of the Week Is My Birthday This Year?', 'What Day of the Week Is My Next Birthday?'),
        ('Enter your birth date in the calculator above to see what day of the week your birthday falls on this year.', 'Enter your birth date in the calculator above to see the weekday of your next birthday.'),
        ('Your birthday falls on a different day of the week each year. Birthdays shift forward by 1 day each year, and by 2 days after a leap year. The calculator above shows you exactly what day of the week your birthday falls on in 2026.', 'Your birthday falls on a different weekday from year to year. The calculator uses the next occurrence of your birthday, so if this year’s date has already passed it shows the weekday for next year instead.'),
        ('<h2>How Many Days Until My Birthday — By Month</h2>\n    <p>Approximate days until upcoming birthdays from late May 2026:</p>\n    <ul>\n      <li>June birthday: approximately 7 to 37 days away</li>\n      <li>July birthday: approximately 38 to 68 days away</li>\n      <li>August birthday: approximately 69 to 99 days away</li>\n      <li>September birthday: approximately 100 to 129 days away</li>\n      <li>December birthday: approximately 191 to 221 days away</li>\n    </ul>', '<h2>Why the Birthday Countdown Changes Every Day</h2>\n    <p>The number of days remaining changes at midnight as the calendar moves forward. Your birth year is used to calculate the age you will turn, while your birth month and day determine the next birthday date.</p>\n    <ul>\n      <li>If your birthday is still ahead this year, the countdown ends on this year’s birthday.</li>\n      <li>If it has already passed, the countdown automatically rolls forward to next year.</li>\n      <li>The result also shows weeks away, hours away, the weekday, and the age you will turn.</li>\n    </ul>'),
        ('Your Zodiac sign is determined by your birthday. The calculator above shows your sign automatically. Birthdays in late May fall under Gemini (May 21 to June 20). Each sign has different date ranges that shift slightly depending on the exact time of year.', 'Your Zodiac sign is determined by your birth month and day. The calculator displays the corresponding sign alongside your countdown so the result stays useful without relying on a particular month of the year.'),
        ('<h2>The Most Common Birthday Month</h2>\n    <p>September is statistically the most common birth month globally. The most common single birthday in the United States is September 9. The least common birthday is February 29, which only exists in leap years — meaning people born on that date only have a real birthday every 4 years.</p>', '<h2>Leap Day Birthdays</h2>\n    <p>February 29 only appears in leap years. If you were born on leap day, legal or customary treatment in non-leap years can vary by jurisdiction and personal convention, so use the countdown as a calendar tool rather than legal guidance.</p>'),
        ('How many days until my birthday if I was born in July?', 'What happens if my birthday already passed this year?'),
        ('If you were born in July and today is late May 2026, your birthday is approximately 38 to 68 days away depending on your exact birth date. Enter your date above for the precise countdown.', 'The calculator automatically moves to the same month and day next year, so the result always counts down to your next birthday.'),
        ('If you were born in July and today is late May 2026, your birthday is approximately 30-60 days away. Enter your exact birth date above for a precise countdown.', 'If your birthday has already passed this year, the calculator automatically counts down to the same month and day next year.'),
        ('Enter your birth date in the calculator above. It will show you exactly what day of the week your birthday falls on in 2026, along with your Zodiac sign.', 'Enter your birth date in the calculator above. It will show the weekday for your next birthday, along with your Zodiac sign.'),
        ('The result includes days, weeks, hours, and the day of the week your birthday falls on this year.', 'The result includes days, weeks, hours, and the weekday of your next birthday.'),
    )
    for source, target in replacements:
        text = text.replace(source, target)

    if "function copyBirthdayCountdown()" not in text:
        script_end = text.rfind("</script>")
        if script_end < 0:
            raise ValueError("Birthday Countdown page has no inline script closing tag")
        text = text[:script_end] + "\n" + COPY_COUNTDOWN_SCRIPT + "\n" + text[script_end:]

    if "late May 2026" in text or "May 24, 2026" in text:
        raise ValueError("Birthday Countdown still contains stale May 2026 copy")
    if 'id="qac-copy-countdown"' not in text or "function copyBirthdayCountdown()" not in text:
        raise ValueError("Birthday Countdown copy control was not generated")

    html_path.write_text(text, encoding="utf-8")
    return text != old


def enhance_pregnancy_page(public_dir: Path) -> bool:
    html_path = public_dir / "pregnancy-due-date" / "index.html"
    text = html_path.read_text(encoding="utf-8")
    old = text
    if 'id="qac-how-far-along"' not in text:
        marker = '<h2>How is the Due Date Calculated?</h2>'
        if marker not in text:
            raise ValueError("Pregnancy page is missing the methodology heading")
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
            raise ValueError("Birth-year hub is missing its top advertisement marker")
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

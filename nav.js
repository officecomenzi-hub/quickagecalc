// QuickAgeCalc - Global Navigation
// Edit this file when adding a primary tool. It safely runs after the page body exists.

(function () {
  function addContextualBirthYearLinks(current) {
    var yearMatch = current.match(/^\/born-in(?:\/|-)(196\d)\/$/);
    if (!yearMatch) {
      return;
    }
    if (document.getElementById('qac-contextual-tools')) {
      return;
    }

    var birthYear = yearMatch[1];
    var generationLabel = parseInt(birthYear, 10) <= 1964 ? 'Baby Boomer' : 'Generation X';
    var section = document.createElement('section');
    section.id = 'qac-contextual-tools';
    section.className = 'card qac-contextual-tools';
    section.setAttribute('aria-labelledby', 'qac-contextual-tools-title');
    section.innerHTML = '<h2 id="qac-contextual-tools-title">Explore More About Your Age</h2>' +
      '<p>Use these related pages to compare nearby birth years, check another year, and confirm your generation.</p>' +
      '<div class="qac-contextual-grid">' +
        '<a href="/born-in-the-1960s/"><strong>1960s Age Guide</strong><span>Compare ages in 2026 for every birth year from 1960 to 1969.</span></a>' +
        '<a href="/age-in-any-year/"><strong>Age in Any Year</strong><span>See how old someone born in ' + birthYear + ' was or will be in any year.</span></a>' +
        '<a href="/what-generation-am-i/"><strong>What Generation Am I?</strong><span>Confirm the ' + generationLabel + ' range and nearby cutoff years.</span></a>' +
        '<a href="/age-questions/"><strong>Age Questions & Answers</strong><span>Find quick answers and the best calculator for common age questions.</span></a>' +
      '</div>';

    var firstContentCard = document.querySelector('.card.content');
    var yearNav = document.querySelector('.year-nav');
    if (firstContentCard && firstContentCard.parentNode) {
      firstContentCard.insertAdjacentElement('afterend', section);
    } else if (yearNav && yearNav.parentNode) {
      yearNav.insertAdjacentElement('afterend', section);
    }
  }

  function addDecadeNavigation(current) {
    var yearMatch = current.match(/^\/born-in(?:\/|-)(19[6-9]\d|200\d)\/$/);
    var hubMatch = current.match(/^\/born-in-the-(1960s|1970s|1980s|1990s|2000s)\/$/);
    var isBirthYearIndex = current === '/born-in-year/';

    if (!yearMatch && !hubMatch && !isBirthYearIndex) {
      return;
    }
    if (document.getElementById('qac-decade-navigation')) {
      return;
    }

    var activeDecade = '';
    var intro = 'Open a decade guide to compare ages in 2026 and reach every individual birth-year calculator.';
    if (yearMatch) {
      var birthYear = parseInt(yearMatch[1], 10);
      activeDecade = String(Math.floor(birthYear / 10) * 10) + 's';
      intro = 'Born in ' + birthYear + '? Open the ' + activeDecade + ' guide or compare nearby birth-year decades.';
    } else if (hubMatch) {
      activeDecade = hubMatch[1];
      intro = 'Compare this decade with nearby birth-year guides and open the central age-by-year index.';
    }

    var decades = ['1960s', '1970s', '1980s', '1990s', '2000s'];
    var links = decades.map(function (decade) {
      var activeClass = decade === activeDecade ? ' class="active"' : '';
      return '<a href="/born-in-the-' + decade + '/"' + activeClass + '><strong>' + decade + '</strong><span>Age by year and generation</span></a>';
    }).join('');

    var section = document.createElement('section');
    section.id = 'qac-decade-navigation';
    section.className = 'card qac-decade-navigation';
    section.setAttribute('aria-labelledby', 'qac-decade-navigation-title');
    section.innerHTML = '<h2 id="qac-decade-navigation-title">Browse Birth-Year Decades</h2>' +
      '<p>' + intro + '</p>' +
      '<div class="qac-decade-grid">' + links +
        '<a href="/born-in-year/"><strong>All years</strong><span>1960 through 2026</span></a>' +
      '</div>';

    var firstContentCard = document.querySelector('.card.content');
    var hero = document.querySelector('.hero');
    var firstCard = document.querySelector('.card');
    if (yearMatch && firstContentCard && firstContentCard.parentNode) {
      firstContentCard.insertAdjacentElement('afterend', section);
    } else if (hero && hero.parentNode) {
      hero.insertAdjacentElement('afterend', section);
    } else if (firstCard && firstCard.parentNode) {
      firstCard.parentNode.insertBefore(section, firstCard);
    }
  }

  function addLastReviewedNote(current) {
    var reviewedPages = {
      '/': { iso: '2026-07-25', label: 'July 25, 2026' },
      '/age-in-any-year/': { iso: '2026-07-28', label: 'July 28, 2026' },
      '/what-year-was-i-born/': { iso: '2026-07-18', label: 'July 18, 2026' },
      '/what-generation-am-i/': { iso: '2026-07-28', label: 'July 28, 2026' },
      '/age-questions/': { iso: '2026-07-28', label: 'July 28, 2026' },
      '/born-in-year/': { iso: '2026-07-29', label: 'July 29, 2026' }
    };
    var review = reviewedPages[current];
    if (!review || document.getElementById('qac-last-reviewed')) {
      return;
    }

    var heading = document.querySelector('h1');
    if (!heading) {
      return;
    }

    var note = document.createElement('p');
    note.id = 'qac-last-reviewed';
    note.className = 'qac-last-reviewed';
    note.innerHTML = 'Last reviewed: <time datetime="' + review.iso + '">' + review.label + '</time>';
    heading.insertAdjacentElement('afterend', note);
  }

  function initQuickAgeCalcNavigation() {
    var tools = [
      { href: '/',                         icon: '\uD83C\uDF82', label: 'Age Calc' },
      { href: '/age-in-any-year/',         icon: '\uD83D\uDCC6', label: 'Any Year' },
      { href: '/what-year-was-i-born/',    icon: '\uD83D\uDD04', label: 'Birth Year' },
      { href: '/what-generation-am-i/',    icon: '\uD83D\uDC65', label: 'Generation' },
      { href: '/date-difference/',          icon: '\uD83D\uDCC5', label: 'Date Diff' },
      { href: '/birthday-countdown/',       icon: '\u23F3',       label: 'Birthday' },
      { href: '/retirement-calculator/',    icon: '\uD83C\uDFD6\uFE0F', label: 'Retirement' },
      { href: '/age-questions/',            icon: '\u2753',       label: 'Questions' },
      { href: '/born-in-year/',             icon: '\uD83D\uDCCB', label: 'By Year' }
    ];

    var current = window.location.pathname.replace(/\/?$/, '/');
    var navHTML = tools.map(function (tool) {
      var isActive = tool.href === '/' ? current === '/' : current.startsWith(tool.href);
      return '<a href="' + tool.href + '"' + (isActive ? ' class="active"' : '') + '>' + tool.icon + ' ' + tool.label + '</a>';
    }).join('');

    var headerHTML = '<header class="qac-global-header"><div class="qac-header-inner"><a class="logo" href="/"><span>Quick</span>AgeCalc</a><nav aria-label="Main navigation">' + navHTML + '</nav></div></header>';
    var year = new Date().getFullYear();
    var footerHTML = '<footer class="qac-global-footer"><p>© ' + year + ' QuickAgeCalc · <a href="/privacy/">Privacy Policy</a> · <a href="/about/">About</a> · <a href="/contact/">Contact</a></p><p class="qac-footer-note">Free online age and date tools. Your entries stay in your browser.</p></footer>';

    var style = document.createElement('style');
    style.textContent = '.qac-global-header{background:#fff;border-bottom:1px solid #e2e6ea;padding:14px 0;margin-bottom:32px}.qac-header-inner{max-width:980px;margin:0 auto;padding:0 20px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px}.qac-global-header .logo{font-family:"Playfair Display",serif;font-size:1.3rem;color:#2563eb;text-decoration:none}.qac-global-header .logo span{color:#1a202c}.qac-global-header nav{display:flex;gap:4px;flex-wrap:wrap}.qac-global-header nav a{font-size:12px;color:#6b7280;text-decoration:none;padding:6px 8px;border-radius:6px;transition:background .2s,color .2s;white-space:nowrap}.qac-global-header nav a:hover,.qac-global-header nav a.active{background:#eff6ff;color:#2563eb}.qac-global-header nav a.active{font-weight:700}.qac-global-footer{text-align:center;padding:28px 20px;font-size:13px;color:#6b7280;border-top:1px solid #e2e6ea;margin-top:32px}.qac-global-footer a{color:#6b7280;text-decoration:none}.qac-global-footer a:hover{color:#2563eb}.qac-footer-note{margin-top:8px}.qac-last-reviewed{display:inline-block;margin:8px 0 0;padding:6px 10px;border:1px solid #bfdbfe;border-radius:999px;background:#eff6ff;color:#1e40af;font-size:12px;font-weight:700;line-height:1.3}.ad-slot{display:none!important;height:0!important;margin:0!important;padding:0!important;border:0!important;overflow:hidden!important}.qac-contextual-tools h2,.qac-decade-navigation h2{font-family:"Playfair Display",serif;font-size:1.35rem;margin-bottom:8px}.qac-contextual-tools>p,.qac-decade-navigation>p{font-size:14px;line-height:1.65;color:#6b7280;margin-bottom:14px}.qac-contextual-grid,.qac-decade-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.qac-contextual-grid a,.qac-decade-grid a{display:block;border:1px solid #e2e6ea;border-radius:10px;padding:14px;text-decoration:none;color:#1a202c;background:#f7f8fa}.qac-contextual-grid a:hover,.qac-decade-grid a:hover,.qac-decade-grid a.active{border-color:#2563eb;background:#eff6ff}.qac-contextual-grid strong,.qac-decade-grid strong{display:block;font-size:14px;margin-bottom:4px}.qac-contextual-grid span,.qac-decade-grid span{display:block;font-size:12px;line-height:1.5;color:#6b7280}@media(max-width:760px){.qac-header-inner{justify-content:center}.qac-global-header .logo{width:100%;text-align:center}.qac-global-header nav{justify-content:center}}@media(max-width:540px){.qac-contextual-grid,.qac-decade-grid{grid-template-columns:1fr}}';
    document.head.appendChild(style);

    if (!document.querySelector('header')) {
      document.body.insertAdjacentHTML('afterbegin', headerHTML);
    }
    if (!document.querySelector('footer')) {
      document.body.insertAdjacentHTML('beforeend', footerHTML);
    }

    addLastReviewedNote(current);
    addDecadeNavigation(current);
    addContextualBirthYearLinks(current);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initQuickAgeCalcNavigation, { once: true });
  } else {
    initQuickAgeCalcNavigation();
  }
})();

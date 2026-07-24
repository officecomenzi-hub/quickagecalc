// QuickAgeCalc - Global Navigation
// Edit this file when adding a primary tool. It safely runs after the page body exists.

(function () {
  function addContextualBirthYearLinks(current) {
    if (!/^\/born-in\/(1961|1965)\/$/.test(current) && !/^\/born-in-(1961|1965)\/$/.test(current)) {
      return;
    }
    if (document.getElementById('qac-contextual-tools')) {
      return;
    }

    var yearMatch = current.match(/(1961|1965)/);
    var birthYear = yearMatch ? yearMatch[1] : '';
    var generationLabel = birthYear === '1961' ? 'Baby Boomer' : 'Generation X';
    var section = document.createElement('section');
    section.id = 'qac-contextual-tools';
    section.className = 'card qac-contextual-tools';
    section.setAttribute('aria-labelledby', 'qac-contextual-tools-title');
    section.innerHTML = '<h2 id="qac-contextual-tools-title">Explore More About Your Age</h2>' +
      '<p>Use these related tools to check your age in another year, confirm your generation, or explore common age questions.</p>' +
      '<div class="qac-contextual-grid">' +
        '<a href="/age-in-any-year/"><strong>Age in Any Year</strong><span>See how old someone born in ' + birthYear + ' was or will be in any year.</span></a>' +
        '<a href="/what-generation-am-i/"><strong>What Generation Am I?</strong><span>Confirm the ' + generationLabel + ' range and nearby cutoff years.</span></a>' +
        '<a href="/what-year-was-i-born/"><strong>Birth Year Calculator</strong><span>Calculate a birth year from a current or future age.</span></a>' +
        '<a href="/age-questions/"><strong>Age Questions & Answers</strong><span>Find quick answers and the best calculator for common age questions.</span></a>' +
      '</div>';

    var yearNav = document.querySelector('.year-nav');
    var firstContentCard = document.querySelector('.card.content');
    if (yearNav && yearNav.parentNode) {
      yearNav.insertAdjacentElement('afterend', section);
    } else if (firstContentCard && firstContentCard.parentNode) {
      firstContentCard.parentNode.insertBefore(section, firstContentCard);
    }
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
    var footerHTML = '<footer class="qac-global-footer"><p>\u00A9 ' + year + ' QuickAgeCalc \u00B7 <a href="/privacy/">Privacy Policy</a> \u00B7 <a href="/about/">About</a> \u00B7 <a href="/contact/">Contact</a></p><p class="qac-footer-note">Free online age and date tools. Your entries stay in your browser.</p></footer>';

    var style = document.createElement('style');
    style.textContent = '.qac-global-header{background:#fff;border-bottom:1px solid #e2e6ea;padding:14px 0;margin-bottom:32px}.qac-header-inner{max-width:980px;margin:0 auto;padding:0 20px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px}.qac-global-header .logo{font-family:"Playfair Display",serif;font-size:1.3rem;color:#2563eb;text-decoration:none}.qac-global-header .logo span{color:#1a202c}.qac-global-header nav{display:flex;gap:4px;flex-wrap:wrap}.qac-global-header nav a{font-size:12px;color:#6b7280;text-decoration:none;padding:6px 8px;border-radius:6px;transition:background .2s,color .2s;white-space:nowrap}.qac-global-header nav a:hover,.qac-global-header nav a.active{background:#eff6ff;color:#2563eb}.qac-global-header nav a.active{font-weight:700}.qac-global-footer{text-align:center;padding:28px 20px;font-size:13px;color:#6b7280;border-top:1px solid #e2e6ea;margin-top:32px}.qac-global-footer a{color:#6b7280;text-decoration:none}.qac-global-footer a:hover{color:#2563eb}.qac-footer-note{margin-top:8px}.ad-slot{display:none!important;height:0!important;margin:0!important;padding:0!important;border:0!important;overflow:hidden!important}.qac-contextual-tools h2{font-family:"Playfair Display",serif;font-size:1.35rem;margin-bottom:8px}.qac-contextual-tools>p{font-size:14px;line-height:1.65;color:#6b7280;margin-bottom:14px}.qac-contextual-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.qac-contextual-grid a{display:block;border:1px solid #e2e6ea;border-radius:10px;padding:14px;text-decoration:none;color:#1a202c;background:#f7f8fa}.qac-contextual-grid a:hover{border-color:#2563eb;background:#eff6ff}.qac-contextual-grid strong{display:block;font-size:14px;margin-bottom:4px}.qac-contextual-grid span{display:block;font-size:12px;line-height:1.5;color:#6b7280}@media(max-width:760px){.qac-header-inner{justify-content:center}.qac-global-header .logo{width:100%;text-align:center}.qac-global-header nav{justify-content:center}}@media(max-width:540px){.qac-contextual-grid{grid-template-columns:1fr}}';
    document.head.appendChild(style);

    if (!document.querySelector('header')) {
      document.body.insertAdjacentHTML('afterbegin', headerHTML);
    }
    if (!document.querySelector('footer')) {
      document.body.insertAdjacentHTML('beforeend', footerHTML);
    }

    addContextualBirthYearLinks(current);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initQuickAgeCalcNavigation, { once: true });
  } else {
    initQuickAgeCalcNavigation();
  }
})();
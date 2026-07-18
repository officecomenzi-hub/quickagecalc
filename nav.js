// QuickAgeCalc - Global Navigation
// Edit this file when adding a primary tool. It safely runs after the page body exists.

(function () {
  function initQuickAgeCalcNavigation() {
    var tools = [
      { href: '/',                         icon: '\uD83C\uDF82', label: 'Age Calc' },
      { href: '/age-in-any-year/',         icon: '\uD83D\uDCC6', label: 'Any Year' },
      { href: '/what-year-was-i-born/',    icon: '\uD83D\uDD04', label: 'Birth Year' },
      { href: '/what-generation-am-i/',    icon: '\uD83D\uDC65', label: 'Generation' },
      { href: '/age-questions/',            icon: '\u2753',       label: 'Questions' },
      { href: '/birthday-countdown/',       icon: '\u23F3',       label: 'Birthday' },
      { href: '/born-in-year/',             icon: '\uD83D\uDCC5', label: 'By Year' }
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
    style.textContent = '.qac-global-header{background:#fff;border-bottom:1px solid #e2e6ea;padding:14px 0;margin-bottom:32px}.qac-header-inner{max-width:900px;margin:0 auto;padding:0 20px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px}.qac-global-header .logo{font-family:"Playfair Display",serif;font-size:1.3rem;color:#2563eb;text-decoration:none}.qac-global-header .logo span{color:#1a202c}.qac-global-header nav{display:flex;gap:4px;flex-wrap:wrap}.qac-global-header nav a{font-size:12px;color:#6b7280;text-decoration:none;padding:6px 8px;border-radius:6px;transition:background .2s,color .2s;white-space:nowrap}.qac-global-header nav a:hover,.qac-global-header nav a.active{background:#eff6ff;color:#2563eb}.qac-global-header nav a.active{font-weight:700}.qac-global-footer{text-align:center;padding:28px 20px;font-size:13px;color:#6b7280;border-top:1px solid #e2e6ea;margin-top:32px}.qac-global-footer a{color:#6b7280;text-decoration:none}.qac-global-footer a:hover{color:#2563eb}.qac-footer-note{margin-top:8px}.ad-slot{display:none!important;height:0!important;margin:0!important;padding:0!important;border:0!important;overflow:hidden!important}@media(max-width:760px){.qac-header-inner{justify-content:center}.qac-global-header .logo{width:100%;text-align:center}.qac-global-header nav{justify-content:center}}';
    document.head.appendChild(style);

    if (!document.querySelector('header')) {
      document.body.insertAdjacentHTML('afterbegin', headerHTML);
    }
    if (!document.querySelector('footer')) {
      document.body.insertAdjacentHTML('beforeend', footerHTML);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initQuickAgeCalcNavigation, { once: true });
  } else {
    initQuickAgeCalcNavigation();
  }
})();

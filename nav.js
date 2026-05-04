// QuickAgeCalc - Global Navigation
// Modifica DOAR acest fisier cand adaugi un tool nou
// Se aplica automat pe toate paginile

(function() {
  var tools = [
    { href: '/',                    icon: '\uD83C\uDF82', label: 'Age Calc' },
    { href: '/date-difference/',    icon: '\uD83D\uDCC5', label: 'Date Diff' },
    { href: '/birthday-countdown/', icon: '\u23F3',       label: 'Birthday' },
    { href: '/age-difference/',     icon: '\uD83D\uDC6B', label: 'Age Diff' },
    { href: '/pregnancy-due-date/', icon: '\uD83E\uDD30', label: 'Due Date' },
    { href: '/dog-age/',            icon: '\uD83D\uDC15', label: 'Dog Age' },
    { href: '/born-in-year/',       icon: '\uD83D\uDCC6', label: 'By Year' },
  ];

  var current = window.location.pathname.replace(/\/?$/, '/');

  var navHTML = tools.map(function(t) {
    var isActive = (t.href === '/' ? current === '/' : current.startsWith(t.href));
    return '<a href="' + t.href + '"' + (isActive ? ' class="active"' : '') + '>' + t.icon + ' ' + t.label + '</a>';
  }).join('');

  var headerHTML = '<header><div class="inner" style="max-width:760px;margin:0 auto;padding:0 20px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;"><a class="logo" href="/" style="font-family:\'Playfair Display\',serif;font-size:1.3rem;color:#2563eb;text-decoration:none;"><span style="color:#1a202c;">Quick</span>AgeCalc</a><nav style="display:flex;gap:4px;flex-wrap:wrap;">' + navHTML + '</nav></div></header>';

  var footerHTML = '<footer style="text-align:center;padding:28px 0;font-size:13px;color:#6b7280;border-top:1px solid #e2e6ea;margin-top:32px;"><p>\u00A9 2026 QuickAgeCalc \u00B7 <a href="/privacy/">Privacy Policy</a> \u00B7 <a href="/about/">About</a> \u00B7 <a href="/contact/">Contact</a></p><p style="margin-top:8px">Free online tools for everyone.</p></footer>';

  var navStyle = '<style>header{background:#ffffff;border-bottom:1px solid #e2e6ea;padding:14px 0;margin-bottom:32px;}header nav a{font-size:13px;color:#6b7280;text-decoration:none;padding:5px 10px;border-radius:6px;transition:background .2s,color .2s;white-space:nowrap;}header nav a:hover{background:#eff6ff;color:#2563eb;}header nav a.active{background:#eff6ff;color:#2563eb;font-weight:700;}footer a{color:#6b7280;text-decoration:none;margin:0 8px;}footer a:hover{color:#2563eb;}</style>';

  document.head.insertAdjacentHTML('beforeend', navStyle);
  document.body.insertAdjacentHTML('afterbegin', headerHTML);
  document.body.insertAdjacentHTML('beforeend', footerHTML);
})();

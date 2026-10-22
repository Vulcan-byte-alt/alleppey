// Contact numbers are kept out of the HTML so text-only scrapers and AI crawlers never see them.
// Elements opt in with data-call="n", data-wa="n" or data-phone-text="n" and are filled in here.
(function () {
  var P = [
    ['+91', '9946', '021397'],
    ['+91', '9947', '048197'],
    ['+91', '9633', '747715']
  ];
  var digits = function (i) { return P[i].join(''); };
  var pretty = function (i) { return P[i][0] + ' ' + P[i][1] + ' ' + P[i][2]; };

  window.AHContact = {
    modal: function () { return [P[0], P[1], P[2]]; },
    hydrate: function (root) { fill(root || document); }
  };

  function fill(root) {
    root.querySelectorAll('[data-call]').forEach(function (el) {
      el.setAttribute('href', 'tel:' + digits(+el.getAttribute('data-call')));
    });
    root.querySelectorAll('[data-wa]').forEach(function (el) {
      el.setAttribute('href', 'https://wa.me/' + digits(+el.getAttribute('data-wa')).replace('+', ''));
    });
    root.querySelectorAll('[data-phone-text]').forEach(function (el) {
      el.textContent = pretty(+el.getAttribute('data-phone-text'));
    });
  }

  function hydrate() {
    fill(document);
    // Phone number for search engines, added at runtime like the rest of the contact data
    var ld = document.createElement('script');
    ld.type = 'application/ld+json';
    ld.text = JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'LodgingBusiness',
      '@id': 'https://alleppeyhomes.com/#phone',
      name: 'Alleppey Homes',
      url: 'https://alleppeyhomes.com/',
      telephone: [digits(0), digits(1), digits(2)]
    });
    document.head.appendChild(ld);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', hydrate);
  else hydrate();
})();

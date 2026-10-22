// Alleppey Homes: menu sheet, mobile dock, contact modal, scroll reveal, simple lightbox.
(function () {
  function ready(fn) { document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', fn) : fn(); }

  ready(function () {
    var $ = function (s, r) { return (r || document).querySelector(s); };

    // Menu sheet
    var toggle = $('#nav-toggle'), sheet = $('#sheet');
    if (toggle && sheet) {
      var setOpen = function (open) {
        toggle.setAttribute('aria-expanded', String(open));
        toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
        document.documentElement.style.overflow = open ? 'hidden' : '';
        if (open) { sheet.hidden = false; requestAnimationFrame(function () { sheet.classList.add('open'); }); }
        else { sheet.classList.remove('open'); setTimeout(function () { if (!sheet.classList.contains('open')) sheet.hidden = true; }, 400); }
      };
      toggle.addEventListener('click', function () { setOpen(toggle.getAttribute('aria-expanded') !== 'true'); });
      sheet.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });
    }

    // Mobile dock appears after the first screen
    var dock = $('#dock');
    if (dock) {
      var onScroll = function () { dock.classList.toggle('show', window.scrollY > 320); };
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();
    }

    // Contact modal: numbers come from contact.js
    var modal = $('#contact-modal');
    if (modal && window.AHContact) {
      var list = $('#contact-modal-numbers');
      AHContact.modal().forEach(function (parts) {
        var tel = parts.join(''), pretty = parts.join(' ');
        var item = document.createElement('div');
        item.className = 'modal__item';
        item.innerHTML = '<b>' + pretty + '</b><div>' +
          '<a class="btn btn--primary btn--sm" href="tel:' + tel + '">Call</a>' +
          '<a class="btn btn--glass btn--sm" target="_blank" rel="noopener" href="https://wa.me/' + tel.replace('+', '') + '">WhatsApp</a></div>';
        list.appendChild(item);
      });
      document.querySelectorAll('[data-open-contact]').forEach(function (b) {
        b.addEventListener('click', function () { if (modal.showModal) modal.showModal(); else window.location.href = 'contact.html'; });
      });
      modal.addEventListener('click', function (e) { if (e.target === modal) modal.close(); });
    }
    if (window.AHContact) AHContact.hydrate(document);

    // Scroll reveal
    var items = document.querySelectorAll('[data-reveal]');
    if ('IntersectionObserver' in window && items.length) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
      }, { rootMargin: '0px 0px -8% 0px' });
      items.forEach(function (el) { io.observe(el); });
    } else { items.forEach(function (el) { el.classList.add('in'); }); }

    // Hero video: only on larger screens, with motion allowed and no data-saver
    var vid = $('video[data-hero]');
    if (vid) {
      var conn = navigator.connection || {};
      var ok = window.matchMedia('(min-width: 700px)').matches && !window.matchMedia('(prefers-reduced-motion: reduce)').matches && !conn.saveData;
      if (ok) { vid.src = vid.getAttribute('data-src'); vid.play().catch(function () {}); vid.addEventListener('playing', function () { vid.classList.add('on'); }); }
    }

    // Lightbox for .masonry galleries
    var galleries = document.querySelectorAll('.masonry');
    if (galleries.length) {
      var lb = document.createElement('dialog');
      lb.className = 'modal';
      lb.style.maxWidth = '96vw';
      lb.innerHTML = '<div class="modal__panel" style="padding:.75rem;background:rgba(10,16,13,.9)"><button class="modal__close" aria-label="Close" type="button">&times;</button><img alt="" style="width:100%;max-height:82vh;object-fit:contain;border-radius:18px"></div>';
      document.body.appendChild(lb);
      var lbImg = lb.querySelector('img');
      lb.querySelector('button').addEventListener('click', function () { lb.close(); });
      lb.addEventListener('click', function (e) { if (e.target === lb) lb.close(); });
      galleries.forEach(function (g) {
        g.addEventListener('click', function (e) {
          var a = e.target.closest('a'); if (!a || !lb.showModal) return;
          e.preventDefault(); lbImg.src = a.getAttribute('href'); lbImg.alt = (a.querySelector('img') || {}).alt || ''; lb.showModal();
        });
      });
    }
  });
})();

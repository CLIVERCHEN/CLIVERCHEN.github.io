(() => {
  'use strict';
  const dialog = document.querySelector('#lightbox');
  const photos = [...document.querySelectorAll('[data-lightbox]')];
  if (dialog && typeof dialog.showModal === 'function' && photos.length) {
    const image = dialog.querySelector('#lightbox-image');
    const caption = dialog.querySelector('#lightbox-caption');
    const counter = dialog.querySelector('#lightbox-count');
    const original = dialog.querySelector('#lightbox-original');
    const closeButton = dialog.querySelector('.lightbox-close');
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    let active = [], index = 0, opener = null, request = 0, closeTimer = null;

    function show(next) {
      index = (next + active.length) % active.length;
      const photo = active[index];
      const currentRequest = ++request;
      image.src = photo.dataset.preview;
      image.alt = photo.querySelector('img').alt;
      caption.textContent = photo.dataset.title;
      counter.textContent = `${index + 1} / ${active.length}`;
      original.href = photo.href;
      const full = new Image();
      full.onload = () => { if (request === currentRequest && dialog.open) image.src = full.src; };
      full.src = photo.href;
      // Preload just the next photograph, never the whole gallery.
      if (active.length > 1) { const preload = new Image(); preload.src = active[(index + 1) % active.length].href; }
    }

    function finishClose() {
      clearTimeout(closeTimer);
      closeTimer = null;
      dialog.close();
      document.documentElement.classList.remove('viewer-open');
      request++;
      opener?.focus({ preventScroll: true });
    }
    function close() {
      if (!dialog.open || closeTimer) return;
      dialog.classList.remove('is-visible');
      if (reducedMotion.matches) finishClose();
      else closeTimer = setTimeout(finishClose, 220);
    }
    photos.forEach(photo => photo.addEventListener('click', event => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      opener = photo;
      active = photos.filter(item => { const details = item.closest('details'); return !details || details.open; });
      clearTimeout(closeTimer); closeTimer = null;
      show(active.indexOf(photo));
      dialog.showModal();
      document.documentElement.classList.add('viewer-open');
      closeButton.focus({ preventScroll: true });
      requestAnimationFrame(() => dialog.classList.add('is-visible'));
    }));
    closeButton.addEventListener('click', close);
    dialog.querySelector('.lightbox-prev').addEventListener('click', () => show(index - 1));
    dialog.querySelector('.lightbox-next').addEventListener('click', () => show(index + 1));
    dialog.addEventListener('cancel', event => { event.preventDefault(); close(); });
    dialog.addEventListener('close', () => document.documentElement.classList.remove('viewer-open'));
    dialog.addEventListener('click', event => { if (event.target === dialog) close(); });
    dialog.addEventListener('keydown', event => {
      if (event.key === 'ArrowLeft') { event.preventDefault(); show(index - 1); }
      if (event.key === 'ArrowRight') { event.preventDefault(); show(index + 1); }
    });
    let startX = 0, startY = 0;
    image.addEventListener('touchstart', event => { startX = event.changedTouches[0].clientX; startY = event.changedTouches[0].clientY; }, { passive:true });
    image.addEventListener('touchend', event => {
      const dx = event.changedTouches[0].clientX - startX;
      const dy = event.changedTouches[0].clientY - startY;
      if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) show(index + (dx < 0 ? 1 : -1));
    }, { passive:true });
  }

  // The content stays visible without JavaScript; only the current nav item changes.
  const sections = [...document.querySelectorAll('main section[id]')];
  if (sections.length && 'IntersectionObserver' in window) {
    const navLinks = [...document.querySelectorAll('[data-section]')];
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        navLinks.forEach(link => {
          if (link.dataset.section === entry.target.id) link.setAttribute('aria-current', 'location');
          else link.removeAttribute('aria-current');
        });
      });
    }, { rootMargin:'-15% 0px -65% 0px', threshold:0 });
    sections.forEach(section => observer.observe(section));
  }
})();

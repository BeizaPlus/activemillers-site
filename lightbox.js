/* Lightbox — click any .image-row or .stacked-images img to open fullscreen.
   Load this file on every case study page. Works standalone, no dependencies. */
(function () {
  if (document.querySelector('.lb-overlay')) return; // already loaded

  var overlay = document.createElement('div');
  overlay.className = 'lb-overlay';
  overlay.innerHTML = '<img src="" alt="" />';
  document.body.appendChild(overlay);

  var closeBtn = document.createElement('button');
  closeBtn.className = 'lb-close';
  closeBtn.setAttribute('aria-label', 'Close');
  closeBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>';
  document.body.appendChild(closeBtn);

  var img = overlay.querySelector('img');

  function open(src, alt) {
    img.src = src;
    img.alt = alt || '';
    overlay.classList.add('open');
    closeBtn.classList.add('visible');
    document.body.style.overflow = 'hidden';
  }

  function close() {
    overlay.classList.remove('open');
    closeBtn.classList.remove('visible');
    document.body.style.overflow = '';
    setTimeout(function () { img.src = ''; }, 300);
  }

  closeBtn.addEventListener('click', function (e) { e.stopPropagation(); close(); });
  overlay.addEventListener('click', function (e) { if (e.target === overlay || e.target === img) close(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });

  // Attach click handlers to all case-study images
  var containers = document.querySelectorAll('.image-row, .stacked-images');
  containers.forEach(function (container) {
    container.querySelectorAll('img').forEach(function (el) {
      el.style.cursor = 'zoom-in';
      el.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        open(el.src, el.alt);
      });
    });
  });
})();

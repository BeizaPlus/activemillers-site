/* Lightbox — click any content image to open fullscreen, arrow through the rest of the page's gallery.
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

  var infoBtn = document.createElement('button');
  infoBtn.className = 'lb-info';
  infoBtn.setAttribute('aria-label', 'Toggle caption');
  infoBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><line x1="12" y1="11" x2="12" y2="16"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>';
  document.body.appendChild(infoBtn);

  var prevBtn = document.createElement('button');
  prevBtn.className = 'lb-arrow lb-prev';
  prevBtn.setAttribute('aria-label', 'Previous image');
  prevBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>';
  document.body.appendChild(prevBtn);

  var nextBtn = document.createElement('button');
  nextBtn.className = 'lb-arrow lb-next';
  nextBtn.setAttribute('aria-label', 'Next image');
  nextBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>';
  document.body.appendChild(nextBtn);

  var counter = document.createElement('div');
  counter.className = 'lb-counter';
  document.body.appendChild(counter);

  var captionBar = document.createElement('div');
  captionBar.className = 'lb-caption';
  captionBar.innerHTML = '<div class="lb-caption-num"></div><div class="lb-caption-title"></div>';
  document.body.appendChild(captionBar);

  var img = overlay.querySelector('img');
  var captionNum = captionBar.querySelector('.lb-caption-num');
  var captionTitle = captionBar.querySelector('.lb-caption-title');
  var gallery = [];
  var currentIndex = 0;
  var captionOpen = false;

  function getCaption(el) {
    var figure = el.closest('.step-figure');
    if (!figure) return null;
    var capEl = figure.querySelector('.step-caption');
    if (!capEl) return null;
    var num = capEl.querySelector('.fig-num');
    var title = capEl.querySelector('.fig-title');
    return {
      num: num ? num.textContent : '',
      title: title ? title.textContent : ''
    };
  }

  function updateCounter() {
    if (gallery.length > 1) {
      counter.textContent = (currentIndex + 1) + ' / ' + gallery.length;
      counter.classList.add('visible');
    } else {
      counter.classList.remove('visible');
    }
  }

  function updateArrows() {
    var show = gallery.length > 1;
    prevBtn.classList.toggle('visible', show);
    nextBtn.classList.toggle('visible', show);
  }

  function updateCaption() {
    var el = gallery[currentIndex];
    var cap = el ? el._lbCaption : null;
    if (cap && (cap.num || cap.title)) {
      infoBtn.classList.add('visible');
      captionNum.textContent = cap.num;
      captionTitle.textContent = cap.title;
      captionBar.classList.toggle('open', captionOpen);
    } else {
      infoBtn.classList.remove('visible');
      captionBar.classList.remove('open');
    }
  }

  function showIndex(i) {
    if (!gallery.length) return;
    currentIndex = (i + gallery.length) % gallery.length;
    var el = gallery[currentIndex];
    img.src = el.src;
    img.alt = el.alt || '';
    updateCounter();
    updateCaption();
  }

  function open(clickedEl) {
    gallery = Array.prototype.slice.call(document.querySelectorAll(
      '.image-row img, .stacked-images img, .step-images img, .full-image img'
    ));
    gallery.forEach(function (el) { el._lbCaption = getCaption(el); });
    var idx = gallery.indexOf(clickedEl);
    captionOpen = false;
    showIndex(idx === -1 ? 0 : idx);
    updateArrows();
    overlay.classList.add('open');
    closeBtn.classList.add('visible');
    document.body.style.overflow = 'hidden';
  }

  function close() {
    overlay.classList.remove('open');
    closeBtn.classList.remove('visible');
    infoBtn.classList.remove('visible');
    prevBtn.classList.remove('visible');
    nextBtn.classList.remove('visible');
    counter.classList.remove('visible');
    captionBar.classList.remove('open');
    document.body.style.overflow = '';
    setTimeout(function () { img.src = ''; }, 300);
  }

  function next() { showIndex(currentIndex + 1); }
  function prev() { showIndex(currentIndex - 1); }
  function toggleCaption() { captionOpen = !captionOpen; captionBar.classList.toggle('open', captionOpen); }

  closeBtn.addEventListener('click', function (e) { e.stopPropagation(); close(); });
  infoBtn.addEventListener('click', function (e) { e.stopPropagation(); toggleCaption(); });
  nextBtn.addEventListener('click', function (e) { e.stopPropagation(); next(); });
  prevBtn.addEventListener('click', function (e) { e.stopPropagation(); prev(); });
  overlay.addEventListener('click', function (e) { if (e.target === overlay || e.target === img) close(); });
  document.addEventListener('keydown', function (e) {
    if (!overlay.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowRight') next();
    if (e.key === 'ArrowLeft') prev();
    if (e.key === 'i' || e.key === 'I') toggleCaption();
  });

  // Attach click handlers to all case-study images
  var containers = document.querySelectorAll('.image-row, .stacked-images, .step-images, .full-image');
  containers.forEach(function (container) {
    container.querySelectorAll('img').forEach(function (el) {
      el.style.cursor = 'zoom-in';
      el.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        open(el);
      });
    });
  });
})();

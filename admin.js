/**
 * ADMIN IMAGE REORDER PANEL — activated by ?edit query param.
 * Drag-and-drop or arrow-click to reorder images. Save writes back to the HTML file.
 */
(function() {
  if (!/[\?&]edit\b/.test(location.search)) return;

  // === CONFIG ===
  const ADMIN_SERVER = 'http://localhost:8760';
  const PAGE_NAME = location.pathname.split('/').pop() || 'index.html';

  // === STATE ===
  let images = [];            // { src, alt, section, el }
  let draggedIdx = -1;

  // === COLLECT ALL CONTENT IMAGES FROM THE PAGE ===
  function collectImages() {
    const result = [];
    // Section order: image-row first, then stacked-images
    const sections = [
      { sel: '.image-row .img-wrap img', name: 'image-row' },
      { sel: '.stacked-images .img-wrap img', name: 'stacked-images' }
    ];
    sections.forEach(function(sec) {
      document.querySelectorAll(sec.sel).forEach(function(img) {
        result.push({
          src: img.getAttribute('src'),
          alt: img.getAttribute('alt') || '',
          section: sec.name,
          el: img
        });
      });
    });
    return result;
  }

  // === BUILD THUMBNAIL HTML ===
  function thumbHTML(img, i) {
    var filename = img.src.split('/').pop();
    var isFirst = i === 0;
    var isLast = i === images.length - 1;
    return '<div class="admin-thumb" draggable="true" data-idx="' + i + '">' +
      '<img src="' + img.src + '" alt="">' +
      '<div class="admin-thumb-info">' +
        '<span class="admin-thumb-label" title="' + filename + '">' + (i + 1) + '. ' + filename + '</span>' +
        '<div class="admin-arrows">' +
          '<button class="admin-arrow admin-up" data-idx="' + i + '" ' + (isFirst ? 'disabled' : '') + '>&#9650;</button>' +
          '<button class="admin-arrow admin-down" data-idx="' + i + '" ' + (isLast ? 'disabled' : '') + '>&#9660;</button>' +
        '</div>' +
      '</div>' +
    '</div>';
  }

  // === RENDER GALLERY ===
  function render() {
    gallery.innerHTML = images.map(function(img, i) { return thumbHTML(img, i); }).join('');
    bindThumbEvents();
  }

  // === BIND DRAG + ARROW EVENTS ===
  function bindThumbEvents() {
    var thumbs = gallery.querySelectorAll('.admin-thumb');

    thumbs.forEach(function(thumb) {
      thumb.addEventListener('dragstart', function(e) {
        draggedIdx = parseInt(thumb.dataset.idx);
        thumb.classList.add('dragging');
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/plain', draggedIdx);
      });

      thumb.addEventListener('dragend', function() {
        thumb.classList.remove('dragging');
        thumbs.forEach(function(t) { t.classList.remove('drag-target'); });
        draggedIdx = -1;
      });

      thumb.addEventListener('dragover', function(e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        if (draggedIdx !== parseInt(thumb.dataset.idx)) {
          thumb.classList.add('drag-target');
        }
      });

      thumb.addEventListener('dragleave', function() {
        thumb.classList.remove('drag-target');
      });

      thumb.addEventListener('drop', function(e) {
        e.preventDefault();
        thumb.classList.remove('drag-target');
        var targetIdx = parseInt(thumb.dataset.idx);
        if (draggedIdx >= 0 && draggedIdx !== targetIdx) {
          moveImage(draggedIdx, targetIdx);
        }
        draggedIdx = -1;
      });
    });

    // Arrow buttons
    gallery.querySelectorAll('.admin-up').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var i = parseInt(btn.dataset.idx);
        if (i > 0) moveImage(i, i - 1);
      });
    });
    gallery.querySelectorAll('.admin-down').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var i = parseInt(btn.dataset.idx);
        if (i < images.length - 1) moveImage(i, i + 1);
      });
    });
  }

  // === MOVE IMAGE IN ARRAY ===
  function moveImage(fromIdx, toIdx) {
    var item = images.splice(fromIdx, 1)[0];
    images.splice(toIdx, 0, item);
    render();
  }

  // === SAVE TO BACKEND ===
  function save() {
    var payload = {
      page: PAGE_NAME,
      images: images.map(function(img) {
        return { src: img.src, alt: img.alt };
      })
    };

    saveBtn.textContent = 'Saving...';
    saveBtn.disabled = true;

    fetch(ADMIN_SERVER + '/save-order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    .then(function(r) {
      if (!r.ok) throw new Error(r.status + ' ' + r.statusText);
      return r.json();
    })
    .then(function(data) {
      toast('Saved — ' + data.count + ' images. Refresh to see.', 'success');
      saveBtn.textContent = 'Save Order';
      saveBtn.disabled = false;
    })
    .catch(function(err) {
      toast('Save failed: ' + err.message + ' (is admin-server.py running on :8760?)', 'error');
      saveBtn.textContent = 'Save Order';
      saveBtn.disabled = false;
    });
  }

  // === TOAST ===
  function toast(msg, type) {
    toastEl.textContent = msg;
    toastEl.className = 'admin-toast ' + type + ' show';
    clearTimeout(toastEl._timeout);
    toastEl._timeout = setTimeout(function() {
      toastEl.classList.remove('show');
    }, 3000);
  }

  // === BUILD UI ===
  var panel = document.createElement('div');
  panel.className = 'admin-panel';
  panel.innerHTML =
    '<div class="admin-panel-header">' +
      '<h3>Edit Image Order — ' + PAGE_NAME + '</h3>' +
      '<div class="admin-actions">' +
        '<button class="admin-btn admin-btn-save" id="adminSave">Save Order</button>' +
        '<button class="admin-btn admin-btn-close" id="adminClose">Close</button>' +
      '</div>' +
    '</div>' +
    '<div class="admin-gallery" id="adminGallery"></div>';

  var toastEl = document.createElement('div');
  toastEl.className = 'admin-toast';

  document.body.appendChild(panel);
  document.body.appendChild(toastEl);

  // Load admin CSS
  var css = document.createElement('link');
  css.rel = 'stylesheet';
  css.href = 'admin.css';
  document.head.appendChild(css);

  var gallery = document.getElementById('adminGallery');
  var saveBtn = document.getElementById('adminSave');
  var closeBtn = document.getElementById('adminClose');

  images = collectImages();
  render();

  saveBtn.addEventListener('click', save);
  closeBtn.addEventListener('click', function() {
    panel.remove();
    toastEl.remove();
  });

  // Keyboard shortcut: Ctrl+S to save
  document.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
      e.preventDefault();
      save();
    }
  });

  console.log('[admin] ' + images.length + ' images loaded for ' + PAGE_NAME + '. Drag to reorder, arrows to move, Save to write.');
  console.log('[admin] Admin server expected at ' + ADMIN_SERVER);
})();

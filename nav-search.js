/* ===== GLOBAL HEADER WIDGET: hamburger nav + case search =====
   Loaded identically on every page. On index.html (where .work-card
   elements exist) the search live-filters + autocompletes locally.
   On every other page it has no local cards to filter, so Enter
   redirects to index.html?q=<query> and index.html re-runs the
   search from that query param on load. */
(function() {
  var toggle = document.getElementById('mobileToggle');
  var nav = document.getElementById('navLinks');
  if (!toggle || !nav) return;
  toggle.addEventListener('click', function() { nav.classList.toggle('mobile-open'); });
  nav.querySelectorAll('a').forEach(function(a) {
    a.addEventListener('click', function() { nav.classList.remove('mobile-open'); });
  });
})();

(function() {
  var input = document.getElementById('caseSearch');
  if (!input) return;
  var suggestBox = document.getElementById('searchSuggestions');
  var noResults = document.getElementById('workNoResults');
  var cards = document.querySelectorAll('.work-card');
  var isIndexPage = cards.length > 0;
  var hasScrolledToResults = false;
  var activeIndex = -1;

  function searchText(card) {
    if (card.dataset.searchText) return card.dataset.searchText;
    var title = card.querySelector('.work-card-title');
    var cat = card.querySelector('.work-card-cat');
    var img = card.querySelector('.work-card-img');
    var href = card.tagName === 'A' ? card.getAttribute('href') : '';
    var bodyIndex = (window.CASE_SEARCH_INDEX && href && window.CASE_SEARCH_INDEX[href]) || '';
    var text = [
      title ? title.textContent : '',
      cat ? cat.textContent : '',
      img ? img.getAttribute('alt') || '' : '',
      bodyIndex
    ].join(' ').toLowerCase();
    card.dataset.searchText = text;
    return text;
  }

  function filterCards(query) {
    var visibleCount = 0;
    cards.forEach(function(card) {
      var match = !query || searchText(card).indexOf(query) !== -1;
      card.classList.toggle('search-hidden', !match);
      if (match) visibleCount++;
    });
    if (noResults) noResults.classList.toggle('visible', query.length > 0 && visibleCount === 0);
  }

  function closeSuggestions() {
    if (!suggestBox) return;
    suggestBox.classList.remove('visible');
    suggestBox.innerHTML = '';
    activeIndex = -1;
  }

  function renderSuggestions(query) {
    if (!suggestBox) return;
    if (!query) { closeSuggestions(); return; }
    var matches = [];
    cards.forEach(function(card) {
      if (card.tagName !== 'A') return; // only real case pages are suggestible
      if (searchText(card).indexOf(query) === -1) return;
      matches.push(card);
    });
    matches = matches.slice(0, 6);
    if (!matches.length) { closeSuggestions(); return; }
    suggestBox.innerHTML = matches.map(function(card, i) {
      var title = card.querySelector('.work-card-title');
      var cat = card.querySelector('.work-card-cat');
      return '<a class="nav-suggestion" href="' + card.getAttribute('href') + '" data-index="' + i + '">' +
        '<div class="nav-suggestion-title">' + (title ? title.textContent : '') + '</div>' +
        '<div class="nav-suggestion-cat">' + (cat ? cat.textContent : '') + '</div>' +
        '</a>';
    }).join('');
    activeIndex = -1;
    suggestBox.classList.add('visible');
  }

  function setActive(index) {
    var items = suggestBox.querySelectorAll('.nav-suggestion');
    items.forEach(function(item) { item.classList.remove('active'); });
    if (index >= 0 && index < items.length) {
      items[index].classList.add('active');
      activeIndex = index;
    }
  }

  function scrollToResultsOnce() {
    if (hasScrolledToResults) return;
    hasScrolledToResults = true;
    var grid = document.getElementById('experiments-anchor');
    if (grid) grid.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function goToIndexWithQuery(query) {
    window.location.href = 'index.html?q=' + encodeURIComponent(query);
  }

  input.addEventListener('input', function() {
    var query = input.value.trim().toLowerCase();
    if (isIndexPage) {
      filterCards(query);
      renderSuggestions(query);
      if (query.length > 0) scrollToResultsOnce();
    }
  });

  input.addEventListener('keydown', function(e) {
    if (isIndexPage) {
      var items = suggestBox ? suggestBox.querySelectorAll('.nav-suggestion') : [];
      if (items.length) {
        if (e.key === 'ArrowDown') { e.preventDefault(); setActive((activeIndex + 1) % items.length); return; }
        if (e.key === 'ArrowUp') { e.preventDefault(); setActive((activeIndex - 1 + items.length) % items.length); return; }
        if (e.key === 'Enter' && activeIndex >= 0) { e.preventDefault(); items[activeIndex].click(); return; }
      }
      if (e.key === 'Escape') closeSuggestions();
    } else if (e.key === 'Enter') {
      e.preventDefault();
      var q = input.value.trim();
      if (q) goToIndexWithQuery(q);
    }
  });

  input.addEventListener('focus', function() {
    if (isIndexPage && input.value.trim()) renderSuggestions(input.value.trim().toLowerCase());
  });

  document.addEventListener('click', function(e) {
    if (!e.target.closest('.nav-search')) closeSuggestions();
  });

  if (isIndexPage) {
    var params = new URLSearchParams(window.location.search);
    var q = params.get('q');
    if (q) {
      input.value = q;
      filterCards(q.trim().toLowerCase());
      scrollToResultsOnce();
    }
  }
})();

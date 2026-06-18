---
layout: page
permalink: /publications/
title: publications
description:
nav: true
nav_order: 2
---

<style>
/* keep the family name bold in the navbar on this page too */
#navbar .navbar-brand.title { font-weight: 700 !important; }
#navbar .navbar-brand .font-weight-bold { font-weight: 400 !important; }

#year-filter { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 1.5rem; }
#year-filter button {
  cursor: pointer; padding: 4px 12px; border-radius: 6px; font-size: 0.85rem;
  background: transparent; color: inherit;
  border: 1px solid var(--global-divider-color, rgba(128,128,128,0.3));
}
#year-filter button:hover { border-color: var(--global-theme-color); }
#year-filter button.active {
  background: var(--global-theme-color); color: #fff; border-color: var(--global-theme-color);
}

/* Landscape, uniform preview thumbnails */
@media (min-width: 576px) {
  .publications .row > .abbr { flex: 0 0 30%; max-width: 30%; }
}
.publications .preview {
  width: 100%;
  height: auto;
  aspect-ratio: 4 / 3;
  object-fit: cover;
  object-position: center top;
}
</style>

{% include bib_search.liquid %}

<div id="year-filter"></div>

<div class="publications">

{% bibliography %}

</div>

<script>
(function () {
  function init() {
    var container = document.querySelector('.publications');
    var bar = document.getElementById('year-filter');
    if (!container || !bar) return;

    var groups = [];
    container.querySelectorAll('h2.bibliography').forEach(function (h) {
      var ol = h.nextElementSibling;
      while (ol && ol.tagName !== 'OL') ol = ol.nextElementSibling;
      groups.push({ year: h.textContent.trim(), h: h, ol: ol });
    });

    function show(year) {
      groups.forEach(function (g) {
        var on = (year === 'All' || g.year === year);
        g.h.style.display = on ? '' : 'none';
        if (g.ol) g.ol.style.display = on ? '' : 'none';
      });
      bar.querySelectorAll('button').forEach(function (b) {
        b.classList.toggle('active', b.dataset.year === year);
      });
    }

    function addBtn(label, val) {
      var b = document.createElement('button');
      b.textContent = label;
      b.dataset.year = val;
      b.addEventListener('click', function () { show(val); });
      bar.appendChild(b);
    }

    addBtn('All', 'All');
    groups.forEach(function (g) { addBtn(g.year, g.year); });
    show('All');
  }
  if (document.readyState !== 'loading') init();
  else document.addEventListener('DOMContentLoaded', init);
})();
</script>

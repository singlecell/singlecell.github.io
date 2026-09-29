---
ref: publications
layout: page
permalink: /publications/
title: publications
description:
nav: true
nav_order: 3
---

{% include publications_style.liquid %}

{% include bib_search.liquid %}

<div id="year-filter"></div>

<div class="publications">

{% bibliography %}

</div>

{% include publications_script.liquid %}

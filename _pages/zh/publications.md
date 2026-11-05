---
ref: publications
lang: zh
layout: page
permalink: /zh/publications/
title: 论文发表
description: 期刊论文，按发表时间倒序排列。
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

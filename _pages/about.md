---
layout: about
title: about
permalink: /
subtitle: Ph.D., Associate Professor<br>Institute of Chinese Materia Medica, <a href='https://www.shutcm.edu.cn/'>Shanghai University of Traditional Chinese Medicine</a>

profile:
  align: right
  image: prof_pic.svg
  image_circular: true # crops the image to make it circular
  more_info: >
    <p>linnanli@shutcm.edu.cn</p>

selected_papers: true # includes a list of papers marked as "selected={true}"
social: true # includes social icons at the bottom of the page

announcements:
  enabled: false # news section removed

latest_posts:
  enabled: false
---

<style>
/* Bold the family name (Li) instead of the given name (Linnan) */
.post-header .post-title,
#navbar .navbar-brand.title { font-weight: 700 !important; }
.post-header .post-title .font-weight-bold,
#navbar .navbar-brand .font-weight-bold { font-weight: 400 !important; }

/* ===== Full-screen hero (assembled by the script below) ===== */
.hero {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 4rem;
  min-height: calc(100vh - 8rem);
  margin-bottom: 3rem;
}
.hero-left { min-width: 0; max-width: 36rem; }
.hero-right { justify-self: end; }
.hero .post-header { margin: 0 0 1.4rem; text-align: left !important; }
.hero .post-header .post-title {
  font-size: clamp(2.6rem, 6vw, 4rem); line-height: 1.05; margin: 0 0 0.9rem;
  text-wrap: balance;
}
.hero .post-header .desc, .hero .post-header p {
  font-size: 1.2rem; line-height: 1.5; color: var(--global-text-color); opacity: 0.85; margin: 0;
  text-wrap: pretty;
}
.hero-intro p {
  font-size: 1.05rem; line-height: 1.65; max-width: 34rem;
  color: var(--global-text-color); margin: 0 0 0.8rem;
  text-wrap: pretty;
}
.hero-intro p:last-child { opacity: 0.7; font-size: 0.95rem; }
.hero-actions { display: flex; flex-wrap: wrap; gap: 0.75rem; margin-top: 1.8rem; }
.hero-btn {
  display: inline-flex; align-items: center; gap: 0.45rem;
  padding: 0.6rem 1.25rem; border-radius: 8px; font-size: 0.95rem; font-weight: 500;
  text-decoration: none; transition: all 0.2s ease; cursor: pointer;
}
.hero-btn.primary { background: var(--global-theme-color); color: #fff; }
.hero-btn.primary:hover { filter: brightness(0.92); }
.hero-btn.secondary {
  color: var(--global-text-color);
  border: 1px solid var(--global-divider-color, rgba(128,128,128,0.3));
}
.hero-btn.secondary:hover { border-color: var(--global-theme-color); color: var(--global-theme-color); }
.hero-right .profile { float: none !important; margin: 0 !important; width: auto !important; }
.hero-right img { width: clamp(220px, 26vw, 320px); height: auto; }
.hero-right .more-info, .hero-right .address { display: none; }

@media (max-width: 768px) {
  .hero {
    grid-template-columns: 1fr; justify-items: center; text-align: center;
    min-height: auto; gap: 1.5rem; padding: 1.5rem 0 0.5rem;
  }
  .hero-left { text-align: center; max-width: 38rem; }
  .hero-right { order: -1; justify-self: center; }
  .hero .post-header { text-align: center !important; }
  .hero-intro p { margin-left: auto; margin-right: auto; }
  .hero-actions { justify-content: center; }
}

/* ===== Consistent section headings (match across the homepage) ===== */
#research-interests h2,
#end-section h2,
.post article > h2 {
  font-size: clamp(1.8rem, 4vw, 2.4rem); font-weight: 700; margin: 3.5rem 0 0.6rem;
  text-transform: capitalize;
}

/* ===== Research interests — card grid (liamcli "highlights" style) ===== */
#research-interests { margin-top: 3.5rem; }
#research-interests h2 { margin-top: 0; }
#research-interests .ri-intro {
  margin: 0 0 1.8rem; max-width: 46rem;
  color: var(--global-text-color); opacity: 0.85; line-height: 1.6;
}
.ri-cards { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1.5rem; }
@media (max-width: 768px) { .ri-cards { grid-template-columns: 1fr; } }
.ri-card {
  background: var(--global-card-bg-color, var(--global-bg-color, #fff));
  border: 1px solid var(--global-divider-color, rgba(128,128,128,0.18));
  border-radius: 14px; padding: 1.7rem 1.8rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}
.ri-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.08);
  border-color: var(--global-theme-color);
}
.ri-icon {
  width: 46px; height: 46px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  background: var(--global-theme-color); color: #fff; margin-bottom: 1.1rem;
}
.ri-icon svg { width: 24px; height: 24px; }
.ri-card h3 { font-size: 1.2rem; font-weight: 700; margin: 0 0 0.4rem; color: var(--global-text-color); }
.ri-card .ri-sub { font-size: 0.85rem; font-weight: 500; color: var(--global-theme-color); margin: 0 0 0.7rem; }
.ri-card .ri-desc { font-size: 0.95rem; line-height: 1.6; margin: 0; color: var(--global-text-color); opacity: 0.8; }

/* ===== Each block fills one screen ===== */
.full-section {
  min-height: 100vh;
  display: flex; flex-direction: column; justify-content: center;
  padding: 5rem 0; box-sizing: border-box;
}
#research-interests.full-section { margin-top: 0; }

/* ===== Affiliations & Contact (relocated to the end) ===== */
#end-section h2 { margin-top: 0 !important; }
.contact-grid {
  display: grid; grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 2rem 3rem; margin-top: 0.5rem;
}
@media (max-width: 768px) { .contact-grid { grid-template-columns: 1fr; } }
.contact-grid h4 { font-size: 1.05rem; font-weight: 600; margin: 0 0 0.6rem; color: var(--global-text-color); }
.contact-grid p { margin: 0; line-height: 1.75; color: var(--global-text-color); opacity: 0.85; }
#end-section .social { margin-top: 2.2rem; text-align: left; }
@media (max-width: 768px) { #end-section .social { text-align: center; } }
</style>

<div id="hero-intro">
<p>I develop new mass spectrometry, chromatography, and sample-pretreatment technologies for the precise analysis of complex natural-medicine systems.</p>
<p>Ph.D. in analytical chemistry from Peking University &middot; B.S. in chemistry from Sichuan University.</p>
</div>

<div id="hero-actions">
<a class="hero-btn primary" href="mailto:linnanli@shutcm.edu.cn">&#9993;&nbsp; Email</a>
<a class="hero-btn secondary" href="{{ '/publications/' | relative_url }}">Publications</a>
</div>

<div id="research-interests" class="full-section">
<h2>Research Interests</h2>
<p class="ri-intro">My work spans the full chain of natural-medicine analysis — from discovering and characterizing active constituents, to decoding their molecular mechanisms, to safeguarding product quality and safety.</p>

<div class="ri-cards">
  <div class="ri-card">
    <div class="ri-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6"/><path d="M10 3v6l-5.4 9.3A1.5 1.5 0 0 0 5.9 21h12.2a1.5 1.5 0 0 0 1.3-2.7L14 9V3"/><path d="M7 14h10"/></svg></div>
    <h3>Analytical Technology Innovation</h3>
    <p class="ri-sub">Mass Spectrometry · Chromatography · Sample Pretreatment</p>
    <p class="ri-desc">Developing new mass spectrometry, chromatography, and sample-pretreatment methods for the precise analysis of complex natural-medicine systems.</p>
  </div>
  <div class="ri-card">
    <div class="ri-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg></div>
    <h3>Active Ingredient Discovery</h3>
    <p class="ri-sub">Natural Products</p>
    <p class="ri-desc">Discovery and structural characterization of bioactive constituents in traditional Chinese medicines.</p>
  </div>
  <div class="ri-card">
    <div class="ri-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2"/></svg></div>
    <h3>Targeting Analysis &amp; Metabolomics</h3>
    <p class="ri-sub">Metabolomics · Molecular Targeting</p>
    <p class="ri-desc">Endogenous molecular targeting analysis and metabolomics to unravel mechanisms of action.</p>
  </div>
  <div class="ri-card">
    <div class="ri-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7 3v6c0 4.6-3.1 7.6-7 9-3.9-1.4-7-4.4-7-9V6z"/><path d="m9 12 2 2 4-4"/></svg></div>
    <h3>Quality Control &amp; Safety</h3>
    <p class="ri-sub">Green Chemistry · Quality Control</p>
    <p class="ri-desc">Green-chemistry strategies plus the quality control and safety evaluation of natural products.</p>
  </div>
</div>
</div>

<div id="end-section" class="full-section">
<h2>Affiliations &amp; Contact</h2>
<div class="contact-grid">
  <div>
    <h4>Affiliations</h4>
    <p>State Key Laboratory of Discovery and Utilization of Functional Components in Traditional Chinese Medicine<br>
    MOE Key Laboratory of Standardization of Chinese Medicines<br>
    SATCM Key Laboratory of New Resources and Quality Evaluation of Chinese Medicines<br>
    Shanghai Key Laboratory of Compound Chinese Medicines</p>
  </div>
  <div>
    <h4>Contact</h4>
    <p>Room 908, International Center for Standardization of Chinese Medicine<br>
    1200 Cailun Road, Zhangjiang Hi-Tech Park, Pudong District, Shanghai 201203, China<br>
    Tel: +86-21-51322417<br>
    Email: <a href="mailto:linnanli@shutcm.edu.cn">linnanli@shutcm.edu.cn</a></p>
  </div>
</div>
</div>

<script>
(function () {
  function build() {
    var article = document.querySelector('.post article') || document.querySelector('article');
    if (!article) return;

    // 1) Assemble the full-screen hero from the name header, intro, actions and photo.
    if (!document.querySelector('.hero')) {
      var header = document.querySelector('.post-header');
      var profile = article.querySelector('.profile');
      var intro = document.getElementById('hero-intro');
      var actions = document.getElementById('hero-actions');
      if (header && profile) {
        var hero = document.createElement('div'); hero.className = 'hero';
        var left = document.createElement('div'); left.className = 'hero-left';
        var right = document.createElement('div'); right.className = 'hero-right';
        left.appendChild(header);
        if (intro) left.appendChild(intro);
        if (actions) left.appendChild(actions);
        right.appendChild(profile);
        hero.appendChild(left);
        hero.appendChild(right);
        article.insertBefore(hero, article.firstChild);
      }
    }

    // 2) Move the affiliations/contact section (and the social icons) to the very end.
    var end = document.getElementById('end-section');
    if (end && !end.dataset.moved) {
      article.appendChild(end);
      var social = article.querySelector('.social');
      if (social) end.appendChild(social);
      end.dataset.moved = '1';
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build);
  else build();
})();
</script>

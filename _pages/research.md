---
layout: page
permalink: /research/
title: Research
description: Two complementary directions — in situ mass spectrometry and precision profiling of natural medicines.
nav: true
nav_order: 1
---

<style>
/* keep the family name bold in the navbar on this page too */
#navbar .navbar-brand.title { font-weight: 700 !important; }
#navbar .navbar-brand .font-weight-bold { font-weight: 400 !important; }

.research-intro {
  max-width: 46rem; margin: 0 0 3rem;
  font-size: 1.1rem; line-height: 1.75;
  color: var(--global-text-color); opacity: 0.88; text-wrap: pretty;
}

.research-area { margin: 0 0 4rem; }
.research-area:last-child { margin-bottom: 1rem; }

.ra-head { display: flex; align-items: flex-start; gap: 1.1rem; margin-bottom: 1rem; }
.ra-icon {
  flex: 0 0 auto; width: 52px; height: 52px; border-radius: 13px;
  display: flex; align-items: center; justify-content: center;
  background: var(--global-theme-color); color: #fff;
}
.ra-icon svg { width: 28px; height: 28px; }
.ra-head h2 {
  font-size: clamp(1.6rem, 3.6vw, 2.1rem); font-weight: 700;
  margin: 0.1rem 0 0.15rem; line-height: 1.2; text-transform: none;
}
.ra-head .ra-en { font-size: 0.9rem; font-weight: 500; color: var(--global-theme-color); margin: 0; letter-spacing: 0.02em; }

.ra-lead {
  max-width: 48rem; margin: 0 0 1.6rem;
  font-size: 1rem; line-height: 1.85;
  color: var(--global-text-color); opacity: 0.85; text-wrap: pretty;
}

.ra-cards { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1.2rem; }
@media (max-width: 768px) { .ra-cards { grid-template-columns: 1fr; } }
.ra-card {
  background: var(--global-card-bg-color, var(--global-bg-color, #fff));
  border: 1px solid var(--global-divider-color, rgba(128,128,128,0.18));
  border-radius: 12px; padding: 1.3rem 1.45rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}
.ra-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.08);
  border-color: var(--global-theme-color);
}
.ra-card h3 { font-size: 1.05rem; font-weight: 700; margin: 0 0 0.4rem; color: var(--global-text-color); }
.ra-card p { font-size: 0.93rem; line-height: 1.75; margin: 0; color: var(--global-text-color); opacity: 0.8; }

.ra-tags { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1.3rem; }
.ra-tag {
  font-size: 0.8rem; padding: 0.3rem 0.7rem; border-radius: 999px;
  border: 1px solid var(--global-divider-color, rgba(128,128,128,0.28));
  color: var(--global-text-color); opacity: 0.85;
}
</style>

<p class="research-intro">
My research develops new analytical chemistry methods — centered on mass spectrometry and combined with chromatographic separation and sample preparation — to enable the precise analysis of complex natural-medicine systems. It unfolds along two complementary directions: <strong>in situ mass spectrometry</strong> brings the measurement to where the sample is, while <strong>precision profiling of natural medicines</strong> clarifies what the sample actually contains.
</p>

<div class="research-area">
  <div class="ra-head">
    <div class="ra-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h4l2 5 4-14 2 9h6"/></svg>
    </div>
    <div>
      <h2>In Situ Mass Spectrometry</h2>
      <p class="ra-en">Bringing the measurement to the sample</p>
    </div>
  </div>

  <p class="ra-lead">
    Developing ambient, miniaturized, and imaging mass spectrometry that analyzes samples in their native state with little or no sample preparation. By combining direct ionization with portable instruments and spatially resolved acquisition, these platforms move analysis out of the lab and into the field — enabling on-site authentication of precious and toxic medicinal materials and revealing how components are truly distributed within tissues.
  </p>

  <div class="ra-cards">
    <div class="ra-card">
      <h3>Ambient ionization</h3>
      <p>DART, paper/capillary spray, thin-layer chromatography–MS (TLC–MS), and liquid extraction surface analysis (LESA) ionize natural products directly from TLC plates, surfaces, and raw materials.</p>
    </div>
    <div class="ra-card">
      <h3>Miniaturized & portable MS</h3>
      <p>Field-deployable miniature mass spectrometers coupled with machine learning for rapid on-site identification and authentication.</p>
    </div>
    <div class="ra-card">
      <h3>Mass spectrometry imaging</h3>
      <p>Spatially resolved imaging of constituents and metabolites in plant and animal tissues, linking chemical information to biological processes.</p>
    </div>
    <div class="ra-card">
      <h3>Rapid ID & safety</h3>
      <p>On-site screening of precious materials such as agarwood, sandalwood, and aged tangerine peel, plus rapid detection of toxic constituents like pyrrolizidine alkaloids.</p>
    </div>
  </div>

  <div class="ra-tags">
    <span class="ra-tag">DART-MS</span>
    <span class="ra-tag">Paper/capillary spray</span>
    <span class="ra-tag">TLC–MS</span>
    <span class="ra-tag">LESA-MS</span>
    <span class="ra-tag">LA-DART-MS</span>
    <span class="ra-tag">Miniature MS</span>
    <span class="ra-tag">MS imaging</span>
  </div>
</div>

<div class="research-area">
  <div class="ra-head">
    <div class="ra-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/></svg>
    </div>
    <div>
      <h2>Precision Profiling of Natural Medicines</h2>
      <p class="ra-en">Clarifying what the sample contains</p>
    </div>
  </div>

  <p class="ra-lead">
    Building multidimensional, integrated strategies that resolve complex natural-medicine systems from constituents to mechanisms. By combining high-resolution and ion-mobility LC–MS (LC–MS / IM-MS), targeted and pseudo-targeted metabolomics, and spatial lipidomics, this work comprehensively characterizes chemical composition, tracks how components transform during processing and in vivo metabolism, and connects them to bioactivity, quality, and safety.
  </p>

  <div class="ra-cards">
    <div class="ra-card">
      <h3>Comprehensive characterization</h3>
      <p>An integrated "3M" workflow with LC–MS / IM-MS structural elucidation accelerates the identification and annotation of complex multi-component systems.</p>
    </div>
    <div class="ra-card">
      <h3>Profiling & transformation</h3>
      <p>Tracking constituent diversity and its active transformations, such as the dynamic changes of ginsenosides during decoction and processing.</p>
    </div>
    <div class="ra-card">
      <h3>Metabolomics & mechanism</h3>
      <p>Targeted, pseudo-targeted, and spatial metabolomics/lipidomics reveal molecular markers and mechanisms of action.</p>
    </div>
    <div class="ra-card">
      <h3>Quality control & safety</h3>
      <p>Green sample preparation and quantitative strategies support quality control, attribution analysis, and safety evaluation of multi-herb formulations.</p>
    </div>
  </div>

  <div class="ra-tags">
    <span class="ra-tag">3M strategy</span>
    <span class="ra-tag">High-resolution LC–MS</span>
    <span class="ra-tag">Ion-mobility MS</span>
    <span class="ra-tag">Targeted metabolomics</span>
    <span class="ra-tag">Spatial lipidomics</span>
    <span class="ra-tag">Network pharmacology</span>
    <span class="ra-tag">Quality control</span>
  </div>
</div>

<p class="research-intro" style="margin-top: 2.5rem; font-size: 1rem;">
  For representative work in both directions, see my <a href="{{ '/publications/' | relative_url }}">publications</a>.
</p>

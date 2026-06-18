---
layout: page
permalink: /research/
title: 研究方向
description: 两个相辅相成的方向——原位质谱与天然药物精准解析。
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
我的研究致力于发展新的分析化学方法——以质谱为核心，结合色谱分离与样品前处理技术——以实现对复杂天然药物体系的精准解析。研究沿两个相辅相成的方向展开：用<strong>原位质谱</strong>把测量带到样品现场，用<strong>天然药物精准解析</strong>厘清样品中究竟含有什么。
</p>

<div class="research-area">
  <div class="ra-head">
    <div class="ra-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h4l2 5 4-14 2 9h6"/></svg>
    </div>
    <div>
      <h2>原位质谱</h2>
      <p class="ra-en">In Situ Mass Spectrometry</p>
    </div>
  </div>

  <p class="ra-lead">
    发展常压敞开式、小型化与质谱成像技术，在样品所处的原位状态下、几乎无需前处理即可完成分析。通过将直接电离与便携式仪器、空间分辨采集相结合，这类平台把分析从实验室带到现场，实现对名贵与有毒药材的现场鉴别，并直观呈现成分在组织中的真实分布。
  </p>

  <div class="ra-cards">
    <div class="ra-card">
      <h3>常压敞开式电离</h3>
      <p>DART、纸喷雾/毛细管喷雾、薄层色谱-质谱（TLC–MS）与表面液体萃取（LESA）等技术，直接从薄层板、表面及原料中电离天然产物。</p>
    </div>
    <div class="ra-card">
      <h3>小型化与便携质谱</h3>
      <p>结合机器学习的现场可部署小型质谱，用于快速的现场识别与真伪鉴别。</p>
    </div>
    <div class="ra-card">
      <h3>质谱成像</h3>
      <p>在植物与动物组织中对成分和代谢物进行空间分辨成像，将化学信息与生物学过程相联系。</p>
    </div>
    <div class="ra-card">
      <h3>快速鉴别与安全性</h3>
      <p>对沉香、檀香、陈皮等名贵药材进行现场筛查，并快速检测吡咯里西啶类生物碱等有毒成分。</p>
    </div>
  </div>

  <div class="ra-tags">
    <span class="ra-tag">DART-MS</span>
    <span class="ra-tag">纸喷雾/毛细管喷雾</span>
    <span class="ra-tag">TLC–MS</span>
    <span class="ra-tag">LESA-MS</span>
    <span class="ra-tag">LA-DART-MS</span>
    <span class="ra-tag">小型质谱</span>
    <span class="ra-tag">质谱成像</span>
  </div>
</div>

<div class="research-area">
  <div class="ra-head">
    <div class="ra-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/></svg>
    </div>
    <div>
      <h2>天然药物精准解析</h2>
      <p class="ra-en">Precision Profiling of Natural Medicines</p>
    </div>
  </div>

  <p class="ra-lead">
    构建多维度、一体化的整合策略，对复杂天然药物体系实现从成分到机制的系统解析。综合运用高分辨与离子淌度液质联用（LC–MS / IM-MS）、靶向与拟靶向代谢组学以及空间脂质组学，全面表征化学组成，追踪成分在炮制与体内代谢过程中的转化，并将其与生物活性、质量及安全性相关联。
  </p>

  <div class="ra-cards">
    <div class="ra-card">
      <h3>成分全面表征</h3>
      <p>基于一体化"3M"工作流与 LC-MS / IM-MS 结构解析，加速复杂多组分体系的成分鉴定与注释。</p>
    </div>
    <div class="ra-card">
      <h3>成分谱与转化追踪</h3>
      <p>追踪成分多样性及其活性转化，如人参皂苷在煎煮与炮制过程中的动态变化。</p>
    </div>
    <div class="ra-card">
      <h3>代谢组学与机制</h3>
      <p>运用靶向、拟靶向及空间代谢组学/脂质组学，揭示分子标志物与作用机制。</p>
    </div>
    <div class="ra-card">
      <h3>质量控制与安全性</h3>
      <p>发展绿色样品前处理与定量策略，服务于复方制剂的质量控制、归属解析与安全性评价。</p>
    </div>
  </div>

  <div class="ra-tags">
    <span class="ra-tag">3M 策略</span>
    <span class="ra-tag">高分辨 LC–MS</span>
    <span class="ra-tag">离子淌度质谱</span>
    <span class="ra-tag">靶向代谢组学</span>
    <span class="ra-tag">空间脂质组学</span>
    <span class="ra-tag">网络药理学</span>
    <span class="ra-tag">质量控制</span>
  </div>
</div>

<p class="research-intro" style="margin-top: 2.5rem; font-size: 1rem;">
  两个方向的代表性工作，详见我的<a href="{{ '/publications/' | relative_url }}">论文发表</a>。
</p>

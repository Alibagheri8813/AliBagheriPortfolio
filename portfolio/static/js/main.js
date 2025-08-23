/* Utilities */
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

function getCsrf() {
  const m = document.cookie.match(/csrftoken=([^;]+)/);
  return m ? decodeURIComponent(m[1]) : "";
}

/* Theme toggle (persist) */
(function themeInit() {
  try {
    const saved = localStorage.getItem("theme");
    if (saved) document.documentElement.setAttribute("data-theme", saved);
  } catch {}
})();
function toggleTheme() {
  const cur = document.documentElement.getAttribute("data-theme") === "light" ? "dark" : "light";
  document.documentElement.setAttribute("data-theme", cur);
  try { localStorage.setItem("theme", cur); } catch {}
}

/* Intersection reveal + progress bars */
function setupReveals() {
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        const bars = $$(".bar > span", e.target);
        bars.forEach(b => requestAnimationFrame(() => b.style.width = b.dataset.w + "%"));
      }
    });
  }, { threshold: 0.3 });
  $$(".skill").forEach(el => obs.observe(el));
}

/* Parallax hero */
function setupParallax() {
  const hero = $(".hero");
  if (!hero) return;
  let y = 0;
  function tick() {
    y += (window.scrollY - y) * 0.06;
    hero.style.transform = `translateY(${y * 0.04}px)`;
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

/* Case study modal with deep links */
function setupProjectModals() {
  const dialog = document.createElement("dialog");
  dialog.className = "modal";
  dialog.innerHTML = `<div class="panel" role="dialog" aria-modal="true"><button class="btn" data-close>Close</button><div class="content"></div></div>`;
  document.body.appendChild(dialog);

  function openModal(slug) {
    fetch(`/projects/${slug}/?partial=1`).then(r => r.text()).then(html => {
      $(".content", dialog).innerHTML = html;
      if (!dialog.open) dialog.showModal();
      history.pushState({ modal: slug }, "", `/projects/${slug}/`);
    });
  }
  function closeModal() {
    if (dialog.open) dialog.close();
    history.pushState({}, "", "/projects/");
  }

  document.addEventListener("click", (e) => {
    const card = e.target.closest("[data-project-slug]");
    if (card && card.dataset.url) {
      e.preventDefault();
      openModal(card.dataset.projectSlug);
    }
    if (e.target.matches("[data-close]")) {
      e.preventDefault();
      closeModal();
    }
  });

  window.addEventListener("popstate", (e) => {
    if (!e.state?.modal) closeModal();
  });

  // Deep-link open if already on detail page and we have partial route fallbacks
  const detailSlug = document.body.dataset.detailSlug;
  if (detailSlug) {
    // Enhance SSR page with modal route navigation
    // No-op by default
  }
}

/* Simple lightbox */
function setupLightbox() {
  const overlay = document.createElement("div");
  overlay.className = "lightbox-open";
  overlay.innerHTML = `<img alt="Preview" />`;
  document.body.appendChild(overlay);
  document.addEventListener("click", (e) => {
    const img = e.target.closest("[data-lightbox]");
    if (img && img.src) {
      overlay.querySelector("img").src = img.src;
      overlay.setAttribute("open", "");
    }
    if (e.target === overlay) overlay.removeAttribute("open");
  });
}

/* Client-side search (instant) */
function setupSearch() {
  const input = $("#search");
  const list = $("#search-results");
  if (!input || !list) return;
  let t = null;
  input.addEventListener("input", () => {
    clearTimeout(t);
    t = setTimeout(async () => {
      const q = input.value.trim();
      if (!q) { list.innerHTML = ""; return; }
      const res = await fetch(`/api/search/?q=${encodeURIComponent(q)}`).then(r => r.json());
      list.innerHTML = `
        <div><strong>Projects</strong>${res.projects.map(p => `<div><a href="/projects/${p.slug}/">${p.title}</a></div>`).join("")}</div>
        <div style="margin-top:8px;"><strong>Blog</strong>${res.posts.map(p => `<div><a href="/blog/${p.slug}/">${p.title}</a></div>`).join("")}</div>
      `;
    }, 160);
  });
}

/* AJAX contact form */
function setupContact() {
  const form = $("#contact-form");
  if (!form) return;
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = new FormData(form);
    const res = await fetch("/contact/", {
      method: "POST",
      headers: { "X-CSRFToken": getCsrf(), "X-Requested-With": "XMLHttpRequest" },
      body: data
    });
    const json = await res.json();
    const msg = $("#contact-message");
    msg.textContent = json.message || (json.ok ? "Thanks!" : "Please fix the errors.");
    msg.style.color = json.ok ? "var(--ok)" : "var(--err)";
  });
}

/* Analytics consent */
function setupConsent() {
  const GA = document.body.dataset.ga || "";
  const banner = $(".consent");
  const ok = localStorage.getItem("consent-analytics");
  if (!GA) return; // disabled
  function loadGA() {
    if (window.dataLayer) return;
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);} window.gtag = gtag;
    gtag('js', new Date()); gtag('config', GA);
    const s = document.createElement("script");
    s.async = true; s.src = `https://www.googletagmanager.com/gtag/js?id=${GA}`;
    document.head.appendChild(s);
  }
  if (ok === "yes") loadGA();
  else if (banner) {
    banner.classList.add("show");
    $("#consent-accept").addEventListener("click", () => {
      localStorage.setItem("consent-analytics", "yes");
      banner.remove();
      loadGA();
    });
    $("#consent-decline").addEventListener("click", () => {
      localStorage.setItem("consent-analytics", "no");
      banner.remove();
    });
  }
}

/* Theme toggle button */
document.addEventListener("click", (e) => {
  if (e.target.closest("#theme-toggle")) {
    e.preventDefault(); toggleTheme();
  }
});

document.addEventListener("DOMContentLoaded", () => {
  setupReveals();
  setupParallax();
  setupProjectModals();
  setupLightbox();
  setupSearch();
  setupContact();
  setupConsent();
});
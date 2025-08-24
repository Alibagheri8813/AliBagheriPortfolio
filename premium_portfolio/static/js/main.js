document.addEventListener("DOMContentLoaded", function () {
  var yearEl = document.querySelector("[data-year]");
  if (yearEl) { yearEl.textContent = String(new Date().getFullYear()); }
  console.debug("static/js/main.js loaded");
});

/* Admin : catégories (Ajouter, Contributions, File d'attente, Versions) et filtres de listes.
   Un seul bloc est affiché à la fois ; le choix est gardé dans l'adresse (#contributions…) et sur l'appareil.
   Ne touche à aucune donnée : seulement l'affichage. */
(function () {
  "use strict";
  var KEY = "onrecord:admin-cat";
  var CATS = ["ajouter", "contributions", "file", "versions"];
  function $(id) { return document.getElementById(id); }
  function pick(cat) {
    if (CATS.indexOf(cat) < 0) cat = "ajouter";
    document.querySelectorAll("[data-cat-pane]").forEach(function (el) {
      el.classList.toggle("cat-off", el.getAttribute("data-cat-pane") !== cat);
    });
    document.querySelectorAll("#cats button").forEach(function (b) {
      b.setAttribute("aria-selected", b.getAttribute("data-cat") === cat ? "true" : "false");
    });
    try { localStorage.setItem(KEY, cat); } catch (e) {}
    try { history.replaceState(null, "", "#" + cat); } catch (e) {}
    var active = document.querySelector('#cats button[aria-selected="true"]');
    if (active && active.scrollIntoView) { try { active.scrollIntoView({ block: "nearest", inline: "center" }); } catch (e) {} }
  }
  function applyFilter(input) {
    var box = document.querySelector(input.getAttribute("data-filter"));
    if (!box) return;
    var q = input.value.trim().toLowerCase();
    var items = box.querySelectorAll(".pv");
    var shown = 0;
    items.forEach(function (it) {
      var ok = !q || it.textContent.toLowerCase().indexOf(q) >= 0;
      it.hidden = !ok;
      if (ok) shown++;
    });
    box.querySelectorAll("details.sec").forEach(function (d) {
      if (q && d.querySelector(".pv:not([hidden])")) d.open = true;
    });
    var note = box.parentNode.querySelector(".filter-none[data-for=\"" + box.id + "\"]");
    if (q && items.length && !shown) {
      if (!note) {
        note = document.createElement("p");
        note.className = "hint filter-none"; note.setAttribute("data-for", box.id);
        note.textContent = "Rien ne correspond.";
        box.parentNode.insertBefore(note, box.nextSibling);
      }
    } else if (note) note.remove();
  }
  function boot() {
    var nav = $("cats");
    if (!nav) return;
    nav.addEventListener("click", function (ev) {
      var b = ev.target.closest && ev.target.closest("button[data-cat]");
      if (b) { pick(b.getAttribute("data-cat")); window.scrollTo(0, 0); }
    });
    var start = (location.hash || "").replace("#", "");
    if (CATS.indexOf(start) < 0) { try { start = localStorage.getItem(KEY) || ""; } catch (e) { start = ""; } }
    pick(start);
    document.querySelectorAll("input[data-filter]").forEach(function (inp) {
      inp.addEventListener("input", function () { applyFilter(inp); });
      var box = document.querySelector(inp.getAttribute("data-filter"));
      if (box && window.MutationObserver) new MutationObserver(function () { if (inp.value) applyFilter(inp); }).observe(box, { childList: true });
    });
    window.addEventListener("hashchange", function () { pick((location.hash || "").replace("#", "")); });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();

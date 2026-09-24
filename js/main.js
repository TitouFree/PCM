/* Paris Carrelages et Matériaux — site statique (aucun backend) */
(function () {
  "use strict";

  /* ---------- menu mobile ---------- */
  var toggle = document.getElementById("navToggle");
  var mobile = document.getElementById("navMobile");
  if (toggle && mobile) {
    toggle.addEventListener("click", function () {
      toggle.classList.toggle("open");
      mobile.classList.toggle("open");
    });
  }

  /* ---------- révélations au scroll ---------- */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("visible"); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("visible"); });
  }

  /* ---------- modale devis (solution mailto, sans serveur) ---------- */
  var modal = document.getElementById("devisModal");
  var chips = [];
  function openModal() { if (modal) { modal.classList.add("open"); document.body.style.overflow = "hidden"; } }
  function closeModal() { if (modal) { modal.classList.remove("open"); document.body.style.overflow = ""; } }
  document.querySelectorAll("[data-open-devis]").forEach(function (b) {
    b.addEventListener("click", function (e) { e.preventDefault(); openModal(); });
  });
  if (modal) {
    modal.addEventListener("click", function (e) { if (e.target === modal) closeModal(); });
    var closeBtn = document.getElementById("devisClose");
    if (closeBtn) closeBtn.addEventListener("click", closeModal);
    modal.querySelectorAll(".chip").forEach(function (chip) {
      chip.addEventListener("click", function () {
        chip.classList.toggle("on");
        var v = chip.getAttribute("data-value");
        if (chip.classList.contains("on")) { chips.push(v); } else { chips = chips.filter(function (x) { return x !== v; }); }
      });
    });
    var form = document.getElementById("devisForm");
    if (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var g = function (id) { var el = document.getElementById(id); return el ? el.value.trim() : ""; };
        var nom = g("dNom"), profil = g("dProfil"), tel = g("dTel"), email = g("dEmail");
        var adresse = g("dAdresse"), delai = g("dDelai"), message = g("dMessage");
        var lignes = [
          "Nom : " + nom,
          "Profil : " + profil,
          "Téléphone : " + tel,
          "E-mail : " + email,
          "Familles concernées : " + (chips.length ? chips.join(", ") : "Non précisé"),
          "Adresse du chantier : " + (adresse || "Non précisée"),
          "Délai souhaité : " + (delai || "Non précisé"),
          "",
          "Message :",
          message,
          "",
          "— Envoyé depuis le site pariscarrelages.fr (GitHub Pages)"
        ];
        var href = "mailto:snpariscm@gmail.com"
          + "?subject=" + encodeURIComponent("Demande de devis — " + nom)
          + "&body=" + encodeURIComponent(lignes.join("\n"));
        window.location.href = href;
        var note = document.getElementById("devisNote");
        if (note) note.classList.add("show");
      });
    }
  }

  /* ---------- visionneuse PDF (lecteur natif du navigateur) ---------- */
  var frame = document.getElementById("pdfFrame");
  if (frame) {
    var DOCS = {
      courte: { file: "documents/PCM_Plaquette_Courte.pdf", pages: 8 },
      complete: { file: "documents/PCM_Plaquette_Complete.pdf", pages: 56 },
      catalogue: { file: "documents/Catalogue_General_PCM.pdf", pages: 37 },
      magazine: { file: "documents/Ebauche_Magazine_PCM.pdf", pages: 4 }
    };
    var params = new URLSearchParams(window.location.search);
    var current = DOCS[params.get("doc")] ? params.get("doc") : "catalogue";
    var page = parseInt(params.get("page") || "1", 10) || 1;
    var zoom = 100;
    var indicator = document.getElementById("viewerIndicator");
    var zoomLabel = document.getElementById("viewerZoom");
    var openRaw = document.getElementById("viewerOpenRaw");

    function render() {
      var d = DOCS[current];
      page = Math.min(Math.max(1, page), d.pages);
      frame.src = d.file + "#page=" + page + "&zoom=" + zoom;
      if (openRaw) openRaw.href = d.file;
      if (indicator) indicator.textContent = "Page " + page + " / " + d.pages;
      if (zoomLabel) zoomLabel.textContent = zoom + " %";
      document.querySelectorAll(".doc-tab").forEach(function (t) {
        t.classList.toggle("active", t.getAttribute("data-doc") === current);
      });
      var idx = document.getElementById("catIndex");
      if (idx) idx.style.display = current === "catalogue" ? "" : "none";
    }
    document.querySelectorAll(".doc-tab").forEach(function (t) {
      t.addEventListener("click", function () { current = t.getAttribute("data-doc"); page = 1; zoom = 100; render(); });
    });
    var prev = document.getElementById("viewerPrev");
    var next = document.getElementById("viewerNext");
    var zin = document.getElementById("zoomIn");
    var zout = document.getElementById("zoomOut");
    if (prev) prev.addEventListener("click", function () { page -= 1; render(); });
    if (next) next.addEventListener("click", function () { page += 1; render(); });
    if (zin) zin.addEventListener("click", function () { zoom = Math.min(250, zoom + 25); render(); });
    if (zout) zout.addEventListener("click", function () { zoom = Math.max(50, zoom - 25); render(); });
    document.querySelectorAll(".cat-jump").forEach(function (b) {
      b.addEventListener("click", function () {
        current = "catalogue";
        page = parseInt(b.getAttribute("data-page"), 10) || 1;
        render();
        frame.scrollIntoView({ behavior: "smooth", block: "center" });
      });
    });
    render();
  }
})();

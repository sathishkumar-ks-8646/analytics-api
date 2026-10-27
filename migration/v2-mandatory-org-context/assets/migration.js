/* ==========================================================================
   Mandatory Organization Context — migration guide behaviour
   Vanilla, no dependencies, no network calls. Every page stays completely
   usable with JavaScript switched off.
   ========================================================================== */
(function () {
  "use strict";

  var root = document.documentElement;
  var STORE = "za-migration-theme";

  /* ------------------------------------------------------------ theme ---- */

  function applyTheme(mode) {
    if (mode === "light" || mode === "dark") {
      root.setAttribute("data-theme", mode);
    } else {
      root.removeAttribute("data-theme");
    }
    var btn = document.getElementById("theme-toggle");
    if (btn) {
      var dark = root.getAttribute("data-theme") === "dark";
      btn.textContent = dark ? "◑" : "◐";
      btn.setAttribute("aria-label", dark ? "Switch to light theme" : "Switch to dark theme");
    }
  }

  try {
    applyTheme(localStorage.getItem(STORE));
  } catch (e) {
    /* storage blocked — the system preference stands */
  }

  document.addEventListener("click", function (ev) {
    var btn = ev.target.closest && ev.target.closest("#theme-toggle");
    if (!btn) { return; }
    var current = root.getAttribute("data-theme");
    if (!current) {
      current = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    }
    var next = current === "dark" ? "light" : "dark";
    applyTheme(next);
    try { localStorage.setItem(STORE, next); } catch (e) { /* ignore */ }
  });

  /* ------------------------------------------------------- mobile nav ---- */

  var navToggle = document.getElementById("nav-toggle");
  var sidebar = document.querySelector(".sidebar");
  if (navToggle && sidebar) {
    var isNarrow = function () { return window.matchMedia("(max-width: 880px)").matches; };
    var syncNav = function () {
      if (isNarrow()) {
        sidebar.hidden = true;
        navToggle.setAttribute("aria-expanded", "false");
      } else {
        sidebar.hidden = false;
      }
    };
    syncNav();
    window.addEventListener("resize", syncNav);
    navToggle.addEventListener("click", function () {
      var open = sidebar.hidden;
      sidebar.hidden = !open;
      navToggle.setAttribute("aria-expanded", String(open));
    });
  }

  /* -------------------------------------------------- copy to clipboard -- */

  Array.prototype.forEach.call(document.querySelectorAll("pre"), function (pre) {
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "copy-btn";
    btn.textContent = "Copy";
    btn.addEventListener("click", function () {
      /* drop shell prompts and unified-diff markers so the paste just runs */
      var text = pre.innerText
        .replace(/^\s*\$ /gm, "")
        .replace(/^[-+] (?=[A-Za-z{"[])/gm, "");
      var done = function () {
        btn.textContent = "Copied";
        setTimeout(function () { btn.textContent = "Copy"; }, 1400);
      };
      var failed = function () { btn.textContent = "Failed"; };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, failed);
      } else {
        var ta = document.createElement("textarea");
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand("copy"); done(); } catch (e) { failed(); }
        document.body.removeChild(ta);
      }
    });
    pre.appendChild(btn);
  });

  /* ------------------------------------------------------ table filter --- */

  var filter = document.getElementById("ep-filter");
  if (filter) {
    var counter = document.getElementById("ep-count");
    var rows = Array.prototype.slice.call(document.querySelectorAll("[data-ep]"));
    var empty = document.getElementById("ep-empty");
    var total = rows.length;

    rows.forEach(function (row) {
      row.dataset.haystack = row.textContent.toLowerCase().replace(/\s+/g, " ");
    });

    var runFilter = function () {
      var query = filter.value.trim().toLowerCase();
      var shown = 0;
      rows.forEach(function (row) {
        var hit = query === "" || row.dataset.haystack.indexOf(query) !== -1;
        row.hidden = !hit;
        if (hit) { shown++; }
      });
      if (counter) { counter.textContent = shown + " of " + total + " endpoints"; }
      if (empty) { empty.hidden = shown !== 0; }
    };

    filter.addEventListener("input", runFilter);
    filter.addEventListener("search", runFilter);
    runFilter();
  }

  /* --------------------------------------------------------- scrollspy --- */

  var tocLinks = Array.prototype.slice.call(document.querySelectorAll(".toc a[href^='#']"));
  if (tocLinks.length && "IntersectionObserver" in window) {
    var byId = {};
    var targets = [];
    tocLinks.forEach(function (link) {
      var el = document.getElementById(link.getAttribute("href").slice(1));
      if (el) { byId[el.id] = link; targets.push(el); }
    });

    var visible = {};
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) { visible[entry.target.id] = entry.isIntersecting; });
      var active = null;
      targets.forEach(function (target) {
        if (!active && visible[target.id]) { active = target; }
      });
      tocLinks.forEach(function (link) { link.classList.remove("is-active"); });
      if (active && byId[active.id]) { byId[active.id].classList.add("is-active"); }
    }, { rootMargin: "-76px 0px -70% 0px", threshold: 0 });

    targets.forEach(function (target) { observer.observe(target); });
  }
})();

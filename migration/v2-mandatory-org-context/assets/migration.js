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

  /* asset panels carry their own copy button in the action row */
  Array.prototype.forEach.call(document.querySelectorAll("pre:not(.asset__code)"), function (pre) {
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

  /* ------------------------------------------------------ agent assets --- */
  /* Copy, download and reveal the source of each shipped file. The text is
     inlined in the page at build time, so all three work with no server and
     no network — the guide opens straight from the filesystem. */

  function assetText(id) {
    var pre = document.getElementById(id);
    return pre ? pre.textContent : "";
  }

  function flash(btn, label, cls) {
    var original = btn.dataset.label || btn.textContent;
    btn.dataset.label = original;
    btn.textContent = label;
    btn.classList.add(cls);
    setTimeout(function () {
      btn.textContent = original;
      btn.classList.remove(cls);
    }, 1600);
  }

  Array.prototype.forEach.call(
    document.querySelectorAll("[data-asset-copy]"),
    function (btn) {
      btn.addEventListener("click", function () {
        var text = assetText(btn.getAttribute("data-asset-copy"));
        var ok = function () { flash(btn, "Copied", "is-done"); };
        var no = function () { flash(btn, "Failed", "is-failed"); };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(ok, no);
        } else {
          var ta = document.createElement("textarea");
          ta.value = text;
          document.body.appendChild(ta);
          ta.select();
          try { document.execCommand("copy"); ok(); } catch (e) { no(); }
          document.body.removeChild(ta);
        }
      });
    }
  );

  Array.prototype.forEach.call(
    document.querySelectorAll("[data-asset-download]"),
    function (btn) {
      btn.addEventListener("click", function () {
        var text = assetText(btn.getAttribute("data-asset-download"));
        var name = btn.getAttribute("data-filename") || "download.txt";
        try {
          var blob = new Blob([text], { type: "text/plain;charset=utf-8" });
          var url = URL.createObjectURL(blob);
          var a = document.createElement("a");
          a.href = url;
          a.download = name;
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          setTimeout(function () { URL.revokeObjectURL(url); }, 2000);
          flash(btn, "Saved", "is-done");
        } catch (e) {
          flash(btn, "Failed", "is-failed");
        }
      });
    }
  );

  Array.prototype.forEach.call(
    document.querySelectorAll("[data-asset-view]"),
    function (btn) {
      btn.addEventListener("click", function () {
        var pre = document.getElementById(btn.getAttribute("data-asset-view"));
        if (!pre) { return; }
        var open = pre.hidden;
        pre.hidden = !open;
        btn.setAttribute("aria-expanded", String(open));
        btn.textContent = open ? "Hide source" : "View source";
        btn.dataset.label = btn.textContent;
      });
    }
  );

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

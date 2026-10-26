/* Progressive enhancement only: the docs are fully usable without JS. */
(function () {
  'use strict';

  // -- theme ---------------------------------------------------------------
  var KEY = 'za-sdk-docs-theme';
  var root = document.documentElement;
  var stored = null;
  try { stored = localStorage.getItem(KEY); } catch (e) {}
  if (stored === 'light' || stored === 'dark') root.setAttribute('data-theme', stored);

  function systemDark() {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
  function currentTheme() {
    return root.getAttribute('data-theme') || (systemDark() ? 'dark' : 'light');
  }
  function paintToggle(btn) {
    var dark = currentTheme() === 'dark';
    btn.setAttribute('aria-pressed', String(dark));
    btn.querySelector('[data-theme-label]').textContent = dark ? 'Light' : 'Dark';
  }

  var toggle = document.querySelector('[data-theme-toggle]');
  if (toggle) {
    paintToggle(toggle);
    toggle.addEventListener('click', function () {
      var next = currentTheme() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem(KEY, next); } catch (e) {}
      paintToggle(toggle);
    });
  }

  // -- mobile navigation ---------------------------------------------------
  var rail = document.querySelector('.rail');
  var navBtn = document.querySelector('[data-nav-toggle]');
  var scrim = null;

  function closeNav() {
    if (!rail) return;
    rail.setAttribute('data-open', 'false');
    if (navBtn) { navBtn.setAttribute('aria-expanded', 'false'); navBtn.focus(); }
    if (scrim) { scrim.remove(); scrim = null; }
  }
  function openNav() {
    rail.setAttribute('data-open', 'true');
    navBtn.setAttribute('aria-expanded', 'true');
    scrim = document.createElement('button');
    scrim.className = 'scrim';
    scrim.setAttribute('aria-label', 'Close navigation');
    scrim.addEventListener('click', closeNav);
    document.body.appendChild(scrim);
    var first = rail.querySelector('a');
    if (first) first.focus();
  }
  if (navBtn && rail) {
    navBtn.addEventListener('click', function () {
      rail.getAttribute('data-open') === 'true' ? closeNav() : openNav();
    });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && rail && rail.getAttribute('data-open') === 'true') closeNav();
  });

  // -- copy buttons --------------------------------------------------------
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var code = btn.closest('figure').querySelector('code');
      if (!code) return;
      var done = function () {
        btn.textContent = 'Copied';
        btn.setAttribute('data-copied', '');
        setTimeout(function () {
          btn.textContent = 'Copy';
          btn.removeAttribute('data-copied');
        }, 1600);
      };
      if (navigator.clipboard) {
        navigator.clipboard.writeText(code.textContent).then(done, function () {});
      } else {
        var sel = window.getSelection();
        var range = document.createRange();
        range.selectNodeContents(code);
        sel.removeAllRanges(); sel.addRange(range);
        try { document.execCommand('copy'); done(); } catch (e) {}
        sel.removeAllRanges();
      }
    });
  });

  // -- "on this page" active marker ---------------------------------------
  var links = Array.prototype.slice.call(document.querySelectorAll('.index a[href^="#"]'));
  if (links.length && 'IntersectionObserver' in window) {
    var byId = {};
    links.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
    var targets = Object.keys(byId)
      .map(function (id) { return document.getElementById(id); })
      .filter(Boolean);
    var visible = new Set();
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) visible.add(en.target.id); else visible.delete(en.target.id);
      });
      links.forEach(function (a) { a.removeAttribute('aria-current'); });
      for (var i = 0; i < targets.length; i++) {
        if (visible.has(targets[i].id)) { byId[targets[i].id].setAttribute('aria-current', 'true'); break; }
      }
    }, { rootMargin: '-80px 0px -70% 0px' });
    targets.forEach(function (t) { io.observe(t); });
  }
})();

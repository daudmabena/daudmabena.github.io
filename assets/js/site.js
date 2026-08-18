/**
 * daudmabena.github.io
 *
 * Progressive enhancement only: the page is fully readable and navigable with
 * this file blocked. No dependencies, no build step.
 */
(function () {
  "use strict";

  var root = document.documentElement;

  /* ---- Colour theme --------------------------------------------------- */

  var STORAGE_KEY = "theme";

  function systemTheme() {
    return window.matchMedia("(prefers-color-scheme: light)").matches
      ? "light"
      : "dark";
  }

  function stored() {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch (error) {
      return null; // Private browsing can throw on access.
    }
  }

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    var toggle = document.querySelector(".theme-toggle");
    if (toggle) {
      toggle.setAttribute(
        "title",
        theme === "dark" ? "Switch to light theme" : "Switch to dark theme"
      );
    }
  }

  applyTheme(stored() || systemTheme());

  // Follow the system setting until the visitor states a preference.
  window
    .matchMedia("(prefers-color-scheme: light)")
    .addEventListener("change", function (event) {
      if (!stored()) applyTheme(event.matches ? "light" : "dark");
    });

  var themeToggle = document.querySelector(".theme-toggle");
  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      applyTheme(next);
      try {
        localStorage.setItem(STORAGE_KEY, next);
      } catch (error) {
        /* Nothing to do; the choice simply will not persist. */
      }
    });
  }

  /* ---- Mobile navigation ---------------------------------------------- */

  var navToggle = document.querySelector(".nav__toggle");
  var navList = document.getElementById("nav-list");

  if (navToggle && navList) {
    var setNav = function (open) {
      navToggle.setAttribute("aria-expanded", String(open));
      navList.classList.toggle("is-open", open);
    };

    navToggle.addEventListener("click", function () {
      setNav(navToggle.getAttribute("aria-expanded") !== "true");
    });

    navList.addEventListener("click", function (event) {
      if (event.target.closest("a")) setNav(false);
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") setNav(false);
    });
  }

  /* ---- Current section in the nav ------------------------------------- */

  var sections = Array.prototype.slice.call(
    document.querySelectorAll("main section[id]")
  );
  var navLinks = Array.prototype.slice.call(
    document.querySelectorAll('.nav__list a[href^="#"]')
  );

  if ("IntersectionObserver" in window && sections.length && navLinks.length) {
    var mark = function (id) {
      navLinks.forEach(function (link) {
        if (link.getAttribute("href") === "#" + id) {
          link.setAttribute("aria-current", "true");
        } else {
          link.removeAttribute("aria-current");
        }
      });
    };

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) mark(entry.target.id);
        });
      },
      // A band near the top of the viewport, so the highlight changes as a
      // heading reaches reading position rather than when it first appears.
      { rootMargin: "-25% 0px -70% 0px" }
    );
    sections.forEach(function (section) {
      observer.observe(section);
    });
  }

  /* ---- Reveal on scroll ----------------------------------------------- */

  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  if ("IntersectionObserver" in window && !reducedMotion.matches) {
    var targets = document.querySelectorAll(
      ".card, .project, .repo, .stack__group, .prose > p"
    );

    var revealObserver = new IntersectionObserver(
      function (entries, self) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          self.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.06 }
    );

    Array.prototype.forEach.call(targets, function (element, index) {
      element.classList.add("reveal");
      // A small stagger, capped so later items are not left waiting.
      element.style.transitionDelay = Math.min(index % 8, 5) * 40 + "ms";
      revealObserver.observe(element);
    });
  }

  /* ---- Footer year ---------------------------------------------------- */

  var year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());
})();

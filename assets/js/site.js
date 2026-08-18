/**
 * daudmabena.github.io — instrumentation
 *
 * Progressive enhancement only. With this file blocked the page is still fully
 * readable and navigable: every architecture description and technology usage
 * note is rendered server-side into the markup, and only the reveal behaviour
 * is added here. No dependencies.
 */
(function () {
  "use strict";

  var root = document.documentElement;
  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  /* ---- Paper / ink theme ------------------------------------------------ */

  var STORAGE_KEY = "theme";

  function systemTheme() {
    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "ink"
      : "paper";
  }

  function stored() {
    try {
      var value = localStorage.getItem(STORAGE_KEY);
      if (value === "dark") return "ink";
      if (value === "light") return "paper";
      return value;
    } catch (error) {
      return null; // Private browsing can throw on access.
    }
  }

  function applyTheme(theme) {
    var resolved = theme === "ink" ? "ink" : "paper";
    root.setAttribute("data-theme", resolved);
    var toggle = document.querySelector(".theme-toggle");
    if (toggle) {
      toggle.setAttribute(
        "title",
        resolved === "ink" ? "Switch to paper theme" : "Switch to ink theme"
      );
    }
  }

  applyTheme(stored() || systemTheme());

  window
    .matchMedia("(prefers-color-scheme: dark)")
    .addEventListener("change", function (event) {
      if (!stored()) applyTheme(event.matches ? "ink" : "paper");
    });

  var themeToggle = document.querySelector(".theme-toggle");
  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      var next =
        root.getAttribute("data-theme") === "ink" ? "paper" : "ink";
      applyTheme(next);
      try {
        localStorage.setItem(STORAGE_KEY, next);
      } catch (error) {
        /* The choice simply will not persist. */
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

    var navObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) mark(entry.target.id);
        });
      },
      { rootMargin: "-20% 0px -72% 0px" }
    );
    sections.forEach(function (section) {
      navObserver.observe(section);
    });
  }

  /* ---- Architecture diagram ------------------------------------------- */

  var flow = document.querySelector(".flow");
  var readout = document.querySelector("[data-readout]");

  if (flow) {
    var nodes = Array.prototype.slice.call(flow.querySelectorAll(".node"));
    var readoutDefault = readout ? readout.textContent : "";

    var byName = {};
    nodes.forEach(function (node) {
      byName[node.getAttribute("data-node")] = node;
    });

    var clearLinks = function () {
      flow.classList.remove("is-focusing");
      nodes.forEach(function (node) {
        node.classList.remove("is-linked");
      });
      if (readout) readout.textContent = readoutDefault;
    };

    var showLinks = function (node) {
      clearLinks();
      flow.classList.add("is-focusing");
      node.classList.add("is-linked");

      (node.getAttribute("data-links") || "")
        .split(/\s+/)
        .forEach(function (name) {
          if (byName[name]) byName[name].classList.add("is-linked");
        });

      if (readout) {
        readout.textContent =
          node.querySelector(".node__name").textContent.trim() +
          " — " +
          (node.getAttribute("data-desc") || "");
      }
    };

    nodes.forEach(function (node) {
      node.addEventListener("mouseenter", function () {
        showLinks(node);
      });
      node.addEventListener("focus", function () {
        showLinks(node);
      });
      node.addEventListener("mouseleave", clearLinks);
      node.addEventListener("blur", clearLinks);
    });
  }

  /* ---- Ink spread on panel hover -------------------------------------- */

  var panels = document.querySelectorAll(".panel");
  panels.forEach(function (panel) {
    panel.addEventListener("mousemove", function (event) {
      var rect = panel.getBoundingClientRect();
      var x = ((event.clientX - rect.left) / rect.width) * 100;
      var y = ((event.clientY - rect.top) / rect.height) * 100;
      panel.style.setProperty("--ink-x", x + "%");
      panel.style.setProperty("--ink-y", y + "%");
    });
  });

  /* ---- Ink splash on click -------------------------------------------- */

  if (!reducedMotion.matches) {
    document.addEventListener("click", function (event) {
      if (event.target.closest("a, button, input, textarea, select")) return;
      if (!event.target.closest("main")) return;
      if (!event.clientX && !event.clientY) return;

      var splash = document.createElement("span");
      splash.className = "ink-splash";
      splash.setAttribute("aria-hidden", "true");
      splash.style.left = event.clientX + "px";
      splash.style.top = event.clientY + "px";
      document.body.appendChild(splash);

      window.setTimeout(function () {
        splash.remove();
      }, 750);
    });
  }

  /* ---- Reveal on scroll ----------------------------------------------- */

  if ("IntersectionObserver" in window && !reducedMotion.matches) {
    var targets = document.querySelectorAll(
      ".panel, .project, .repo, .spec-grid > div, .gauge, .rev"
    );

    var revealObserver = new IntersectionObserver(
      function (entries, self) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          self.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -6% 0px", threshold: 0.05 }
    );

    Array.prototype.forEach.call(targets, function (element, index) {
      element.classList.add("reveal");
      element.style.transitionDelay = Math.min(index % 6, 5) * 35 + "ms";
      revealObserver.observe(element);
    });
  }

  /* ---- Footer year ---------------------------------------------------- */

  var year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());
})();

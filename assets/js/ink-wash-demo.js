/**
 * Ink Wash demo — progressive enhancement
 * Ink drop on click, scroll nav highlighting, reveal, light parallax.
 */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- Active section in sidebar nav ---------------------------------- */

  var navLinks = document.querySelectorAll(".nav-link");
  var sections = document.querySelectorAll("main section[id], main header[id]");

  if ("IntersectionObserver" in window && navLinks.length && sections.length) {
    var setActive = function (id) {
      navLinks.forEach(function (link) {
        var match = link.getAttribute("data-section") === id;
        link.classList.toggle("is-active", match);
        link.setAttribute("aria-current", match ? "true" : "false");
      });
    };

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) setActive(entry.target.id);
        });
      },
      { rootMargin: "-25% 0px -60% 0px" }
    );

    sections.forEach(function (section) {
      observer.observe(section);
    });
  }

  /* ---- Scroll reveal -------------------------------------------------- */

  if ("IntersectionObserver" in window && !reduced) {
    var reveals = document.querySelectorAll(".reveal");
    var revealObs = new IntersectionObserver(
      function (entries, self) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          self.unobserve(entry.target);
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
    );
    reveals.forEach(function (el) {
      revealObs.observe(el);
    });
  } else {
    document.querySelectorAll(".reveal").forEach(function (el) {
      el.classList.add("is-visible");
    });
  }

  /* ---- Ink drop on click ---------------------------------------------- */

  if (!reduced) {
    document.addEventListener("click", function (event) {
      if (event.target.closest("a, button, input, textarea, select, nav")) return;
      if (!event.clientX && !event.clientY) return;

      var drop = document.createElement("span");
      drop.className = "ink-drop";
      drop.setAttribute("aria-hidden", "true");
      drop.style.left = event.clientX + "px";
      drop.style.top = event.clientY + "px";
      document.body.appendChild(drop);

      window.setTimeout(function () {
        drop.remove();
      }, 2500);
    });
  }

  /* ---- Gallery card ink spread on hover ------------------------------- */

  document.querySelectorAll(".gallery-card").forEach(function (card) {
    card.addEventListener("mousemove", function (event) {
      var rect = card.getBoundingClientRect();
      var x = ((event.clientX - rect.left) / rect.width) * 100;
      var y = ((event.clientY - rect.top) / rect.height) * 100;
      card.style.backgroundImage =
        "radial-gradient(circle at " +
        x +
        "% " +
        y +
        "%, rgb(26 26 26 / 0.04), transparent 55%)";
    });
    card.addEventListener("mouseleave", function () {
      card.style.backgroundImage = "";
    });
  });

  /* ---- Light scroll parallax on hero ---------------------------------- */

  var hero = document.getElementById("hero");
  if (hero && !reduced) {
    window.addEventListener(
      "scroll",
      function () {
        var y = window.scrollY;
        var opacity = Math.min(y / 600, 1);
        hero.style.setProperty("--parallax-opacity", String(1 - opacity * 0.3));
        hero.style.opacity = String(1 - opacity * 0.25);
      },
      { passive: true }
    );
  }

  /* ---- Footer year ---------------------------------------------------- */

  var year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());
})();

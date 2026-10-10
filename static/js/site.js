document.addEventListener("DOMContentLoaded", () => {
  const choiceButtons = document.querySelectorAll("[data-choice-id]");

  choiceButtons.forEach((button) => {
    button.addEventListener("click", async () => {
      if (button.classList.contains("is-selected")) return;

      button.classList.add("is-selected");

      let weight = {};
      try {
        weight = JSON.parse(button.dataset.weight || "{}");
      } catch (_) {}

      try {
        await fetch("/api/save-choice/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
          body: JSON.stringify({
            choice: button.dataset.choiceId,
            weight,
          }),
        });
      } catch (_) {
        // The visual journey should continue even if analytics/API is unavailable.
      }

      const currentPath = window.location.pathname;

      // Give the selected state a moment to register visually before the page transition.
      await new Promise((resolve) => setTimeout(resolve, 420));

      if (currentPath === "/") {
        window.location.href = "/argument/2/";
      } else if (currentPath.includes("/argument/2/")) {
        window.location.href = "/argument/3/";
      } else {
        window.location.href = "/reveal/";
      }
    });
  });

  const toggle = document.querySelector(".menu-toggle");
  if (toggle) {
    toggle.addEventListener("click", () => {
      const open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      document.body.classList.toggle("menu-open", !open);
    });
  }

  function getCookie(name) {
    const cookie = document.cookie
      .split("; ")
      .find((row) => row.startsWith(`${name}=`));
    return cookie ? decodeURIComponent(cookie.split("=")[1]) : "";
  }

  function getCsrfToken() {
    const cookieToken = getCookie("csrftoken");
    if (cookieToken) return cookieToken;

    const input = document.querySelector(
      'input[name="csrfmiddlewaretoken"]'
    );
    return input ? input.value : "";
  }
});


  // Small editorial motion layer: reveal content as it enters the viewport.
  const revealItems = document.querySelectorAll(
    ".choice-card, .identity, .dna, .mini-journey, .why-block, .experience-block, .itinerary, .price-panel"
  );
  if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("in-view");
        obs.unobserve(entry.target);
      });
    }, { threshold: 0.12 });
    revealItems.forEach((item) => {
      item.classList.add("motion-ready");
      observer.observe(item);
    });
  }


  // Persistent day/night mode. The visual system stays the same;
  // only the canvas, surfaces, text and controls adapt.
  const themeToggle = document.querySelector(".theme-toggle");
  const themeMeta = document.querySelector("#theme-color-meta");

  function applyTheme(theme) {
    const isLight = theme === "light";
    document.documentElement.dataset.theme = isLight ? "light" : "dark";

    if (themeToggle) {
      themeToggle.setAttribute("aria-pressed", String(isLight));
      themeToggle.setAttribute("aria-label", isLight ? "Switch to night mode" : "Switch to day mode");
      const label = themeToggle.querySelector(".theme-label");
      if (label) label.textContent = isLight ? "DAY" : "NIGHT";
    }

    if (themeMeta) {
      themeMeta.setAttribute("content", isLight ? "#f8f6f0" : "#081716");
    }
  }

  const savedTheme = localStorage.getItem("joy-theme");
  applyTheme(savedTheme === "light" ? "light" : "dark");

  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      const next = document.documentElement.dataset.theme === "light" ? "dark" : "light";
      localStorage.setItem("joy-theme", next);
      applyTheme(next);
    });
  }

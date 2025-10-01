(function () {
  const STORAGE_KEY = "theme-preference";
  const root = document.documentElement;
  const toggle = document.getElementById("theme-toggle");

  // figure out starting theme (stored or system)
  const stored = localStorage.getItem(STORAGE_KEY);
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const initial = stored ?? (prefersDark ? "dark" : "light");
  setTheme(initial);

  // click to toggle
  toggle?.addEventListener("click", () => {
    const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    setTheme(next, true);
  });

  // follow system changes if user hasn’t chosen
  const mq = window.matchMedia("(prefers-color-scheme: dark)");
  mq.addEventListener?.("change", (e) => {
    if (!localStorage.getItem(STORAGE_KEY)) {
      setTheme(e.matches ? "dark" : "light");
    }
  });

  function setTheme(mode, persist = false) {
    root.setAttribute("data-theme", mode);
    if (persist) localStorage.setItem(STORAGE_KEY, mode);

    const pressed = mode === "dark";
    if (toggle) {
      toggle.setAttribute("aria-pressed", String(pressed));
      const icon = toggle.querySelector(".theme-toggle__icon");
      if (icon) icon.textContent = pressed ? "☀️" : "🌙";
    }
  }
})();

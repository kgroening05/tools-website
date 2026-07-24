(function () {
  const rawEl = document.getElementById("markdown-raw");
  const renderedEl = document.getElementById("markdown-rendered");
  const toggle = document.getElementById("view-toggle");
  const downloadBtn = document.getElementById("download-btn");
  const originalName = document.querySelector(".result").dataset.filename || "converted";
  if (!rawEl) return;  // page loaded without a result — nothing to wire up

  // --- Render markdown into the rendered view ---
  const rawText = rawEl.textContent;
  renderedEl.innerHTML = DOMPurify.sanitize(marked.parse(rawText));

  // --- View toggle (raw <-> rendered) ---
  function setView(mode) {
    const showRaw = mode === "raw";
    rawEl.hidden = !showRaw;
    renderedEl.hidden = showRaw;
    toggle.querySelectorAll("button").forEach(function (b) {
      b.setAttribute("aria-pressed", b.dataset.mode === mode ? "true" : "false");
    });
  }

  toggle.addEventListener("click", function (e) {
    const btn = e.target.closest("button[data-mode]");
    if (btn) setView(btn.dataset.mode);
  });

  setView("rendered");  // default

  // --- Download ---
  downloadBtn.addEventListener("click", function () {
    const blob = new Blob([rawText], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = mdFilename(originalName);
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  });

  function mdFilename(name) {
    const dot = name.lastIndexOf(".");
    const base = dot > 0 ? name.slice(0, dot) : name;
    return base + ".md";
  }
})();
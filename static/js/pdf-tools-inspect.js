import * as pdfjsLib from "/static/js/vendor/pdfjs/pdf.mjs";

// PDF.js needs to know where its worker file lives
pdfjsLib.GlobalWorkerOptions.workerSrc = "/static/js/vendor/pdfjs/pdf.worker.mjs";

const fileInput = document.querySelector('input[type="file"]');
const infoEl = document.getElementById("pdf-info");

fileInput.addEventListener("change", async (e) => {
  const file = e.target.files[0];
  if (!file) {
    infoEl.textContent = "";
    return;
  }

  infoEl.textContent = "Reading PDF...";

  try {
    const arrayBuffer = await file.arrayBuffer();
    const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
    infoEl.textContent = `${file.name} — ${pdf.numPages} pages`;
  } catch (err) {
    console.error(err);
    infoEl.textContent = `Could not read PDF: ${err.message}`;
  }
});
const fileInput = document.getElementById("image-input");
const updateBtn = document.getElementById("update-btn");
const resultEl = document.getElementById("result");
const outputFormatSelect = document.getElementById("format-select");
const qualityInput = document.getElementById("quality-input");
const numColumnsInput = document.getElementById("columns-input");
const imageInfo = document.getElementById("image-info");

updateBtn.addEventListener("click", updateOutput);

async function updateOutput() {
  const files = Array.from(fileInput.files);
  if (files.length === 0) {
    resultEl.textContent = "Please select at least one image.";
    return;
  }

  resultEl.textContent = "Rendering...";

  const numColumns = Number(numColumnsInput.value);
  const quality = Number(qualityInput.value) / 100;
  const format = outputFormatSelect.value;

  const images = await Promise.all(files.map(loadImage));

  const cellWidth = Math.max(...images.map(img => img.width));
  const cellHeight = Math.max(...images.map(img => img.height));
  const numRows = Math.ceil(images.length / numColumns);

  const canvas = document.createElement("canvas");
  canvas.width = cellWidth * numColumns;
  canvas.height = cellHeight * numRows;
  const ctx = canvas.getContext("2d");

  for (let i = 0; i < images.length; i++) {
    const col = i % numColumns;
    const row = Math.floor(i / numColumns);
    ctx.drawImage(images[i], col * cellWidth, row * cellHeight);
  }

  canvas.toBlob((blob) => {
    const url = URL.createObjectURL(blob);
    resultEl.innerHTML = "";
    const link = document.createElement("a");
    link.href = url;
    link.download = "collage." + format.split("/")[1];
    link.textContent = "Download Collage";
    resultEl.appendChild(link);
    resultEl.appendChild(canvas);
    imageInfo.textContent = `File size: ${Math.round(blob.size / 1024)} KB`;
  }, format, quality);

}

function loadImage(file) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => {
      URL.revokeObjectURL(img.src);
      resolve(img);
    };
    img.onerror = () => reject(new Error(`Failed to load: ${file.name}`));
    img.src = URL.createObjectURL(file);
  });
}
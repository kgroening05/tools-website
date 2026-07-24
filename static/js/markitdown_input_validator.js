(function () {
  const fileInput = document.querySelector('input[type="file"]');
  const errorSpan = document.getElementById('filesize-error-message');

  if (!fileInput) return;

  fileInput.addEventListener('change', function (e) {
    console.log('File input changed');
    const file = e.target.files[0];
    if (!file) return;

    errorSpan.textContent = ''; // Clear previous error messages

    const allowedTypes = ['.pdf', '.docx'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();

    if (!allowedTypes.includes(fileExtension)) {
      const message = `Invalid file type. Please upload a PDF or DOCX file.`;
      const errorSpan = document.getElementById('filetype-error-message');
      if (errorSpan) {
        errorSpan.textContent = message;
      }
      e.target.value = ''; // Clear the file input
    }

    const maxFileSize = 10 * 1024 * 1024; // 10 MB
    if (file.size > maxFileSize) {
      const message = `File size exceeds the 10 MB limit. Please upload a smaller file.`;
      if (errorSpan) {
        errorSpan.textContent = message;
      }
      e.target.value = ''; // Clear the file input
    }
  });

})();
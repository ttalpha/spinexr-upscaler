const dropZone = document.getElementById("drop-zone");
const errorMessage = document.getElementById("error-message");
const successUpload = document.getElementById("success-upload");
const wrongFile = document.getElementById("wrong-file");
const fileList = document.getElementById("file-list");
const dropInput = document.getElementById("drop-input");
const resetBtn = document.querySelector(".reset-btn");
const submitBtn = document.querySelector(".submit-btn");
const uploadBox = document.getElementById("upload-box");
const option = document.getElementById("option");
const progressContainer = document.getElementById("progress-container");
const wait = document.getElementById("wait");
// Prevent default drag behaviors
["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
  dropZone.addEventListener(eventName, preventDefaults, false);
  document.body.addEventListener(eventName, preventDefaults, false);
});

// Highlight drop zone when item is dragged over it
["dragenter", "dragover"].forEach((eventName) => {
  dropZone.addEventListener(eventName, highlight, false);
});

["dragleave", "drop"].forEach((eventName) => {
  dropZone.addEventListener(eventName, unhighlight, false);
});

// Handle dropped files
dropZone.addEventListener("drop", handleDrop, false);

// Handle button clicks
resetBtn.addEventListener("click", handleReset);
submitBtn.addEventListener("click", handleSubmit);

function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}

function highlight(e) {
  dropZone.classList.add("dragover");
}

function unhighlight(e) {
  dropZone.classList.remove("dragover");
}

document.querySelectorAll(".btn").forEach((button) => {
  button.addEventListener("click", () => {
    document
      .querySelectorAll(".btn")
      .forEach((btn) => btn.classList.remove("active"));
    button.classList.add("active");
  });
});

function handleDrop(e) {
  const dt = e.dataTransfer;
  const files = dt?.files || e.target?.files;

  // Create and show loading bar
  const loadingBar = document.createElement("div");
  loadingBar.classList.add("loading-bar");
  const progress = document.createElement("div");
  progress.classList.add("progress");
  loadingBar.appendChild(progress);
  dropZone.appendChild(loadingBar);

  // Start loading animation
  let progressWidth = 0;
  const interval = setInterval(() => {
    progressWidth += 5;
    progress.style.width = `${progressWidth}%`;
    if (progressWidth >= 100) {
      clearInterval(interval);
      loadingBar.remove(); // Remove loading bar when complete
      handleFiles(files); // Process files after loading
    }
  }, 50);
}

function handleFiles(files) {
  fileList.innerHTML = ""; // Clear existing list
  let hasValidFiles = false;

  for (const file of files) {
    if (file) {
      // Check if there is a file
      if (
        file.type === "application/dicom" ||
        file.name.toLowerCase().endsWith(".dicom") ||
        file.name.toLowerCase().endsWith(".dcm")
      ) {
        hasValidFiles = true;

        // Create preview container
        const previewArea = document.createElement("div");
        previewArea.className = "preview-area";

        // Append DICOM preview area to preview container
        fileList.appendChild(previewArea);

        // Create a div for file name and remove button
        const div = document.createElement("div");
        div.className = "file-item";
        div.innerHTML = `
            <span>${file.name}</span>
            <svg class="remove-file-btn" data-filename="${file.name}" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 6 6 18"/>
              <path d="m6 6 12 12"/>
            </svg>`;

        // Append file item to fileList
        fileList.appendChild(div);

        // Read and render DICOM file
        const fileReader = new FileReader();
        fileReader.onload = function () {};

        // Read file as ArrayBuffer (needed for DICOM processing)
        fileReader.readAsArrayBuffer(file);
      } else {
        wrongFile.style.display = "block"; // Show wrong file message
        setTimeout(() => {
          wrongFile.style.display = "none";
        }, 5000);
      }
    }
  }

  // Add event listener to remove file
  document.querySelectorAll(".remove-file-btn").forEach((btn) => {
    btn.addEventListener("click", function () {
      const fileName = this.getAttribute("data-filename");

      // Find and remove the corresponding file item
      const fileItem = this.closest(".file-item");
      if (fileItem) fileItem.remove();

      // Find and remove the corresponding DICOM preview
      const preview = fileList.querySelector(".preview-area");
      if (preview) preview.remove();

      // Hide buttons if no valid files remain
      if (!fileList.querySelector(".file-item")) {
        resetBtn.style.display = "block";
        submitBtn.style.display = "block";
      }
    });
  });

  // Show buttons when files are added
  if (hasValidFiles) {
    resetBtn.style.display = "block";
    submitBtn.style.display = "block";
  }
}

// Update handleReset function to restore original state
function handleReset() {
  // Clear the file list and hide buttons
  fileList.innerHTML = "";
  errorMessage.classList.add("hidden");
}

let selectedScale = 2;
let selectedBitDepth = 8;
let uploadData = [];

// Handle scale button clicks
document.querySelectorAll(".scale-btn").forEach((button) => {
  button.addEventListener("click", function () {
    document
      .querySelectorAll(".scale-btn")
      .forEach((btn) => btn.classList.remove("active"));
    this.classList.add("active");
    selectedScale = +this.getAttribute("data-value");
  });
});

// Handle bit depth selection
const bitSelect = document.getElementById("bit-select");
bitSelect.addEventListener("change", function () {
  selectedBitDepth = +this.value; // Get selected value
});

// Update handlesubmit function to show full image
async function handleSubmit() {
  // Clear everything except the last preview
  const previews = document.querySelectorAll(".preview-area");
  const lastPreview = previews[previews.length - 1];
  errorMessage.classList.add("hidden");
  errorMessage.style.display = "none";

  if (!fileList.querySelector(".file-item")) {
    // Show error message after 7 seconds
    errorMessage.style.display = "block"; // Show error message
    setTimeout(() => {
      errorMessage.style.display = "none"; // Hide error message after 7 seconds
    }, 5000);
    return; // Exit if no files are present
  }
  const formData = new FormData();

  formData.append("scale", selectedScale);
  formData.append("bitDepth", selectedBitDepth);

  // Append each file to the FormData object and push to uploadData array
  const files = Array.from(fileList.querySelectorAll(".file-item"));

  files.forEach((file) => {
    if (file) {
      formData.append("files", file); // Append file to FormData
    }
  });

  // Send the files to the server
  try {
    // const response = await fetch("http://47.236.113.136:8080", {
    //   method: "POST",
    //   body: formData,
    // });

    uploadBox.style.display = "none";
    option.style.display = "none";

    successUpload.style.display = "block";
    setTimeout(() => {
      successUpload.style.display = "none";
    }, 5000);
    console.log("success");

    processBar();

    wait.style.display = "block";
  } catch (error) {
    console.error("Error:", error);
    errorMessage.textContent = "Error submitting files. Please try again.";
    errorMessage.style.display = "block";
  }
  // Hide buttons after submitting
  resetBtn.style.display = "none";
  submitBtn.style.display = "none";
}

function processBar() {
  progressContainer.style.display = "flex";
  const progressBar = document.createElement("div");
  progressBar.classList.add("progress-bar");
  const progress = document.createElement("div");
  progress.classList.add("progress");
  progressBar.appendChild(progress);
  progressContainer.appendChild(progressBar); // Append the progress bar to the body

  // Start loading animation
  let progressWidth = 0;
  const interval = setInterval(() => {
    progressWidth += 5;
    progress.style.width = `${progressWidth}%`;
    if (progressWidth >= 100) {
      clearInterval(interval);
      progressBar.remove(); // Remove loading bar when complete
    }
  }, 1000);
}

document.querySelector(".submit-btn").addEventListener("click", handleSubmit);
dropInput.addEventListener("input", handleDrop);

resetBtn.addEventListener("click", handleReset);
submitBtn.addEventListener("click", handleSubmit);

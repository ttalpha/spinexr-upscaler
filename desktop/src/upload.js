const dropZone = document.getElementById("drop-zone");
const errorMessage = document.getElementById("error-message");
const successUpload = document.getElementById("success-upload");
const wrongFile = document.getElementById("wrong-file");
const fileList = document.getElementById("file-list");
const dropInput = document.getElementById("drop-input");
const resetBtn = document.querySelector(".reset-btn");
const submitBtn = document.querySelector(".submit-btn");
const uploadBox = document.getElementById("upload-box");
const progressContainer = document.getElementById("progress-container");
const resultsContainer = document.getElementById("results-container");
const submitFiles = [];

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
  let validFileCount = 0; // Counter for valid files

  for (const file of files) {
    if (file) {
      // Check if there is a file
      if (
        validFileCount < 3 && // Limit to a maximum of 3 files
        (file.type === "application/dicom" ||
          file.name.toLowerCase().endsWith(".dicom") ||
          file.name.toLowerCase().endsWith(".dcm"))
      ) {
        hasValidFiles = true;
        validFileCount++;

        const div = document.createElement("div");
        div.className = "file-item";
        div.innerHTML = `
            <span>${file.name}</span>
            <img src="trash-icon.svg" class="remove-file-btn" data-filename="${file.name}"/>
            `;

        // Append file item to fileList
        fileList.appendChild(div);
        submitFiles.push(file);
      } else if (validFileCount >= 3) {
        // Show message if more than 3 files are attempted to be uploaded
        wrongFile.style.display = "block"; // Show wrong file message
        wrongFile.textContent = "You can only upload a maximum of 3 files.";
        setTimeout(() => {
          wrongFile.style.display = "none";
        }, 5000);
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
      const index = submitFiles.findIndex((file) => file.name === fileName);

      // Find and remove the corresponding file item
      const fileItem = this.closest(".file-item");
      if (fileItem) fileItem.remove();

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

// Update handlesubmit function to show full image
async function handleSubmit() {
  // Clear everything except the last preview
  errorMessage.classList.add("hidden");
  errorMessage.style.display = "none";

  if (!fileList.querySelector(".file-item")) {
    // Show error message after 5 seconds
    errorMessage.style.display = "block"; // Show error message
    setTimeout(() => {
      errorMessage.style.display = "none"; // Hide error message after 5 seconds
    }, 5000);
    return; // Exit if no files are present
  }
  const formData = new FormData();
  formData.append("files", submitFiles);

  // Send the files to the server
  try {
    // const response = await fetch("http://47.236.113.136:8080", {
    //   method: "POST",
    //   body: formData,
    // });

    uploadBox.style.display = "none";

    successUpload.style.display = "block";
    setTimeout(() => {
      successUpload.style.display = "none";
    }, 5000);

    processBar();
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
      results();
    }
  }, 500);
}

function results() {
  progressContainer.style.display = "none";
  resultsContainer.style.display = "flex";
  // Create a container for the results
  fileList.innerHTML = "";

  for (const file of submitFiles) {
    const fileItem = document.createElement("div");
    fileItem.className = "file-item";

    fileItem.innerHTML = `
    <div class="near-by">
      <img src="file-icon.svg"/>
      <span>${file.name}</span>
    </div>
    <div class="near-by">
      <img src="download-icon.svg" class="download-file-btn" data-filename="${file.name}"/>
    </div>
    `;
    const downloadBtn = fileItem.querySelector(".download-file-btn");
    downloadBtn.addEventListener("click", function () {
      downloadFile(file.name); // Call the download function
    });
    resultsContainer.appendChild(fileItem);
  }
}

function downloadFile(fileName) {
  const fileData = new Blob(["Dummy content for " + fileName], {
    type: "application/octet-stream",
  });
  const url = URL.createObjectURL(fileData);

  const a = document.createElement("a");
  a.href = url;
  a.download = fileName; // Set the file name for download
  document.body.appendChild(a);
  a.click(); // Trigger the download
  document.body.removeChild(a);
  URL.revokeObjectURL(url); // Clean up the URL object
}

document.querySelector(".submit-btn").addEventListener("click", handleSubmit);
dropInput.addEventListener("input", handleDrop);

resetBtn.addEventListener("click", handleReset);
submitBtn.addEventListener("click", handleSubmit);

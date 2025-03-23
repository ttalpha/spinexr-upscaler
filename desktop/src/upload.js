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
const resultsContainer = document.getElementById("results-container");
const title = document.getElementById("title");
const subTitle = document.getElementById("sub-title");

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
        validFileCount++; // Increment valid file count

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
            <img src="trash-icon.svg" class="remove-file-btn" data-filename="${file.name}"/>
            `;

        // Append file item to fileList
        fileList.appendChild(div);

        // Read file as ArrayBuffer (needed for DICOM processing)
        const fileReader = new FileReader();
        fileReader.onload = function () {};
        fileReader.readAsArrayBuffer(file);
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

let listFiles = [];

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
      const fileName = file.querySelector("span").textContent;
      listFiles.push(fileName);
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

    wait.style.display = "block";
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
      wait.style.display = "none";
      results();
    }
  }, 500);
}

function results() {
  progressContainer.style.display = "none";
  resultsContainer.style.display = "flex";
  title.style.display = "block";
  // Create a container for the results
  fileList.innerHTML = "";
  const resultsPreviewArea = document.createElement("div");
  resultsPreviewArea.className = "preview-area"; // Add a class for styling

  // Display each uploaded file in the results
  fileList.appendChild(resultsPreviewArea);
  while (listFiles.length > 0) {
    const fileName = listFiles.pop(); // Pop the last file name from the array

    // Create a div for each file preview
    const div = document.createElement("div");
    div.className = "file-item";

    div.innerHTML = `
    <div class="near-by">   
    <img src="file-icon.svg"/>
            <span>${fileName}</span>
            </div>
            <div class="near-by">
            <img src="download-icon.svg" class="download-file-btn" data-filename="${fileName}"/>
            <img src="trash-icon.svg" class="remove-file-btn" data-filename="${fileName}"/>
</div>
    `;
    // Append the file preview to the results preview area
    resultsPreviewArea.appendChild(div);
    const downloadBtn = div.querySelector(".download-file-btn");
    downloadBtn.addEventListener("click", function () {
      downloadFile(fileName); // Call the download function
    });

    // Add event listener for the remove button
    const removeBtn = div.querySelector(".remove-file-btn");
    removeBtn.addEventListener("click", function () {
      div.remove(); // Remove the file item from the results
    });
  }

  // Append the results preview area to the results container
  resultsContainer.appendChild(resultsPreviewArea);
  subTitle.style.display = "block";
}
function downloadFile(fileName) {
  // Assuming you have the file data available, you can create a Blob
  // For demonstration, let's create a dummy Blob. Replace this with actual file data.
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

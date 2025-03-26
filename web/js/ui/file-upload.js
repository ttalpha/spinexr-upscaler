// Store uploaded files, the index of the currently selected file for editing,
// and a copy of the original image before edits.
let files = [];
let selectedFileIndex = null;
let originalImage = null; // Store the original image for editing.

/**
 * Initializes the file upload and image editing UI.
 */
export function initFileUpload() {
  console.log('File upload initialized');

  // Get references to DOM elements.
  const goBack = document.getElementById('go-back-btn');
  const dropZone = document.getElementById('drop-zone');
  const fileInput = document.getElementById('file-input');
  const previewContainer = document.getElementById('preview-container');
  const convertBtn = document.getElementById('convert-btn');
  const editControls = document.getElementById('edit-controls');
  const cropWidthInput = document.getElementById('crop-width');
  const cropHeightInput = document.getElementById('crop-height');
  const resizeWidthInput = document.getElementById('resize-width');
  const resizeHeightInput = document.getElementById('resize-height');
  const rotateAngleInput = document.getElementById('rotate-angle');

  // --- Drag-and-Drop Event Handlers ---
  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault(); // Prevent default behavior to allow drop.
    console.log('Dragover event triggered');
    dropZone.classList.add('border-blue-500'); // Add visual cue.
  });

  dropZone.addEventListener('dragleave', () => {
    console.log('Dragleave event triggered');
    dropZone.classList.remove('border-blue-500'); // Remove visual cue.
  });

  dropZone.addEventListener('drop', (e) => {
    e.preventDefault(); // Prevent default browser behavior (opening the file).
    console.log('Drop event triggered', e.dataTransfer.files);
    dropZone.classList.remove('border-blue-500'); // Remove visual cue.
    handleFiles(e.dataTransfer.files); // Process the dropped files.
  });

  // --- File Input Event Handlers ---
  dropZone.addEventListener('click', () => {
    console.log('Drop zone clicked');
    fileInput.click(); // Trigger the file input's click event.
  });

  goBack.addEventListener('click', () => {
    location.reload();
    
  });

  fileInput.addEventListener('change', () => {
    console.log('File input changed', fileInput.files);
    handleFiles(fileInput.files); // Process the selected files.
    fileInput.value = ''; // Reset the input to allow re-selection of the same file.
  });



  /**
   * 
   * @param {number} index 
   */
  
  function showEditControls(index) {
    selectedFileIndex = index;
    editControls.classList.remove('hidden'); // Show the edit controls.
    const file = files[index];
    loadImageForPreview(file); // Load the image for editing.
  }
  function updateConvertButton() {
    convertBtn.disabled = files.length === 0; 
  }

  
  /**
   * 
   * @param {File} file 
   */
  function loadImageForPreview(file) {
    const img = new Image();
    img.onload = () => {
      originalImage = img; // Store the original image for editing.

      // Initialize input fields with the image's original dimensions.
      cropWidthInput.value = img.width;
      cropHeightInput.value = img.height;
      resizeWidthInput.value = img.width;
      resizeHeightInput.value = img.height;
      rotateAngleInput.value = 0; // Default rotation.

      updatePreview(); // Initial preview rendering.
    };
    img.onerror = (error) => console.error(`Failed to load image for preview: ${error.message}`);
    img.src = URL.createObjectURL(file); // Create a URL for the image.
  }


 

  /**
   * 
   * @param {FileList} newFiles The files to add.
   */
  function handleFiles(newFiles) {
    console.log('Handling files:', newFiles);

   
    const validFiles = Array.from(newFiles).filter((file) => {
      if (!file.type === "application/dicom" && !file.type.startsWith('/image')) {
        console.log(`Invalid file type for ${file.name}:`, file.type);
        return false; 
      }
      if (file.size > 5 * 1024 * 1024) { // 5MB limit
        console.log(`File too large for ${file.name}:`, file.size);
        return false; 
      }
      return true; 
    });

    if (validFiles.length === 0) {
      console.log('No valid image files');
      alert('Please upload valid image files.'); 
      return;
    }

    files = [...files, ...validFiles]; 
    console.log('Updated files:', files);
    updatePreviews(); 
    updateConvertButton(); 
  }
  
  function updatePreviews() {
    console.log('Updating previews for files:', files);
    previewContainer.innerHTML = ''; // Clear existing previews.

    files.forEach((file, index) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        console.log('Preview loaded for file:', file.name);
        // Create preview card elements.
        const previewCard = document.createElement('div');
        previewCard.className = 'preview-card';

        const img = document.createElement('img');
        img.src = e.target.result; // Set the image source to the data URL.
        img.className = 'preview-image';
        img.alt = file.name;

        const removeBtn = document.createElement('button');
        removeBtn.className = 'remove-btn';
        removeBtn.innerHTML = 'X'; 
        removeBtn.title = 'Remove image';
        removeBtn.setAttribute('aria-label', `Remove ${file.name}`);
        removeBtn.addEventListener('click', () => {
          console.log('Removing file:', file.name);
          files.splice(index, 1); // Remove the file from the array.
          updatePreviews(); // Update the previews.
          updateConvertButton(); // Update the convert button state.
        });

        const editBtn = document.createElement('button');
        editBtn.className = 'edit-btn';
        editBtn.innerHTML = 'Edit';
        editBtn.title = 'Edit image';
        editBtn.setAttribute('aria-label', `Edit ${file.name}`);
        editBtn.addEventListener('click', () => {
          showEditControls(index); // Show edit controls for this image.
        });

        // Assemble the preview card.
        previewCard.appendChild(img);
        previewCard.appendChild(removeBtn);
        
        previewContainer.appendChild(previewCard);
      };
      reader.readAsDataURL(file); // Read the file as a data URL (for preview).
    });
  }


}

/**
 * Returns the array of currently uploaded files.
 * @returns {Array<File>} The array of files.
 */
export function getFiles() {
  return files;
}

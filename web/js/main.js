// Import necessary modules from other files.
import { initFileUpload, getFiles } from './ui/file-upload.js';


// Wait for the DOM to be fully loaded before running the main logic.
document.addEventListener('DOMContentLoaded', () => {
  // Log a message to the console to indicate that main.js has loaded.
  console.log('Main.js loaded');

  // Initialize the file upload functionality (drag-and-drop and file input).
 async function name(params) {
  
 } initFileUpload();
  // Get references to DOM elements.
  const resultPage = document.getElementById('result-page')
  const convertBtn = document.getElementById('convert-btn');
  const formatSelect = document.getElementById('format-select');
  const progressContainer = document.getElementById('progress-container');
  const progressBar = document.getElementById('progress-bar');
  const progressText = document.getElementById('progress-text');

  // Add a click event listener to the convert button.
  convertBtn.addEventListener('click', async () => {
   
    console.log('Convert button clicked');
    const files = getFiles();
    const outputFormat = formatSelect.value;

    if (files.length === 0) {
      alert('Please upload files to convert.');
      return;
    }
    
    
    document.body.innerHTML = '';
    document.body.appendChild(resultPage);
    resultPage.classList.remove('hidden')  
    });
   
    
    

    document.getElementById('convert-btn').addEventListener('click', function () {
      const files = getFiles(); // Retrieve uploaded files
      if (files.length === 0) {
        alert('Please upload files to convert.');
        return;
      }
      
      const processedImages = [];
      const resultContainer = document.getElementById('result-container');
      resultContainer.innerHTML = ''; // Clear previous results
    
      files.forEach((file, index) => {
        const imageCard = document.createElement('div');
        imageCard.className = 'flex items-center bg-gray-100 border-2 border-line border-gray-400 rounded-lg p-4 gap-4'; // Flexbox for alignment
    
        const img = document.createElement('img');
        img.src = URL.createObjectURL(file); // Generate a preview URL
        img.alt = file.name;
        img.className = 'w-48 h-auto rounded-md';
    
        const downloadBtn = document.createElement('a');
        downloadBtn.href = img.src;
        downloadBtn.download = file.name;
        downloadBtn.innerText = '⤓';
        downloadBtn.className = 'text-white text-sm font-black bg-gray-500 rounded-full px-4 py-2 hover:bg-gray-600';
    
        imageCard.appendChild(img);
        imageCard.appendChild(downloadBtn);
        resultContainer.appendChild(imageCard);
    
        processedImages.push(img.src); // Store the preview URL
      });
    
      localStorage.setItem('processedImages', JSON.stringify(processedImages)); // Save processed images
    });
    
    
    

    


    // Show the progress bar and initialize its state.
    progressContainer.classList.remove('hidden');
    progressBar.style.width = '0%';
    progressText.textContent = 'Processing: 0%';


  
});
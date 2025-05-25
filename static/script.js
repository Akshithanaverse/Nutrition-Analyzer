document.getElementById('uploadForm').addEventListener('submit', function() {
    document.getElementById('loading').style.display = 'block';
});

document.getElementById('imageInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = function() {
        const img = document.getElementById('uploadedImage');
        img.src = reader.result;
        img.classList.remove('hidden'); 
        img.style.display = 'block';
    };

    if (file) {
        reader.readAsDataURL(file);
    }
});

// Toggle Dark Mode
document.getElementById('theme-toggle').addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');
});

window.onload = function() {
    const outputText = document.querySelector('.output-container p');
    if (outputText) {
        // outputText.style.fontWeight = "bold";
        outputText.style.fontSize = "1.1rem";
    }
};
window.onload = function() {
    const outputContainer = document.querySelector('.output-container');
    if (outputContainer) {
        // Convert **bold text** to <strong>bold text</strong>
        outputContainer.innerHTML = outputContainer.innerHTML.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    }

    // Hide loading message when output appears
    document.getElementById('loading').style.display = 'none';
};

const BACKEND_URL = '/api';
document.getElementById('uploadForm').addEventListener('submit', function (e) {
    e.preventDefault();
    uploadImage();
});

document.addEventListener('DOMContentLoaded', function () {
    loadImagesFromServer();
});

function uploadImage() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select a file to upload.');
        return;
    }
    const formData = new FormData();
    formData.append('image', file);
    fetch(`${BACKEND_URL}/upload`, {
        method: 'POST',
        body: formData
    }).then(async response => {
        if (!response.ok) {
            return response.text().then(text => {
                let message;
                try {
                    const json = JSON.parse(text);
                    message = json.error || 'Something went wrong.';
                    console.error('Error:', json);
                } catch {
                    message = text || 'Unexpected error.';
                }
                alert(message);
            });
        }
        return response.json();
    }).then(() => {
        loadImagesFromServer();
    }).catch(error => {
        console.error('Error:', error);
    });
}

function loadImagesFromServer() {
    fetch(`${BACKEND_URL}/getImages`, {
        method: 'GET'
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(data => {
        const images = data.images;
        const imageListElement = document.getElementById('imageList');
        imageListElement.innerHTML = '';
        images.forEach(image => {
            const imgElement = document.createElement('img');
            imgElement.alt = image.filename;
            imgElement.src = `data:image/*;base64,${image.data}`;
            imgElement.style.width = '100px';
            imgElement.style.margin = '5px';
            imageListElement.appendChild(imgElement);
        });
    }).catch(error => {
        console.error('Error:', error);
    });
}
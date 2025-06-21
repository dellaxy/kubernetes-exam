const BACKEND_URL = '/api';

const imageListElement = document.getElementById('imageList')
const uploadForm = document.getElementById('uploadForm')


uploadForm.addEventListener('submit', function (event) {
    event.preventDefault();
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
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
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
    }).then(images => {
        imageListElement.innerHTML = '';
        images.forEach(image => {
            const imgElement = document.createElement('img');
            imgElement.alt = image;
            imgElement.style.width = '100px';
            imgElement.style.margin = '5px';
            imageListElement.appendChild(imgElement);
        });
    }).catch(error => {
        console.error('Error:', error);
    });
}
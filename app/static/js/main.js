// static/js/main.js
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const thumbnailContainer = document.getElementById('thumbnailContainer');
const photoCount = document.getElementById('photoCount');
const status = document.getElementById('status');
const prompt = document.getElementById('prompt');
const uploadAndNextBtn = document.getElementById('uploadAndNext');
const takePhotoBtn = document.getElementById('takePhoto');
let capturedPhotos = [];
let stream = null;

function showStatus(message, duration = 2000) {
    status.textContent = message;
    status.style.display = 'block';
    setTimeout(() => {
        status.style.display = 'none';
    }, duration);
}

function updatePhotoCount() {
    photoCount.textContent = capturedPhotos.length === 0
        ? 'No photos'
        : `${capturedPhotos.length} photo${capturedPhotos.length === 1 ? '' : 's'}`;
    uploadAndNextBtn.disabled = capturedPhotos.length === 0;
}

function addThumbnail(imageData, index) {
    const wrapper = document.createElement('div');
    wrapper.className = 'thumbnail-wrapper';

    const img = document.createElement('img');
    img.src = imageData;
    img.className = 'thumbnail';

    const undoButton = document.createElement('button');
    undoButton.className = 'undo-button';
    undoButton.innerHTML = '×';
    undoButton.onclick = (e) => {
        e.stopPropagation();
        capturedPhotos.splice(index, 1);
        updateThumbnails();
        updatePhotoCount();
    };

    wrapper.appendChild(img);
    wrapper.appendChild(undoButton);
    thumbnailContainer.appendChild(wrapper);
}

function updateThumbnails() {
    thumbnailContainer.innerHTML = '';
    capturedPhotos.forEach((photo, index) => addThumbnail(photo, index));
}

// Start camera with user gesture
document.getElementById('startCamera').addEventListener('click', async () => {
    try {
        if (navigator.mediaDevices?.getUserMedia === undefined) {
            navigator.mediaDevices = {};
        }

        stream = await navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: 'environment',
                width: { ideal: 1920 },
                height: { ideal: 1080 }
            }
        });

        video.srcObject = stream;
        await video.play();
        prompt.style.display = 'none';
        takePhotoBtn.disabled = false;

    } catch (error) {
        showStatus('Camera error: ' + error.message);
    }
});

// Take photo using direct camera access
takePhotoBtn.addEventListener('click', () => {
    if (!stream) return;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0);

    const imageData = canvas.toDataURL('image/jpeg');
    capturedPhotos.push(imageData);
    updateThumbnails();
    updatePhotoCount();
});

// Upload and process photos
uploadAndNextBtn.addEventListener('click', () => {
    CameraApp.handleUploadAndNext(capturedPhotos, showStatus, updateThumbnails, updatePhotoCount);
});

// Initialize
updatePhotoCount();
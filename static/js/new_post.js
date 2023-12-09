let isDrawing = false;
let eraseEnable = false;
let lineThicknessInput;

let canvas;
let ctx;

function startDrawing(e) {
    e.preventDefault();
    isDrawing = true;
    ctx.beginPath();
    ctx.moveTo(e.offsetX, e.offsetY);
}

function draw(e) {
    e.preventDefault();
    if (!isDrawing) return;
    ctx.lineWidth = lineThicknessInput.value;
    if (eraseEnable) {
        ctx.clearRect(e.offsetX, e.offsetY, lineThicknessInput.value, lineThicknessInput.value);
    } else {
        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.stroke();
    }
}

function stopDrawing(e) {
    e.preventDefault();
    isDrawing = false;
    ctx.closePath();
}

function toggleErase() {
    eraseEnable = !eraseEnable; 
}

function clearCanvas(){
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function onSave() {
    const imageDataURL = canvas.toDataURL('image/jpeg', 1.0);
    const base64Data = imageDataURL.split(',')[1];

    const postData = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        image: base64Data
    }

    // Make the POST request using the Fetch API
    fetch('/post/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData)
    })
    .then(response => {
        if (!response.ok) 
            throw new Error("Network response was not OK.");

        return response.json();
    })
    .then(data => {
        // todo: here we grab the id of the post
        window.location.href = "/post/0";
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function InitializeCanvas() {
    canvas = document.querySelector('#c');
    ctx = canvas.getContext('2d');

    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, 512, 512);

    canvas.addEventListener("mouseup", stopDrawing);
    canvas.addEventListener("mousedown", startDrawing);
    canvas.addEventListener("mousemove", draw);
    canvas.addEventListener("mouseout", stopDrawing);
} 

document.addEventListener("DOMContentLoaded", function () {
    InitializeCanvas();
    lineThicknessInput = document.getElementById('ln_thk');
    document.querySelector('#save').addEventListener('click', onSave);
    document.querySelector('#ln_ers').addEventListener('click', toggleErase);
    document.querySelector('#ln_clr').addEventListener('click',clearCanvas);
});
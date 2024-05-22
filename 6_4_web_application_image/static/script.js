 function toggleMenu() {
    var menu = document.getElementById("menu");
    if (menu.style.display === "none") {
        menu.style.display = "block";
    } else {
        menu.style.display = "none";
    }
}

 function repaint(){
    var brightness = document.getElementById("brightness").value;
    var contrast = document.getElementById("contrast").value;
    var sharpness = document.getElementById("sharpness").value;
    var color = document.getElementById("color").value;
    console.log("Brightness:", brightness, "Contrast:", contrast, "Sharpness:", sharpness,"Color:", color);

    var imageUrl = document.getElementById("original-image-url").value;

    fetch('/update_image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            brightness: brightness,
            contrast: contrast,
            sharpness: sharpness,
            color: color,
            url: imageUrl
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.processed_image_url) {
            document.getElementById("uploaded-image").src = data.processed_image_url;
        }
    })
    .catch(error => console.error('Error:', error));
 }

 function downloadImage() {
    var imageUrl = document.getElementById("uploaded-image").src;
    var link = document.createElement('a');
    link.href = imageUrl;
    link.download = 'processed_image.jpg';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
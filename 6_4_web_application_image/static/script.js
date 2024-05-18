 function toggleMenu() {
    var menu = document.getElementById("menu");
    if (menu.style.display === "none") {
        menu.style.display = "block";
    } else {
        menu.style.display = "none";
    }
}

var brightnessSlider = document.getElementById("brightness");
var contrastSlider = document.getElementById("contrast");

brightnessSlider.addEventListener("input", function() {
    updateBrightness(this.value);
});

contrastSlider.addEventListener("input", function() {
    updateContrast(this.value);
});
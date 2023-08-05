console.log("onload.js fetched");
// window.addEventListener('DOMContentLoaded', function () {
window.onload = function () {
    console.log("onload.js loaded");
    // setTimeout(function () {
        var footer = document.querySelector('footer');
    
        if (footer) {
            footer.style.display = 'none';
        } else {
            console.log("footer not found");
        }
    // }, 1000);
};
// );
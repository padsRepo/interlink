let elm = document.getElementById("screenSize");
let width = window.innerWidth;
let height = window.innerHeight;
elm.outerHTML = width + "x" + height;
console.log("Screen Size Loaded.")
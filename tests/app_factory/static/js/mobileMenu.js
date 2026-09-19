var menu = document.getElementById("mobileMenu");
function openMenu(){
  if (menu.style.display == "block"){
    menu.style.display = "none";
  }
  else{
    menu.style.display = "block";
  }
}

var width = window.outerWidth;
var pTag = document.getElementById("greeting");
if (width <= "599"){
  pTag.style.display = "none";
}
else{
  pTag.style.display = "inline";
}

console.log("Mobile Menu Feature is Loaded")

//Slideshow Settings
var slideIndex = 0;
slideshow();
function slideshow(){
  var slides = document.getElementsByClassName("slide");
  var dots = document.getElementsByClassName("dot");
  for (var i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (var i = 0; i < dots.length; i++) {
    dots[i].style.display = "inline-block";
    dots[i].style.background = "grey";
  }
  slideIndex++;
  if (slideIndex > slides.length){slideIndex = 1}
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].style.background = "white";
  setTimeout(slideshow, 5000);
}
console.log("Slideshow Feature is Loaded")

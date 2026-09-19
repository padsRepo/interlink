function changeSlide(img, item){
  var image = document.getElementsByClassName("detailedImg");
  for (i = 0; i < image.length; i++){
    image[i].style.display = "none";
  }
  var highlight = document.getElementsByClassName("highlight");
  for (i = 0; i < highlight.length; i++){
    highlight[i].style.boxShadow = "";   
  }
  document.getElementById(img).style.display = "block";
  item.style.boxShadow = "2px 2px 10px white";
}
document.getElementById("default").click();
console.log("displaySlide Feature is loaded");
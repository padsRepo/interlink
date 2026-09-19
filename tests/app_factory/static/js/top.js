var up = document.getElementById('top');
window.onscroll = function(){scrollFunction()};
function scrollFunction(){
  if(document.body.scrollTop > 500 || document.documentElement.scrollTop > 500){
    up.style.display = "block";
  } else {
    up.style.display = "none";
  }
}
function topFunction(){
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}
console.log("Top Feature is Loaded")

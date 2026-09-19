function tab(page,item){
  content = document.getElementsByClassName("content");
  for (i = 0; i < content.length; i++){
    content[i].style.display = "none";
  }
  btn = document.getElementsByClassName("highlight");
  for (i = 0; i < btn.length; i++){
    btn[i].style.boxShadow = "";
  }
  document.getElementById(page).style.display = "block";
  item.style.boxShadow = "2px 2px 10px white";
}
document.getElementById("default").click();
console.log("Tab Feature is loaded");
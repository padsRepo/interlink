//Dark Mode Settings
function darkmode(){
  var x = document.body.style;
  var y = document.querySelector("header").style;

  if (x.backgroundColor === "black") {
    x.backgroundColor = "white";
    x.color = "black";
    y.border = "2px solid black";
    y.boxShadow = "10px 10px black";
  }else {
    x.backgroundColor = "black";
    x.color = "green";
    y.border = "2px solid green";
    y.boxShadow = "10px 10px black";
  }
}
console.log("Dark Mode Feature is Loaded")

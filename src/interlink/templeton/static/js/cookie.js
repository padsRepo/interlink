document.cookie = "user=; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
function getCookie(cname) {
  let name = cname + "=";
  let ca = document.cookie.split(';');
  for(let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}
function checkCookies() {
  var user = getCookie("user");
  if (navigator.cookieEnabled == true) {
    if (user == ""){
      var text = document.createElement("INPUT");
      text.setAttribute("id", "cname");
      text.setAttribute("type", "text");
      text.setAttribute("placeholder", "Enter a name: ");
      var submit = document.createElement("INPUT");
      submit.setAttribute("type", "submit");
      submit.setAttribute("value", "Submit");
      submit.setAttribute("onclick", "makeCookie()");
      document.body.appendChild(text);
      document.body.appendChild(submit);
    }
    else {
      text = "Welcome, " + getCookie("user");
    }
  } 
  else {
    text = "Cookies are not enabled.";
  }
  document.getElementById("cookie").innerText = text;
}

function makeCookie(){
  var x = document.getElementById("cname");
  document.cookie = "user=" + x;
  document.getElementById("cookie").innerText = "makeCookie" + document.cookie;
}
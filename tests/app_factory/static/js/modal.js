//Modal Settings
var btn = document.getElementById('btn');
var modal = document.getElementById('modal');
var modalContent = document.getElementById('modalContent');
var span = document.getElementById('close');

btn.onclick = function(){
  modal.style.display = "block";
  modalContent.style.display = "block";
}
span.onclick = function(){
  modal.style.display = "none";
  modalContent.style.display = "none";
}
modal.onclick = function(){
  modal.style.display = "none";
  modalContent.style.display = "none";
}

let d = luxon.DateTime;
let y = d.year;
const monthArray = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
let year = d.local(y).year;
let month = d.local(y).month;
let mdiv = document.getElementsByClassName("month");
let weeksInYear = d.local(y).weeksInWeekYear;
let week = d.local(y).weekNumber;

function clock(){
  let d = luxon.DateTime;
  let y = d.year;
  let h = ("0" + d.local(y).hour).slice(-2);
  let m = ("0" + d.local(y).minute).slice(-2);
  let s = ("0" + d.local(y).second).slice(-2);
  let year = d.local(y).year;
  let month = d.local(y).month;
  let day = d.local(y).day;
  let today = year + " " + monthArray[month] + " " + day;
  let time = h + ':' + m + ':' + s;
  document.getElementById("clock").innerText = today + ' @ ' + time;
}
setInterval(clock, 1000);

document.getElementById('copyright').outerText = " 2023-" + year;
document.getElementById("weekofyear").innerText = "Week: " + week + "/" + weeksInYear;
for (i = 0; i < month; i++){mdiv[i].style.backgroundColor = "red";}

console.log("Clock Feature is Loaded");

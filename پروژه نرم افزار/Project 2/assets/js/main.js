function responsiveMenu() {
  var x = document.getElementById("topMenu");
  if (x.className === "tm") {
    x.className += " responsive";
  } else {
    x.className = "tm";
  }
}

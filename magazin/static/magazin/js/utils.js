function getsize() {
    var win = window,
        doc = document,
        docElem = doc.documentElement,
        body = doc.getElementsByTagName('body')[0],
        x = win.innerWidth || docElem.clientWidth || body.clientWidth,
        y = win.innerHeight|| docElem.clientHeight|| body.clientHeight;
    return {width:x, height:y};
}

// Open the Modal
function openModal() {
  document.getElementById("myModal").style.display = "block";
}
// Close the Modal
function closeModal() {
  document.getElementById("myModal").style.display = "none";
}
var slideIndex = 1;
showSlides(slideIndex);
// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}
// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}
function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  // var dots = document.getElementsByClassName("demo");
  // var captionText = document.getElementById("caption");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  // for (i = 0; i < dots.length; i++) {
  //   dots[i].className = dots[i].className.replace(" active", "");
  // }
  slides[slideIndex-1].style.display = "block";
  // dots[slideIndex-1].className += " active";
  // captionText.innerHTML = dots[slideIndex-1].alt;
}

// evaluare produs
function fillStars(index){
  if(!rated) {
      for (let i = 0; i < 5; ++i) {
          let itag = document.getElementById("star-" + i)
          if (i <= index) {
              itag.classList.add("fa-star")
              itag.classList.remove("fa-star-o")
          } else {
              itag.classList.add("fa-star-o")
              itag.classList.remove("fa-star")
          }
      }
  }
}
function serialize(obj) {
  var str = [];
  for(var p in obj)
     str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
  return str.join("&");
}
function activateAlert(text, state="success"){
    alerttag = document.getElementById("alerteval")
    alert(state)
    alert(alerttag.classList.length)
    for(let i=0;i<alerttag.classList.length;++i)
    {
        let cls = alerttag.classList[i]
        if(cls.startsWith("alert-"))
            alerttag.classList.remove(cls)
    }
    alerttag.classList.add("alert-"+state)
    alerttag.classList.remove("d-none")
    document.getElementById("alerttext").innerHTML = text
    setTimeout(function () {document.getElementById("alerteval").classList.add("d-none")}, 5000 )
}
var rated = false
function rateproduct(i) {
  if(!rated)
  {
    httpRequest = new XMLHttpRequest()
    httpRequest.open('GET', window.location.href+"-----/rate/?"+serialize({stars: i+1}))
    httpRequest.send()
    httpRequest.onreadystatechange = function(){
    // Process the server response here.
    if (httpRequest.readyState === XMLHttpRequest.DONE) {
      if (httpRequest.status === 200) {
          activateAlert("<strong>Multumim!</strong> Evaluarea dvs a fost inregistrata!");
          rated = true
      }
      else{
          activateAlert('<strong>A aparut o eroare.</strong>', "danger");
      }
    }
    }
  }
}

// filter
function setprice() {
    let range = document.getElementById("pricerange"),
        span = document.getElementById("pretvalue");
    span.innerText = range.value
}

function checkinput(elem, value)
{
    // alert(elem.getAttribute("name") + " " + value)
    if(value.localeCompare("False") === 0){
        if(elem.hasAttribute("checked"))
            elem.removeAttribute("checked")
    }
    else{
        if(!elem.hasAttribute("checked"))
            elem.setAttribute("checked", "")
    }
}


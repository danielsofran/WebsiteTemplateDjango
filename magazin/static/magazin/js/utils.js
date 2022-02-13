function getsize()
{
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

var rated = false

function rateproduct(i)
{
  if(!rated)
  {
    rated = true
    $.ajax({
        type: 'GET',
        url: window.location.href + "/rate",
        data: {stars: i+1},
        success: function (response) {
            // more like a modal show here
            alert("Multumim!")
        },
        error: function (response) {
            // register error on server and contact admin
            alert(response["responseJSON"]["error"]);
        }
    })
  }
}

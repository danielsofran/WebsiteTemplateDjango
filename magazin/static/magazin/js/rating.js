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

function activateAlert(text, state="success"){
    alerttag = document.getElementById("alerteval")
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

function serialize(obj) {
  var str = [];
  for(var p in obj)
     str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
  return str.join("&");
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

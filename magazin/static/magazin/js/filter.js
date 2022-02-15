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


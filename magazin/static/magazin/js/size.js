// for slideshow breakpoint
function getsize() {
    var win = window,
        doc = document,
        docElem = doc.documentElement,
        body = doc.getElementsByTagName('body')[0],
        x = win.innerWidth || docElem.clientWidth || body.clientWidth,
        y = win.innerHeight|| docElem.clientHeight|| body.clientHeight;
    return {width:x, height:y};
}

function istall()
{
    let size = getsize()
    return size.height / size.width > 1.5;
}

function getsize() {
    var win = window,
        doc = document,
        docElem = doc.documentElement,
        body = doc.getElementsByTagName('body')[0],
        x = win.innerWidth || docElem.clientWidth || body.clientWidth,
        y = win.innerHeight|| docElem.clientHeight|| body.clientHeight;
    return {width:x, height:y};
}

function istall() {
    let size = getsize()
    if(size.height/size.width > 1.4)
        return true
    return false
}

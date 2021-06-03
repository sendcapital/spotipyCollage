// Get a reference to the button
let btn = document.getElementById("abtn");

// Add an event handler for the click event
// There is a much older way of doing this, which is using embedded event attributes
// like onclick, do not do this
btn.addEventListener("click", randomColor);

function randomColor() {
    // Converting to Hexadecimal numbers (base 16)
    // Since colors range from #000000 to #ffffff, there's 16**6 combinations of rgb colors
    let color = '#' + Math.floor(Math.random() * 16 ** 6).toString(16);

    // innerHTML property to get or set an HTML markup contained in the element
    document.getElementById("collage").style.background = color;
    // slicing string
    let contrast = '#' + invertHex(color.substring(1));
    document.getElementById("collage-header").style.color = contrast;
}

function invertHex(hex) {
    return (Number(`0x1${hex}`) ^ 0xFFFFFF).toString(16).substr(1).toUpperCase()
}